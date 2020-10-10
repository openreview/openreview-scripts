import openreview
import argparse
from tqdm import tqdm
import csv

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('file',help="a csv file with light review load requests in the form first_name, middle_name, last_name, email, reduced_load")
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    reviewer_group = client.get_group('ICLR.cc/2021/Conference/Reviewers')
    confirmations = {}
    confirmation_notes = openreview.tools.iterget_notes(
                client,
                invitation='ICLR.cc/2021/Conference/Reviewers/-/Registration')
    max3_accepted_users = { n.content['user'] for n in openreview.tools.iterget_notes(
                client,
                invitation='ICLR.cc/2021/Conference/-/Recruit_Reviewers',
                content={ 'response': Yes },
                mintcdate=1598590800000)} # August 28th

    for note in tqdm(confirmation_notes):
        # Check if this user has posted multiple confirmations
        if note.tauthor in confirmations:
            # Check if note is a newer confirmation
            if note.tcdate > confirmations[note.tauthor].tcdate:
                confirmations[note.tauthor] = note
        else:
            confirmations[note.tauthor] = note

    print ('Registrations received: ', len(confirmations))

    reduced_loads = {}
    with open(args.file) as f:
        csv_reader = csv.reader(f)
        next(csv_reader, None)
        for row in csv_reader:
            reduced_loads[row[3]] = row[4]

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
        max3_accepted = None

        ids = profile.content['emailsConfirmed'] + [ n['username'] for n in profile.content['names'] if 'username' in n]
        for i in ids:
            if not confirmation and (i in confirmations):
                confirmation = confirmations[i]
            if not custom_load and (i in reduced_loads):
                custom_load = reduced_loads[i]
            if not max3_accepted and (i in max3_accepted_users):
                max3_accepted = max3_accepted_users[i]

        emergency_review_count = int(confirmation.content.get('emergency_review_count')) if confirmation else 0

        if custom_load:
            review_capacity = int(custom_load) - emergency_review_count
        else if max3_accepted:
            review_capacity = 3 - emergency_review_count
        else:
            review_capacity = 5 - emergency_review_count

        if review_capacity < 0:
            print(reviewer)
            continue

        if review_capacity != 4:
            edge = openreview.Edge(
                head='ICLR.cc/2021/Conference/Reviewers',
                tail=profile.id,
                invitation='ICLR.cc/2021/Conference/Reviewers/-/Custom_Max_Papers',
                readers=[
                    'ICLR.cc/2021/Conference',
                    'ICLR.cc/2021/Conference/Area_Chairs',
                    profile.id],
                writers=['ICLR.cc/2021/Conference'],
                signatures=['ICLR.cc/2021/Conference'],
                weight=review_capacity
            )
            custom_load_edges.append(edge)

    print ('Posting {0} edges'.format(len(custom_load_edges)))
    posted_edges = openreview.tools.post_bulk_edges(client, custom_load_edges)
    print ('Posted {0} edges'.format(len(posted_edges)))

    print ('Users with no profiles:', users_without_profiles)