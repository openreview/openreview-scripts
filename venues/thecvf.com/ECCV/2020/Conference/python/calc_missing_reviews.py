import openreview
import csv
from tqdm import tqdm
import argparse

def get_pref_name(profile):
    names = profile.content.get('names', [])
    for name in names:
        if name.get('preferred', False):
            return name
    return names[0] if names else {}

def get_pref_email(profile):
    prefEmail = profile.content.get('preferredEmail')
    if not prefEmail:
        prefEmail = profile.content.get('emailsConfirmed')[0]
    return prefEmail

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    map_number_to_submission = {int(note.number): note for note in openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    print('{} submission found'.format(len(map_number_to_submission)))

    official_reviews = list(openreview.tools.iterget_notes(
        client,
        invitation='^thecvf.com/ECCV/2020/Conference/Paper[0-9]*/-/Official_Review$'))
    print('{} official reviews found'.format(len(official_reviews)))

    all_assignments = list(openreview.tools.iterget_groups(
        client, 
        regex='^thecvf.com/ECCV/2020/Conference/Paper[0-9]*/AnonReviewer[0-9]*$'))
    print('{} reviewer assignments found'.format(len(all_assignments)))
    
    map_normal_assignments = {}
    map_ac_assignments = {}
    map_paper_to_assignments = {}
    map_group_id_to_anon_group = {}
    map_user_to_anon_groups = {}
    for group in tqdm(all_assignments):
        paper_number = int(group.id.split('Paper')[1].split('/')[0])
        map_group_id_to_anon_group[group.id] = group

        if paper_number not in map_paper_to_assignments:
            map_paper_to_assignments[paper_number] = {}
        map_paper_to_assignments[paper_number][group.id] = group

        if group.signatures[0] not in map_user_to_anon_groups:
            map_user_to_anon_groups[group.signatures[0]] = []
        map_user_to_anon_groups[group.signatures[0]].append(group.id)

        if 'Area_Chairs' in group.signatures[0] or 'Program_Chairs' in group.signatures[0]:
            if paper_number not in map_ac_assignments:
                map_ac_assignments[paper_number] = []
            map_ac_assignments[paper_number].append(group.id)
        else:
            if paper_number not in map_normal_assignments:
                map_normal_assignments[paper_number] = []
            map_normal_assignments[paper_number].append(group.id)

    print('{} papers have normal assignments'.format(len(map_normal_assignments)))
    print('{} papers have pc/ ac assignments'.format(len(map_ac_assignments)))

    map_group_to_review = {}
    map_paper_to_reviews = {}
    map_paper_to_completed_reviewers = {}
    # Freeze reviews
    print('Freezing existing reviews')
    for review in tqdm(official_reviews):
        review.writers = []
        # client.post_note(review)
        paper_number = int(review.invitation.split('Paper')[1].split('/')[0])
        if paper_number in map_number_to_submission:
            if review.signatures[0] in map_group_to_review:
                print('Multiple reviews by ', review.signatures[0])
            map_group_to_review[review.signatures[0]] = review
            
            if paper_number not in map_paper_to_reviews:
                map_paper_to_reviews[paper_number] = []
            map_paper_to_reviews[paper_number].append(review)

            if paper_number not in map_paper_to_completed_reviewers:
                map_paper_to_completed_reviewers[paper_number] = []
            map_paper_to_completed_reviewers[paper_number].append(review.signatures[0])

    print('{} reviews are now frozen'.format(len(official_reviews)))

    ##########
    # TODO: Stats for ECCV PCs
    # Write a CSV recording each reviewers assigned by matcher results, how many reviews were missed by them
    ##########
    out_file = '/Users/muniyal/Desktop/eccv20_reviewer_stats_21_may.csv'

    map_user_to_reviews = {}
    for paper, groups in map_normal_assignments.items():
        for group_id in groups:
            reviewer_group = map_group_id_to_anon_group[group_id]
            if reviewer_group.members:
                reviewer = reviewer_group.members[0]
                review = map_group_to_review.get(group_id, None)
                if reviewer not in map_user_to_reviews:
                    map_user_to_reviews[reviewer] = []
                map_user_to_reviews[reviewer].append(review)

    map_user_to_profiles = {}
    profiles = client.search_profiles(ids=list(map_user_to_reviews.keys()))
    for profile in profiles:
        map_user_to_profiles[profile.id] = profile

    print('Writing stats for ECCV PCs to {}'.format(out_file))
    with open(out_file, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['OpenReview Id', 'Name', 'Email', 'Reviews Assigned', 'Reviews Missing'])
        for user, reviews in tqdm(sorted(map_user_to_reviews.items(), key=lambda x:x)):
            assigned_reviews = len(reviews)
            available_reviews = len([review for review in reviews if review])
            profile = map_user_to_profiles.get(user)
            if not profile:
                if user.startswith('~'):
                    profile = client.search_profiles(ids=[user])
                    if profile:
                        profile = profile[0]
                else:
                    profile = client.search_profiles(emails=[user])
                    if profile:
                        profile = profile[user]
            email = get_pref_email(profile)
            name_obj = get_pref_name(profile)
            full_name = ''
            if name_obj:
                full_name = ' '.join([name for name in [name_obj.get('first'), name_obj.get('last'), name_obj.get('middle')] if name])
            csv_writer.writerow([user, full_name, email, assigned_reviews, assigned_reviews - available_reviews])

    ##########
    # TODO: Stats for OpenReview's records
    # Write a CSV recording each paper's reviewers, if they were added normally or by AC/PC, if they have completed their review
    ##########
    internal_out_file = '/Users/muniyal/Desktop/eccv20_internal_paper_reviewer_stats_21_may.csv'

    with open(internal_out_file, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([['Paper', 'Reviewer', 'Review Completed', 'Matcher Assignment']])
        # for paper in 

    for number, note in map_number_to_submission.items():
        reviews = map_paper_to_reviews[number]
        reviewers = map_paper_to_assignments[number]
        if len(reviews) >= 3:
            # find late reviewers of this paper
            for reviewer in reviewers:
                # print('Checking {}'.format(reviewer))
                if reviewer not in map_paper_to_completed_reviewers[number]:
                    user = map_group_id_to_anon_group[reviewer].members[0]
                    # print('Removing {}'.format(user))
                    openreview.tools.assign(
                        client, 
                        paper_number=number, 
                        conference='thecvf.com/ECCV/2020/Conference',
                        reviewer_to_remove=user)
                    # print('Paper {} Removed {}'.format(number, user))
