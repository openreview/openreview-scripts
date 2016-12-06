#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import csv
import sys
import openreview

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--invitation', help="choose either 'question' to email users that have not submitted their pre-review question, or 'review' to do the same for official reviews")
parser.add_argument('-v','--verbose', help="set to true if you want late users listed per-paper")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)

#################################################
#                                               #
#   EDIT YOUR MESSAGE AND SUBJECT LINE BELOW    #
#                                               #
#################################################


subjectline = "<Insert your subject line here>"

message = """

<Insert your multi-line email message here>

"""


#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################

iclrsubs = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')

invitation = None

if args.invitation == 'question':
    invitation = 'pre-review/question'
elif args.invitation == 'review':
    invitation = 'official/review'

verbose = True if args.verbose.lower()=='true' else False


total_missing = 0;
total_complete = 0;

if invitation:

    late_users = set()
    print "Collecting users that did not submit their %s" % invitation

    for n in iclrsubs:
        revs = client.get_group('ICLR.cc/2017/conference/paper%s/reviewers' % n.number)

        notes = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper%s/%s' % (n.number,invitation))

        ontime_reviewers = [r.signatures[0] for r in notes]
        late_AnonReviewers = [r for r in revs.members if r not in ontime_reviewers]

        for l in late_AnonReviewers:
            late_anonRev = client.get_group(l)
            late_user = late_anonRev.members
            if verbose:
                print "late users on paper %s: %s" % (n.number,late_user)
            late_users.update(late_user)

        total_missing += len(late_AnonReviewers)
        total_complete += len(ontime_reviewers)

    response = client.send_mail(subjectline, list(late_users), message)
    print "Emailing the following users:"
    print response.json()['groups']

    print "%s: %s %ss missing" % (invitation,total_missing,args.invitation)
    print "%s: %s %ss complete" % (invitation,total_complete,args.invitation)
else:
    print "Please specify which invitation you would like to check. e.g. 'email-lazy-reviewers.py --invitation <invitation>'"



