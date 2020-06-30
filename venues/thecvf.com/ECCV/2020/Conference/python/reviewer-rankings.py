import openreview
import csv
import time
from tqdm import tqdm
import argparse
from collections import defaultdict

reviewer_email_dict = {}

def get_profile(id):
    if id in reviewer_email_dict:
        return reviewer_email_dict.get(id)
    else:
        if '@' in id:
            profiles = client.search_profiles(emails=[id])
            reviewer_email_dict[id] = profiles.get(id)
            return reviewer_email_dict[id]
        else:
            profiles = client.search_profiles(ids=[id])
            return profiles[0] if profiles else None

def get_reviewer_details(tilde):
    profile = get_profile(tilde)
    
    if not profile:
        print('Line#27: profile not found for', tilde)
        return {'tilde':'', 'name': '', 'email': tilde}

    pref_name = []
    for name in profile.content['names']:
        if name.get('preferred'):
            pref_name = [name.get('first'), name.get('last')]
            if name.get('middle'):
                pref_name.insert(1, name.get('middle'))

    if not pref_name:
        name = profile.content['names'][0]
        pref_name = [name.get('first'), name.get('last')]
        if name.get('middle'):
            pref_name.insert(1, name.get('middle'))

    pref_email = profile.content.get('preferredEmail')
    if not pref_email:
        pref_email = profile.content['emailsConfirmed'][0]
    
    return {'tilde': profile.id, 'name': ' '.join(pref_name), 'email': pref_email}

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help='base url')
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--outfile')
    args = parser.parse_args()
    outfile = args.outfile if args.outfile else 'final_reviewer_ratings.csv'

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    # Step 0: Create maps for blind and withdrawn papers
    blind_notes = {note.id: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}

    withdrawn_notes = {note.id: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Withdrawn_Submission')}

    desk_rejected_notes = {note.id: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Desk_Rejected_Submission')}




    # Step 1: Gather all reviewers

    # Step 1.1: Reviewers from 21May file
    file_reviewers_ds = defaultdict(dict)
    print('Reading from file')
    with open('eccv20_internal_paper_reviewer_stats_21_may.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        count = 0
        for line in csv_reader:
            reviewer = line[1]
            paper_number = line[0]
            emergency = False if line[3] == 'thecvf.com/ECCV/2020/Conference' else True
            record = {
                'completed_at': line[2] if line[2] else None,
                'assigned_at': line[4],
                'assigned_by': line[3],
                'emergency': emergency
            }
            if '@' in reviewer:
                details = get_reviewer_details(reviewer)
                reviewer = details['tilde']
            file_reviewers_ds[reviewer][paper_number] = record
            count += 1
        print('Found {} records from file'.format(count))


    # Step 1.2: Gather new reviewers since the time this file was created
    map_current_reviewer_groups = {grp.id: grp for grp in openreview.tools.iterget_groups(
        client,
        regex='thecvf.com/ECCV/2020/Conference/Paper[0-9]+/AnonReviewer[0-9]+$') if len(grp.members)}
    print('Processing AnonReviewer groups')
    for grp_id, group in map_current_reviewer_groups.items():
        if group.members:
            paper_number = grp_id.split('Paper')[1].split('/')[0]
            reviewer = group.members[0]
            if reviewer not in file_reviewers_ds:
                reviewer_profile = get_profile(reviewer)
                reviewer = reviewer_profile.id

            if reviewer not in file_reviewers_ds or paper_number not in file_reviewers_ds.get(reviewer, {}):
                emergency = False if group.signatures[0] == 'thecvf.com/ECCV/2020/Conference' else True
                record = {
                    'completed_at': None,
                    'assigned_at': group.cdate, # Using the AnonReviewerX group's cdate as assigned_date
                    'assigned_by': group.signatures[0],
                    'emergency': emergency
                }
                file_reviewers_ds[reviewer][paper_number] = record
    print('Processed {} AnonReviewer groups'.format(len(map_current_reviewer_groups)))



    # Step 2: Find ALL reviews (regardless of whether the paper is withdrawn or not)
    reviews = openreview.tools.iterget_notes(client, invitation='^thecvf.com/ECCV/2020/Conference/Paper[0-9]+/-/Official_Review$')
    print('Processing Official reviews')
    for idx, review in enumerate(reviews):
        paper_number = review.invitation.split('Paper')[1].split('/')[0]
        reviewer_group_id = review.signatures[0]
        reviewer_group = map_current_reviewer_groups.get(reviewer_group_id)
        if reviewer_group:
            reviewer = reviewer_group.members[0]
        else:
            print('Line#133: Reviewer not found for {}'.format(reviewer_group))
            reviewer = get_profile(review.tauthor).id
            print('Line#135: Found id {}'.format(reviewer))

        reviewer_records = file_reviewers_ds.get(reviewer, {})
        if not reviewer_records:
            print('Line#139: Not found reviewer {} for paper {}'.format(reviewer, paper_number))

        record = reviewer_records.get(paper_number, {})
        if record and not record['completed_at']:
            record['completed_at'] = review.tcdate
        count += 1
    
    print('Processed {} official reviews'.format(idx+1))




    # Step 3: Get emergency assignment edges to identify emergency assignments
    emergency_edges = openreview.tools.iterget_edges(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Paper_Assignment',
        label='emergency-assignment-4')

    print('Processing Emergency assignment edges')
    for idx, edge in enumerate(emergency_edges):
        paper = blind_notes.get(edge.head) or withdrawn_notes.get(edge.head) or desk_rejected_notes.get(edge.head)
        paper_number = str(paper.number) if paper else None
        if not paper_number:
            # This must be a desk rejected paper
            print('Line#163: Paper not found in ds: edge.id:{}, paper:{}'.format(edge.id, paper_number))
            continue

        reviewer = edge.tail

        # find this record and set emergency=True
        record = file_reviewers_ds.get(reviewer, {}).get(paper_number)
        if record:
            record['emergency'] = True
        else:
            print('Line#173: Assignment missing for edge: reviewer:{}, paper:{}'.format(reviewer, paper_number))
            file_reviewers_ds[reviewer][paper_number] = {
                'completed_at': None,
                'assigned_at': None,
                'assigned_by': None,
                'emergency': True
            }

    print('Processed {} edges'.format(idx+1))




    # Step 4: Get all review ratings and organize it
    map_ratings = defaultdict(dict)
    review_ratings = openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/AnonReviewer[0-9]*/-/Review_Rating$'
    )
    print('Processing Review Ratings')
    for idx, rating in enumerate(review_ratings):
        paper_number = rating.invitation.split('Paper')[1].split('/')[0]
        anon_rev_group = rating.invitation.split('/-/')[0]
        reviewer_group = map_current_reviewer_groups.get(anon_rev_group)
        if not reviewer_group:
            print('Line#198: {} not found in current reviewer groups'.format(anon_rev_group))
        reviewer = reviewer_group.members[0]
        map_ratings[reviewer][paper_number] = int(rating.content['rating'].split(':')[0])

    print('Processed {} review ratings'.format(idx+1))




    # Step 4: Aggregate data for each reviewer
    print('Aggregating scores')
    final_result_map = []
    for reviewer, records in file_reviewers_ds.items():
        score = 0

        count_completed_emergency_reviews = len(list(filter(lambda x:(records[x]['emergency'] and records[x]['completed_at']), records)))

        completed_reviews = list(filter(lambda x:records[x]['completed_at'], records))

        for paper_number in completed_reviews:
            rating = map_ratings.get(reviewer, {}).get(paper_number)
            if rating:
                # Add rating received from AC
                score += rating
            else:
                # Add 1 in case rating is not available
                score += 1

        # Add 1 for each emergency review done by this reviewer
        score += count_completed_emergency_reviews

        # Subtract 1 for each missing review (assigned reviews MINUS completed reviews)
        score -= (len(records) - len(completed_reviews))

        reviewer_record = {
            'tilde': reviewer,
            'reviews_assigned': len(records),
            'reviews_completed': len(completed_reviews),
            'total_score': score
        }
        final_result_map.append(reviewer_record)




    # Step 5: Output CSV with (reviewer name, reviewer email, number of reviews, total score)
    # Total score = SUM(all the scores received from ACs) + 1 for each review that was not rated (because the AC did not rate it or because the paper was withdrawn) - 1 for each missing review + 1 for each delivered emergency review.
    print('Writing to {}'.format(outfile))
    with open(outfile, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Reviewer ID', 'Reviewer Name', 'Email', 'Assigned Reviews', 'Completed Reviews', 'Total Score'])
        for result in tqdm(final_result_map):
            reviewer_details = get_reviewer_details(tilde=result['tilde'])
            csv_writer.writerow([result['tilde'], reviewer_details['name'], reviewer_details['email'], result['reviews_assigned'], result['reviews_completed'], result['total_score']])
