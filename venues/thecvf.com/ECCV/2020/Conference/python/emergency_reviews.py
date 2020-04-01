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
    emergency_reviewer_group = client.post_group(openreview.Group(
        id = 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers',
        signatures = ['thecvf.com/ECCV/2020/Conference'],
        signatories = ['thecvf.com/ECCV/2020/Conference/Emergency_Reviewers'],
        readers = [
            'thecvf.com/ECCV/2020/Conference',
            'thecvf.com/ECCV/2020/Conference/Area_Chairs',
            'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers'],
        writers = ['thecvf.com/ECCV/2020/Conference',
        'thecvf.com/ECCV/2020/Conference/Area_Chairs'],
        members = []
    ))
    print ('Posted group:', emergency_reviewer_group.id)

    emergency_load_invitation = client.post_invitation(openreview.Invitation(
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
    ))
    print ('Posted invitation:', emergency_load_invitation.id)
    
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

    print ('Confirmations received: ', len(confirmations))

    profile_map = {}
    tildes = []

    for member in reviewer_group.members:
        if member.startswith('~'):
            tildes.append(member)

    tilde_profiles=client.search_profiles(ids=tildes)

    for profile in tilde_profiles:
        profile_map[profile.id] = profile

    emergency_load_edges = []

    for reviewer in tqdm(reviewer_group.members):
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
                edge = openreview.Edge(
                    head = 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers',
                    tail = profile.id,
                    invitation = 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Custom_Max_Papers',
                    readers = [
                        'thecvf.com/ECCV/2020/Conference',
                        'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                        profile.id
                        ],
                    writers = ['thecvf.com/ECCV/2020/Conference'],
                    signatures = ['thecvf.com/ECCV/2020/Conference'],
                    weight = review_capacity
                )
                emergency_load_edges.append(edge)
                emergency_reviewer_group.members.append(profile.id)

    x = client.post_group(emergency_reviewer_group)
    print('posted updated emergency reviewers group')
    print ('Posting {0} edges'.format(len(emergency_load_edges)))
    posted_edges = openreview.tools.post_bulk_edges(client, emergency_load_edges)
    print ('Posted {0} edges'.format(len(posted_edges)))

    map_submissions = {note.number: note for note in openreview.tools.iterget_notes(client, invitation = 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    all_reviews = openreview.tools.iterget_notes(client, invitation='thecvf.com/ECCV/2020/Conference/Paper[0-9]*/-/Official_Review')
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

    emergency_demand_invitation = client.post_invitation(openreview.Invitation(
        id='thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Custom_Max_Users',
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
    ))
    print ('Posted invitation:', emergency_demand_invitation.id)

    emergency_review_demands = []
    # TODO: Need to add a conflict edge for the reviewers of the existing reviews for a paper ?
    for paper_num, reviews in map_paper_to_reviews.items():
        if len(reviews) < 3:
            emergency_review_demands.append(openreview.Edge(
                head = map_submissions[paper_num].id,
                tail = 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers',
                invitation = 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers/-/Custom_Max_Users',
                readers = [
                    'thecvf.com/ECCV/2020/Conference',
                    'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                    ],
                writers = ['thecvf.com/ECCV/2020/Conference'],
                signatures = ['thecvf.com/ECCV/2020/Conference'],
                weight = 3 - len(reviews)
            ))

    print ('Posting {0} edges'.format(len(emergency_review_demands)))
    posted_edges = openreview.tools.post_bulk_edges(client, emergency_review_demands)
    print ('Posted {0} edges'.format(len(emergency_review_demands)))