import openreview
import requests
import csv
import argparse
import re

def get_or_create_profile(client, email, first, last, allow_duplicates=False, verbose=False):

    profile_by_email_response = requests.get(client.baseurl+"/user/profile?email=%s" % email)

    if 'error' in profile_by_email_response.json() or 'errors' in profile_by_email_response.json(): #if the email address doesn't belong to any tilde group
        tilderesponse = requests.get(client.baseurl+'/tildeusername?first=%s&last=%s' %(first,last) )

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


if __name__ == '__main__':

    ## Handle the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('file',help="a csv file with the users to precreate, formatted as email,firstname,lastname")
    parser.add_argument('-g','--group', help = "after creating user profiles, add them as members to this group")
    parser.add_argument('--baseurl', help="openreview base URL")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    ## Initialize the client library with username and password
    if args.username!=None and args.password!=None:
        client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    else:
        client = openreview.Client(baseurl=args.baseurl)

    user_info = []
    with open(args.file) as f:
        reader = csv.reader(f)

        for row in reader:
            user_info.append((row[0],row[1],row[2]))

    profiles = []
    for u in user_info:
        email = u[0].strip()
        first = u[1].strip()
        last = u[2].strip()

        if email:
            profileId = get_or_create_profile(client, email.lower(), first, last, verbose=True)
            profiles.append(profileId)

    add_to_group = 'y' if args.group else raw_input("Would you like to add these profiles to a group? (y/N): ")

    if add_to_group.lower() == 'y' or add_to_group.lower() == 'yes':
        group_id = args.group if args.group else raw_input("Please enter the full path of the group that you would like to add these members to: ")

        group = client.get_group(group_id)

        client.add_members_to_group(group, profiles)

        print "Profiles added as members of group %s" % group.id


