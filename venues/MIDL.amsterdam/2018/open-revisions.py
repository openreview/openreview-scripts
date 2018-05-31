#!/usr/bin/python

"""
## turn on revisions for accepted papers
## send emails to accepted authors
"""

## Import statements
import argparse
import openreview
import csv

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)


#################################################
#                                               #
#   EDIT YOUR MESSAGE AND SUBJECT LINE BELOW    #
#                                               #
#################################################

title = 'MIDL submission revisions open'
message = '''Thank you for your submission to MIDL. You are allowed to add revisions to your submission between now and June 11th.

Sincerely,
Geert Litjens
Ivana Isgum
Clarisa Sanchez
'''
#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################

def open_and_send(track):
    conference = 'MIDL.amsterdam/2018/' + track
    revisions = client.get_invitations(regex=conference + '/-/Paper.*/Add/Revision')
    decisions = client.get_notes(invitation=conference + '/-/Paper.*/Acceptance_Decision')

    rev_by_num = {}
    for rev in revisions:
        paper_num = rev.id.split('Paper')[1].split('/')[0]
        rev_by_num[paper_num] = rev

    for dec in decisions:
        if dec.content['decision'] != 'Reject':
            paper_num = dec.invitation.split('Paper')[1].split('/')[0]
            author_group = client.get_group(conference + '/Paper' + paper_num + '/Authors')
            # allow authors to add revisions
            rev_by_num[paper_num].invitees = [author_group.id]
            client.post_invitation(rev_by_num[paper_num])
            #print track+': '+paper_num + " " + dec.content['decision']
            # send email
            client.send_mail(title, author_group.members, message)


open_and_send('Conference')
open_and_send('Abstract')