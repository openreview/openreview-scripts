#!/usr/bin/python

###############################################################################
# ex. python author-precreate-profile.py --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# Find authors and precreate profiles if they are missing.
# Possible to change out emails w/ tildeId's in future.
###############################################################################

## Import statements
import argparse
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

"""
Wrapper around OpenReview.get_profile to catch Profile not found exceptions.
"""
def get_profile(value):
    profile = None
    try:
        profile = client.get_profile(value)
    except openreview.OpenReviewException as e:
        # throw an error if it is something other than "not found"
        if e[0][0] != 'Profile not found':
            print "OpenReviewException: {0}".format(e)
            raise e
    return profile

"""
Create user profiles -  the groups and profile are created, but not activated.
The first time the user logs in they will have to fill in their information.
"""
def create_profile(email, first, last, tilde_id, verbose=False):

    tilde_group = openreview.Group(tilde_id,
                                   signatures = ["OpenReview.net"],
                                   signatories=[tilde_id],
                                   readers=[tilde_id],
                                   writers=[tilde_id],
                                   nonreaders=[],
                                   members=[email])
    if verbose: print "Generating new tilde group %s" % tilde_id
    client.post_group(tilde_group)

    email_group = openreview.Group(email,
                                   signatures=["OpenReview.net"],
                                   signatories=[email],
                                   readers=[email],
                                   writers=[email],
                                   nonreaders=[],
                                   members=[tilde_id])
    client.post_group(email_group)

    profile = openreview.Note.from_json({
        'id': tilde_id,
        'content': {
            'emails': [email],
            'preferred_email': email,
            'names': [{
                'first': first,
                'middle': '',
                'last': last,
                'username': tilde_id
            }]
        }
    })

    # Why doesn't  "client.post_note(profile)" work? throws OpenReviewException: [u'note does not exist']
    response = requests.put(client.baseurl+"/user/profile", json=profile.to_json(), headers=client.headers)


# for all submissions get authorids, if in form of email address, try to find associated profile
# if profile doesn't exist, create one
offset = 0
limit = 200
while True:
    # go through all notes, count as submission if it has authorids
    notes = client.get_notes(offset=offset, limit=limit)
    for note in notes:
        if 'authorids' in note.content:
            # iterate through authorids and authors at the same time
            for (id, name) in zip(note.content['authorids'], note.content['authors']):
                if '@' in id:
                    # if the id is in the form of an email, try to get the profile
                    id = id.strip()
                    id = id.encode('utf-8')
                    email_profile = get_profile(id)
                    if email_profile == None:
                        # author profile doesn't exist with this email address
                        # look up profile using author's ~id
                        name = name.strip()
                        name = name.encode('utf-8')
                        name = name.replace(' ', '_')
                        tildename = "~" + name + "1"
                        # print tildename
                        name_profile = get_profile(tildename)
                        if name_profile != None:
                            # if name_profile exists - print to examine if correct person
                            print "Does '{0}' email belong with {1} '{2}'?".format(id, tildename, name_profile.content[
                                'preferred_email'])
                        else:
                            # if name_profile doesn't exists create profile
                            first = name.split('_')[0]
                            last = name.split('_')[-1]
                            try:
                                create_profile(id, first, last, tildename, True)
                            except openreview.OpenReviewException as e:
                                print "ERROR note: {0} OpenReviewException: {1}".format(note.id, e)

    ## run out of notes
    if len(notes) < limit:
        break
    offset += limit
