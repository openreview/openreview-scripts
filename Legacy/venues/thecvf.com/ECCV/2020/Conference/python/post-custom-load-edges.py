import openreview
import argparse
from tqdm import tqdm

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    
    reviewer_group = client.get_group('thecvf.com/ECCV/2020/Conference/Reviewers')
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

    reduced_loads = {}
    reduced_load_notes = openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/-/Reduced_Load')

    for note in tqdm(reduced_load_notes):
        # Check if this user has posted multiple reduced load notes
        if note.content['user'] in reduced_loads:
            # Check if note is a newer confirmation
            if note.tcdate > reduced_loads[note.content['user']].tcdate:
                reduced_loads[note.content['user']] = note
        else:
            reduced_loads[note.content['user']] = note

    print ('Reduced loads received: ', len(reduced_loads))

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

    users_without_profiles = []
    custom_load_edges = []

    for reviewer in tqdm(reviewer_group.members):
        review_capacity = 0
        
        profile = profile_map.get(reviewer, None)
        if not profile:
            users_without_profiles.append(reviewer)
            continue
        
        confirmation = None
        custom_load = None
        
        ids = profile.content['emailsConfirmed'] + [ n['username'] for n in profile.content['names'] if 'username' in n]
        for i in ids:
            if not confirmation and (i in confirmations):
                confirmation = confirmations[i]
            if not custom_load and (i in reduced_loads):
                custom_load = reduced_loads[i]
        
        emergency_review_count = int(confirmation.content.get('emergency_review_count', '0')) if confirmation else 0

        if custom_load:
            review_capacity = int(custom_load.content['reviewer_load']) - emergency_review_count
        else:
            review_capacity = 7 - emergency_review_count

        if review_capacity != 7:
            edge = openreview.Edge(
                head='thecvf.com/ECCV/2020/Conference/Reviewers',
                tail=profile.id,
                invitation='thecvf.com/ECCV/2020/Conference/Reviewers/-/Custom_Load',
                readers=[
                    'thecvf.com/ECCV/2020/Conference',
                    'thecvf.com/ECCV/2020/Conference/Area_Chairs',
                    profile.id],
                writers=['thecvf.com/ECCV/2020/Conference'],
                signatures=['thecvf.com/ECCV/2020/Conference'],
                weight=review_capacity
            )
            custom_load_edges.append(edge)

    print ('Posting {0} edges'.format(len(custom_load_edges)))
    posted_edges = openreview.tools.post_bulk_edges(client, custom_load_edges)
    print ('Posted {0} edges'.format(len(posted_edges)))

    print ('Users with no profiles:', users_without_profiles)