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

    emergency_load_invitation = client.get_invitation('thecvf.com/ECCV/2020/Conference/Reviewers/-/Custom_Load')
    emergency_load_invitation.id = 'thecvf.com/ECCV/2020/Conference/Reviewers/-/Emergency_Load'
    emergency_load_invitation.reply['content']['head']['query'] = {'id' : 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers'}
    emergency_load_invitation.reply['content']['tail']['query'] = {'id' : 'thecvf.com/ECCV/2020/Conference/Emergency_Reviewers'}
    emergency_load_invitation = client.post_invitation(emergency_load_invitation)
    
    
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

    active = 0
    tilde_profiles=client.search_profiles(ids=tildes)

    inactives = []

    for profile in tilde_profiles:
        profile_map[profile.id] = profile
        if profile.active and profile.password:
            active+=1
        else:
            inactives.append(profile.id)

    print ('Number of active profiles:', active)
    print ('Number of inactive profiles:', len(inactives))

    emergency_load_edges = []

    for reviewer in tqdm(reviewer_group.members):
        review_capacity = 0
        
        profile = profile_map.get(reviewer, None)
        if not profile:
            print ('Issue with reviewer:', reviewer)
            # profile = openreview.tools.get_profile(client, reviewer)

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
                    invitation = 'thecvf.com/ECCV/2020/Conference/Reviewers/-/Emergency_Load',
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

    print('posting updated emergency grp')
    x = client.post_group(emergency_reviewer_group)
    print('posted updated emergency grp')
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

    emergency_review_demands = []
    for paper_num, reviews in map_paper_to_reviews.items():
        if len(reviews) < 3:
            emergency_review_demands.append(openreview.Edge(
                head = map_submissions[paper_num].id,
                tail = map_submissions[paper_num].id,
                invitation = 'thecvf.com/ECCV/2020/Conference/Reviewers/-/Emergency_Demand',
                readers = [
                    'thecvf.com/ECCV/2020/Conference',
                    'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                    ],
                writers = ['thecvf.com/ECCV/2020/Conference'],
                signatures = ['thecvf.com/ECCV/2020/Conference'],
                weight = 3 - len(reviews)
            ))
    
    # Need to add a conflict edge for the reviewers of the existing reviews for a paper

    emergency_demand_invitation = client.get_invitation('thecvf.com/ECCV/2020/Conference/Reviewers/-/Custom_Load')
    emergency_demand_invitation.id = 'thecvf.com/ECCV/2020/Conference/Reviewers/-/Emergency_Demand'
    emergency_demand_invitation.reply['content']['head'] = {
        'query' : {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
        'type': 'Note'
    }

    emergency_demand_invitation.reply['content']['tail'] = {
        'query' : {'invitation': 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission'},
        'type': 'Note'
    }

    emergency_demand_invitation = client.post_invitation(emergency_demand_invitation)

    print ('Posting {0} edges'.format(len(emergency_review_demands)))
    posted_edges = openreview.tools.post_bulk_edges(client, emergency_review_demands)
    print ('Posted {0} edges'.format(len(emergency_review_demands)))