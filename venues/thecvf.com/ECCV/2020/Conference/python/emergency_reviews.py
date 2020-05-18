import openreview
import csv
from tqdm import tqdm
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    reviewer_group = client.get_group('thecvf.com/ECCV/2020/Conference/Reviewers')
    emergency_reviewer_group = client.get_group('thecvf.com/ECCV/2020/Conference/Emergency_Reviewers')
    print ('Found emergency group {} with {} members\n'.format(emergency_reviewer_group.id, len(emergency_reviewer_group.members)))

    emergency_load_invitation = openreview.Invitation(
        id='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Custom_Max_Papers',
        signatures=['thecvf.com/ECCV/2020/Conference'],
        readers=[
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Area_Chairs'],
        writers=['thecvf.com/ECCV/2020/Conference'],
        invitees=['thecvf.com/ECCV/2020/Conference'],
        reply = {
            'readers': {'values-copied': [
                'thecvf.com/ECCV/2020/Conference',
                'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                '{tail}']},
            'nonreaders': {'values-regex': 'thecvf.com/ECCV/2020/Conference/Paper.*/Authors'},
            'writers': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'signatures': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'content': {
                'head': {
                    'query' : {'id': 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers'},
                    'type': 'Group'
                },
                'tail': {
                    'query' : {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
                    'type': 'Note'
                },
                'weight': {
                    'value-regex': '[-+]?[0-9]*\\.?[0-9]*'
                },
                'label': {
                    'value-regex': '.*'
                }
            }
        }
    )
    # emergency_load_invitation = client.post_invitation(emergency_load_invitation)
    # print('Posted invitation:{}\n'.format(emergency_load_invitation.id))

    # DO SEPARATELY
    # print('Deleting edges for invitation {}\n'.format(emergency_load_invitation.id))
    # client.delete_edges(invitation=emergency_load_invitation.id)

    confirmations = {}
    confirmation_notes = openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/Reviewers/-/Profile_Confirmation')

    for note in tqdm(confirmation_notes):
        # Check if this user has posted multiple confirmations
        if note.tauthor in confirmations:
            # Check if note is a newer confirmation
            if note.tcdate > confirmations[note.tauthor].tcdate:
                confirmations[note.tauthor] = note
        else:
            confirmations[note.tauthor] = note

    print ('Confirmations received: {}\n'.format(len(confirmations)))

    profile_map = {}
    tildes = []

    for member in emergency_reviewer_group.members:
        if member.startswith('~'):
            tildes.append(member)

    tilde_profiles=client.search_profiles(ids=tildes)

    for profile in tilde_profiles:
        profile_map[profile.id] = profile

    emergency_load_edges = []
    total_review_capacity = 0

    for reviewer in tqdm(emergency_reviewer_group.members):
        review_capacity = 0

        profile = profile_map.get(reviewer, None)
        if not profile:
            print ('Issue with reviewer:', reviewer)

        confirmation = None
        if profile:
            ids = profile.content['emailsConfirmed'] + [ n['username'] for n in profile.content['names'] if 'username' in n]
            for i in ids:
                if i in confirmations:
                    confirmation=confirmations[i]

        if confirmation:
            review_capacity = int(confirmation.content.get('emergency_review_count', '0'))
            if review_capacity:
                total_review_capacity += review_capacity
                edge = openreview.Edge(
                    head = 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers',
                    tail = profile.id,
                    invitation = 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Custom_Max_Papers',
                    readers = [
                        'thecvf.com/ECCV/2020/Conference',
                        'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                        profile.id],
                    writers = ['thecvf.com/ECCV/2020/Conference'],
                    signatures = ['thecvf.com/ECCV/2020/Conference'],
                    weight = review_capacity
                )
                emergency_load_edges.append(edge)

    print('Posting {0} edges'.format(len(emergency_load_edges)))
    posted_edges = openreview.tools.post_bulk_edges(client, emergency_load_edges)
    print('Posted {0} edges\n'.format(len(posted_edges)))

    map_submissions = {note.number: note for note in openreview.tools.iterget_notes(client, invitation = 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}

    all_reviews = list(openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/-/Official_Review$'))
    print('Found {} official reviews\n'.format(len(all_reviews)))
    
    map_paper_to_reviews = {}
    for review in all_reviews:
        paper_num = int(review.invitation.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions:
            if paper_num not in map_paper_to_reviews:
                map_paper_to_reviews[paper_num] = []
            map_paper_to_reviews[paper_num].append(review)

    # Add entries for papers without any reviews
    for paper_num in map_submissions:
        if paper_num not in map_paper_to_reviews:
            map_paper_to_reviews[paper_num] = []

    emergency_demand_invitation = openreview.Invitation(
        id='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Custom_User_Demands',
        signatures=['thecvf.com/ECCV/2020/Conference'],
        readers=[
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Area_Chairs'],
        writers=['thecvf.com/ECCV/2020/Conference'],
        invitees=['thecvf.com/ECCV/2020/Conference'],
        reply = {
            'readers': {'values-copied': [
                'thecvf.com/ECCV/2020/Conference',
                'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                '{tail}']},
            'nonreaders': {'values-regex': 'thecvf.com/ECCV/2020/Conference/Paper.*/Authors'},
            'writers': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'signatures': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'content': {
                'head': {
                    'query' : {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
                    'type': 'Note'
                },
                'tail': {
                    'query' : {'id': 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers'},
                    'type': 'Group'
                },
                'weight': {
                    'value-regex': '[-+]?[0-9]*\\.?[0-9]*'
                },
                'label': {
                    'value-regex': '.*'
                }
            }
        }
    )
    emergency_demand_invitation = client.post_invitation(emergency_demand_invitation)
    print('Posted invitation {}\n'.format(emergency_demand_invitation.id))

    # DO SEPARATELY
    # print('Deleting old edges for invitation {}\n'.format(emergency_demand_invitation.id))
    # client.delete_edges(invitation=emergency_demand_invitation.id)

    ac_groups = openreview.tools.iterget_groups(client, regex='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/Area_Chairs$')
    map_paper_to_ac = {}
    for grp in ac_groups:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions and grp.members:
            map_paper_to_ac[paper_num] = grp.members[0]

    map_paper_to_reviewers = {}
    reviewer_groups = list(openreview.tools.iterget_groups(client, regex='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/AnonReviewer[0-9]*$'))
    for grp in reviewer_groups:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions and grp.members:
            if paper_num not in map_paper_to_reviewers:
                map_paper_to_reviewers[paper_num] = []
            map_paper_to_reviewers[paper_num].append(grp.members[0])
    
    ac_recommendation_edges = list(openreview.tools.iterget_edges(
        client, 
        invitation='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Recommendation'))

    papers_with_recommendations = set()
    for edge in ac_recommendation_edges:
        papers_with_recommendations.add(edge.head)

    print('Found {} papers with AC recommendations\n'.format(len(papers_with_recommendations)))

    emergency_review_demands = []

    recommendation_based_review_demand = 0
    filtered_demand = 0
    absolute_demand = 0
    ac_with_missing_recs = set()
    paper_left_due_to_filtering = 0
    reviewers_left_due_to_filtering = 0

    for paper_num, reviews in map_paper_to_reviews.items():
        paper_note = map_submissions[paper_num]
        ac = map_paper_to_ac[paper_num]
        missing_reviews = 3-len(reviews)
        if missing_reviews > 0:
            if paper_note.id in papers_with_recommendations:
                recommendation_based_review_demand += missing_reviews
            else:
                ac_with_missing_recs.add(ac)

            if (len(map_paper_to_reviewers[paper_num]) <= 3 and missing_reviews > 0) or (len(map_paper_to_reviewers[paper_num]) > 3 and missing_reviews > 1):
                # Don't use papers with 1 missing review AND more than 3 assigned reviewers
                emergency_review_demands.append(openreview.Edge(
                    head=paper_note.id,
                    tail='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers',
                    invitation='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Custom_User_Demands',
                    readers=[
                        'thecvf.com/ECCV/2020/Conference',
                        'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                        ],
                    writers=['thecvf.com/ECCV/2020/Conference'],
                    signatures=['thecvf.com/ECCV/2020/Conference'],
                    weight=missing_reviews
                ))
                filtered_demand += missing_reviews
            else:
                paper_left_due_to_filtering += 1
                reviewers_left_due_to_filtering += missing_reviews

            absolute_demand += missing_reviews

    print('Custom_User_Demands: Posting {0} edges'.format(len(emergency_review_demands)))
    posted_edges = openreview.tools.post_bulk_edges(client, emergency_review_demands)
    print('Custom_User_Demands: Posted {0} edges\n'.format(len(posted_edges)))

    emergency_aggregate_invitation = openreview.Invitation(
        id='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Aggregate_Score',
        signatures=['thecvf.com/ECCV/2020/Conference'],
        readers=[
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Area_Chairs'],
        writers=['thecvf.com/ECCV/2020/Conference'],
        invitees=['thecvf.com/ECCV/2020/Conference'],
        reply = {
            'readers': {'values-copied': [
                'thecvf.com/ECCV/2020/Conference',
                'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                '{tail}']},
            'nonreaders': {'values-regex': 'thecvf.com/ECCV/2020/Conference/Paper.*/Authors'},
            'writers': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'signatures': {'values': ['thecvf.com/ECCV/2020/Conference']},
            'content': {
                'head': {
                    'query' : {'id': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
                    'type': 'Note'
                },
                'tail': {
                    'query' : {'invitation': 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers'},
                    'type': 'Profile'
                },
                'weight': {
                    'value-regex': '[-+]?[0-9]*\\.?[0-9]*'
                },
                'label': {
                    'value-regex': '.*'
                }
            }
        }
    )
    emergency_aggregate_invitation = client.post_invitation(emergency_aggregate_invitation)
    print('Posted invitation {}\n'.format(emergency_aggregate_invitation.id))

    # DO SEPARATELY
    # print('\nDeleting old edges for invitation:"thecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict" and label: "Already Assigned"\n')
    # client.delete_edges(invitation='thecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict', label='Already Assigned')

    conflicts = []

    for grp in reviewer_groups:
        paper_num = int(grp.id.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions and grp.members:
            conflicts.append(openreview.Edge(
                head=map_submissions[paper_num].id,
                tail=grp.members[0],
                invitation='thecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict',
                readers=[
                    'thecvf.com/ECCV/2020/Conference',
                    'thecvf.com/ECCV/2020/Conference/Area_Chairs'
                ],
                writers=['thecvf.com/ECCV/2020/Conference'],
                signatures=['thecvf.com/ECCV/2020/Conference'],
                weight=-1,
                label='Already Assigned'
            ))

    print('\nthecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict: Posting {0} edges'.format(len(conflicts)))
    posted_edges = openreview.tools.post_bulk_edges(client, conflicts)
    print('\nthecvf.com/ECCV/2020/Conference/Reviewers/-/Conflict: Posted  {0} edges'.format(len(posted_edges)))

    print('\nChecking if emergency reviewer matching is set up already')
    emergency_assignment_invi = openreview.tools.get_invitation(client, 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Assignment_Configuration')
    
    if emergency_assignment_invi:
        print('\nEmergency Reviewer matching has been setup already')
    else:
        print('Emergency Reviewer matching not set up. Setting it up now.')
        # conference = openreview.helpers.get_conference(
        #     client, 
        #     request_form_id='Skx6tVahYB')
        
        # # Setting conference reviewers group to "Emergency_Reviewers"
        # conference.set_reviewers_name('Emergency_Reviewers')
        # conference.setup_matching()
        # print('Emergency Reviewer match setup done.')

    print('\nFiltered Emergency Review Demand: {}'.format(filtered_demand))
    print ('\nAbsolute Emergency Review Demand: {}'.format(absolute_demand))
    print('\nTotal Emergency Review Supply: {}\n'.format(total_review_capacity))
    print('\nACs with missing recommendations: {}\n'.format(len(ac_with_missing_recs)))

    print('\nPapers left out due to filtering: {}\n'.format(paper_left_due_to_filtering))
    print('\nReviews left out due to filtering: {}\n'.format(reviewers_left_due_to_filtering))
