#!/usr/bin/python

###############################################################################
# ex. python freeze-submissions.py --cpath MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
# Prevents submissions from being edited or deleted.
# Change the submission invitation so reply writers of invitations can be set to []
# For each paper: change writers to []
###############################################################################

## Import statements
import argparse
import sys
from openreview import *
import rssdata

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

###### update submission invite to allow setting writers set to []
# still allows new submissions that can't be edited
# the duedate determines whether or not new submissions can be added
submission_invite = rssdata.POSTER+'/-/Submission'
invite = client.get_invitation(submission_invite)
invite.reply['writers']['values-regex'] = '(~.*)?'
client.post_invitation(invite)

submissions = client.get_notes(invitation=submission_invite)
for paper in submissions:
    paper.writers = []
    client.post_note(paper)
    print "freezing Poster paper{0}".format(paper.number)

submission_invite = rssdata.PROCEEDINGS+'/-/Submission'
invite = client.get_invitation(submission_invite)
invite.reply['writers']['values-regex'] = '(~.*)?'
client.post_invitation(invite)

submissions = client.get_notes(invitation=submission_invite)
for paper in submissions:
    paper.writers = []
    client.post_note(paper)
    print "freezing Proceedings paper{0}".format(paper.number)
