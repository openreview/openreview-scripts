import openreview
import csv
import time
from tqdm import tqdm
import argparse
from collections import defaultdict

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help='base url')
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    # Step 0: Create maps for blind and withdrawn papers
    blind_notes = {note.id: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}

    withdrawn_notes = {note.id: note for note in openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/-/Withdrawn_Submission')}


    # Step 1: Gather all reviewers

    # Step 1.1: Reviewers from reviewer group
    file_reviewers_ds = defaultdict(dict)
    with open('eccv20_internal_paper_reviewer_stats_21_may.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
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
            file_reviewers_ds[reviewer][paper_number] = record

    # Step 1.2: Gather new reviewers since this file was created
    reviewer_group = client.get_group('thecvf.com/ECCV/2020/Conference/Reviewers')
    reviewers = set(reviewer_group.members)

    map_current_reviewer_groups = {grp.id: grp for grp in openreview.tools.iterget_groups(
        client, 
        regex='thecvf.com/ECCV/2020/Conference/Paper[0-9]+/AnonReviewer[0-9]+$')}

    for grp_id, group in map_current_reviewer_groups.items():
        if group.members:
            paper_number = grp_id.split('Paper')[1].split('/')[0]
            reviewer = group.members[0]
            if reviewer not in file_reviewers_ds or paper_number not in file_reviewers_ds.get(reviewer, {}):
                emergency = False if group.signatures[0] == 'thecvf.com/ECCV/2020/Conference' else True
                record = {
                    'completed_at': None,
                    'assigned_at': group.cdate, # Using the AnonReviewerX group's cdate as assigned_date
                    'assigned_by': group.signatures[0],
                    'emergency': emergency
                }
                file_reviewers_ds[reviewer][paper_number] = record

    # Step 2: Find ALL reviews (regardless of whether the paper is withdrawn or not)
    reviews = openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]+/-/Official_Reviews$')
    for review in reviews:
        paper_number = review.invitation.split('Paper')[1].split('/')[0]
        reviewer = review
        record = file_reviewers_ds.get(reviewer).get(paper_number)
        if not record:
            print('Not found paper {} - reviewer {}'.format(paper_number, reviewer))
        if not record['completed_at']:
            record['completed_at'] = review.tcdate


    # Step 3: Get emergency assignment edges to identify emergency assignments
    emergency_edges = openreview.tools.iterget_edges(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Paper_Assignment',
        label='emergency-assignment-4')

    for idx, edge in enumerate(emergency_edges):
        paper = blind_notes.get(edge.head) or withdrawn_notes.get(edge.head)
        paper_number = str(paper.number)
        reviewer = edge.tail
        # find this record and set emergency=True
        record = file_reviewers_ds[reviewer][paper_number]
        record['emergency'] = True
    print('Updated {} edges'.format(idx))

    # Step 4: Get all review ratings and organize it
    map_ratings = defaultdict(dict)
    review_ratings = openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/AnonReviewer[0-9]*/-/Review_Rating'
    )
    for rating in review_ratings:
        paper_number = rating.invitation.split('Paper')[1].split('/')[0]
        anon_rev_group = rating.invitation.split('/-/'[0])
        reviewer_group = map_current_reviewer_groups.get(anon_rev_group)
        if not reviewer_group:
            print('{} not found in current reviewer groups'.format(anon_rev_group))
            break
        reviewer = reviewer_group.members[0]
        map_ratings[reviewer][paper_number] = rating.content['rating']

    # Step 4: Aggregate data for each reviewer
    final_result_map = defaultdict()
    for reviewer, records in file_reviewers_ds.items():
        count_completed_reviews = len(list(filter(lambda rec:rec['completed_at'], records.values())))
        emergency_reviews = len(list(filter(lambda rec:rec['emergency'], records.values())))


    # Step 5: Output CSV with (reviewer name, reviewer email, number of reviews, total score)
    # Total score = SUM(all the scores received from ACs) + 1 for each review that was not rated (because the AC did not rate it or because the paper was withdrawn) - 1 for each missing review + 1 for each delivered emergency review.

    with open('final_reviewer_ratings.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Reviewer Name', 'Email', 'Number of Reviews','Total Score'])
        for result in final_result_map:
            reviewer_details = get_reviewer_details(tilde=result[0])
            csv_writer.writerow(reviewer_details['name'], reviewer_details['email'], result[1], result[2])


def get_reviewer_details(tilde):
    profile = client.search_profiles(ids=[tilde])
    pref_name = None
    for name in profile.content['names']:
        if name.get('preferred'):
            pref_name = [name.get('first')]
            if name.get('middle'):
                pref_name.append(name.get('middle'))
            pref_name.append(name.get('last'))
    if not pref_name:
        name = profile.content['names'][0]
        pref_name = name.get('first')
        if name.get('middle'):
            pref_name.append(name.get('middle'))
        pref_name.append(name.get('last'))

    pref_email = profile.content.get('preferredEmail')
    if not pref_email:
        pref_email = profile.content['emailsConfirmed'][0]
    
    return {'name': pref_name, 'email': pref_email}

