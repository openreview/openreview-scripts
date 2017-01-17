import openreview
import requests
import csv
import argparse
import re
from uaidata import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('file',help="the csv file containing the Senior_Program_Committee names and email addresses")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)

def get_or_create_profile(email, first, last):

    profile_by_email_response = requests.get(client.baseurl+"/user/profile?email=%s" % email)

    if 'error' in profile_by_email_response.json() or 'errors' in profile_by_email_response.json(): #if the email address doesn't belong to any tilde group
        tilderesponse = requests.get(client.baseurl+'/tildeusername?first=%s&last=%s' %(first,last) )
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

        print "Generating new tilde group %s" % tilde
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
        print "tilde groups exist for email %s" % email
        return profile_by_email_response.json()['profile']['id']


spc_member_info = []
with open(args.file) as f:
    reader = csv.reader(f)

    for row in reader:
        spc_member_info.append((row[0],row[1],row[2]))

spcs_invited = client.get_group(id=SPC+'/invited')
profiles = []

for u in spc_member_info:
    email = u[0].strip()
    first = u[1].strip()
    last = u[2].strip()

    if email:
        profileId = get_or_create_profile(email.lower(), first, last)

        if profileId not in spcs_invited.members:
            profiles.append(profileId)

client.add_members_to_group(spcs_invited, profiles)

print "Profiles added: ", profiles


