import openreview
import requests
import csv
import argparse
import os

"""
Create user profiles -  the groups and profile are created, but not activated.
The first time the user logs in they will have to fill in their information.
"""
def get_or_create_profile(client, email, first, last, allow_duplicates=False, verbose=False):

    profile_by_email_response = requests.get(client.baseurl+"/user/profile?email=%s" % email)

    # check if email is already in use
    if 'error' in profile_by_email_response.json() or 'errors' in profile_by_email_response.json(): #if the email address doesn't belong to any tilde group
        # new user, check if this is first ~name for this name
        tilderesponse = requests.get(client.baseurl+'/tildeusername?first=%s&last=%s' %(first,last) )

        # if either first user or if duplicate and duplicates are allowed, create new profile
        if '1' in tilderesponse.json()['username'] or allow_duplicates:

            tilde = tilderesponse.json()['username']

            tilde_group = openreview.Group.from_json({
                "id": tilde,
                "tauthor": "OpenReview.net",
                "signatures": [
                    "OpenReview.net"
                ],
                "signatories": [
                    tilde
                ],
                "readers": [
                    tilde
                ],
                "writers": [
                    tilde
                ],
                "nonreaders": [],
                "members": [
                    email
                ]
            })

            if verbose: print "Generating new tilde group %s" % tilde
            client.post_group(tilde_group)

            email_group = openreview.Group.from_json({
                "id": email,
                "tauthor": "OpenReview.net",
                "signatures": [
                    "OpenReview.net"
                ],
                "signatories": [
                    email
                ],
                "readers": [
                    email
                ],
                "writers": [
                    email
                ],
                "nonreaders": [],
                "members": [
                    tilde
                ]
            })

            client.post_group(email_group)


            profile = openreview.Note.from_json({
                'id': tilde,
                'content': {
                    'emails': [email],
                    'preferred_email': email,
                    'names': [
                        {
                            'first': first,
                            'middle': '',
                            'last': last,
                            'username': tilde
                        }
                    ]
                }
            })
            response = requests.put(client.baseurl+"/user/profile", json=profile.to_json(), headers=client.headers)

            profile_by_email_response = requests.get(client.baseurl+"/user/profile?email=%s" % email)
            assert tilde in profile_by_email_response.json()['profile']['id']

            profilenote = client.get_note(tilde)
            assert email in profilenote.content['emails']

            return tilde
        else:
            print "Duplicates not allowed: %s" % tilderesponse.json()['username']
    else:
        if verbose: print "tilde groups exist for email %s" % email
        return profile_by_email_response.json()['profile']['id']




## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="openreview base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


## Read in file to user_info
user_info = []


with open(os.path.join(os.path.dirname(__file__), '../data/reviewers-formatted.csv')) as f:
    reader = csv.reader(f)

    for row in reader:
        user_info.append((row[0],row[1],row[2]))

## split user_info line into parts to create profile
profiles = []
for u in user_info:
    email = u[0].strip()
    first = u[1].strip()
    last = u[2].strip()

    if email:
        profileId = get_or_create_profile(client, email.lower(), first, last, verbose=True)
        profiles.append(profileId)


reviewers_group = client.get_group('cv-foundation.org/ECCV/2018/Demo/Reviewers')
print 'adding users to ', reviewers_group.id
client.add_members_to_group(reviewers_group, profiles)


# update profiles with conflicts

profile_notes_by_email = {}

with open(os.path.join(os.path.dirname(__file__), '../data/eccv16-reviewers-v1-conflicts.csv-36b674db-0a2a-4156-974b-baa0eae58116.csv-uploaded.csv')) as f:
    reader = csv.reader(f)
    reader.next()

    for line in reader:
        reviewer_first = line[0]
        reviewer_last = line[1]
        reviewer_email = line[2]
        relation_first = line[3]
        relation_last = line[4]
        relation_email = line[5]

        if reviewer_email not in profile_notes_by_email:
            try:
                profile = client.get_profile(reviewer_email)
                profile_note = client.get_note(profile.id)
                profile_notes_by_email[reviewer_email] = profile_note
            except openreview.OpenReviewException as e:
                print e, reviewer_email
                pass
        else:
            profile_note = profile_notes_by_email[reviewer_email]

        if 'relations' not in profile_note.content:
            profile_note.content['relations'] = []

        new_entry = {
            'email': relation_email,
            'end': None,
            'name': '{first} {last}'.format(first=relation_first, last=relation_last).title(),
            'relation': None,
            'start': None
        }
        profile_note.content['relations'].append(new_entry)
        profile_notes_by_email[reviewer_email] = profile_note

for k, v in profile_notes_by_email.iteritems():
    client.post_note(v)
