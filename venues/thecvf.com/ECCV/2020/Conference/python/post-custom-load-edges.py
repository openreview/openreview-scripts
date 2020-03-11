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
    reviewer_group_name = 'Reviewers'

    reviewer_group = client.get_group('thecvf.com/ECCV/2020/Conference/' + reviewer_group_name)

    confirmations = {}
    confirmation_notes = openreview.tools.iterget_notes(
                client,
                invitation='thecvf.com/ECCV/2020/Conference/{grp}/-/Profile_Confirmation'.format(grp=reviewer_group_name))
    for note in tqdm(confirmation_notes):
        # Check if this user has posted multiple confirmations
        if note.tauthor in confirmations:
            # Check if note is a newer confirmation
            if note.tcdate > confirmations[note.tauthor].tcdate:
                confirmations[note.tauthor] = note
        else:
            confirmations[note.tauthor] = note

    print ('Confirmations received: ', len(confirmations))

    custom_loads = {}
    custom_load_notes = openreview.tools.iterget_notes(
        client,
        invitation='thecvf.com/ECCV/2020/Conference/-/Reduced_Load')

    for note in tqdm(custom_load_notes):
        # Check if this user has posted multiple reduced load notes
        if note.content['user'] in custom_loads:
            # Check if note is a newer confirmation
            if note.tcdate > custom_loads[note.content['user']].tcdate:
                custom_loads[note.content['user']] = note
        else:
            custom_loads[note.tauthor] = note

    print ('Reduced loads received: ', len(custom_loads))

    profile_map = {}

    emails = []
    tildes = []
    for ac in reviewer_group.members:
        if ac.startswith('~'):
            tildes.append(ac)
        else:
            emails.append(ac)

    active = 0
    tilde_profiles=client.search_profiles(ids=tildes)
    email_profiles=client.search_profiles(emails=emails)

    inactives = []

    for profile in tilde_profiles:
        profile_map[profile.id] = profile
        if profile.active and profile.password:
            active+=1
        else:
            inactives.append(profile.id)

    for member in email_profiles:
        profile_map[member] = email_profiles[member]
        if profile_map[member].active and profile_map[member].password:
            active+=1
        else:
            inactives.append(member)


    print ('Number of active profiles:', active)
    print ('Number of inactive profiles:', len(inactives))

    miss = 0
    total_review_capacity = 0

    custom_load_edges = []

    for reviewer in tqdm(reviewer_group.members):
        review_capacity = 0
        
        profile = profile_map.get(reviewer, None)
        if not profile:
            miss += 1
            profile = openreview.tools.get_profile(client, reviewer)

        confirmation = None
        custom_load = None
        if profile:
            ids = profile.content['emailsConfirmed'] + [ n['username'] for n in profile.content['names'] if 'username' in n]
            for i in ids:
                if not confirmation and i in confirmations:
                    confirmation = confirmations[i]
                if not custom_load and i in custom_loads:
                    custom_load = custom_loads[i]

        output = []
        output.append(reviewer)
        
        if custom_load:
            review_capacity = int(custom_load.content['reviewer_load']) - (int(confirmation.content.get('emergency_review_count', '0')) if confirmation else 0)
        else:
            review_capacity = 7 - (int(confirmation.content.get('emergency_review_count', '0')) if confirmation else 0)

        if review_capacity != 7:
            edge = openreview.Edge(
                head='thecvf.com/ECCV/2020/Conference/' + reviewer_group_name,
                tail=profile.id,
                invitation='thecvf.com/ECCV/2020/Conference/{}/-/Custom_Load'.format(reviewer_group_name),
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

    print ('Users with no profiles: ', miss)