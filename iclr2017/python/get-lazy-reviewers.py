#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import csv
import sys
import openreview
import requests

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

headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + client.token}
total_missing = 0
total_complete = 0
email_reviewers = {}


def get_reviewer_email(id):

    if id not in email_reviewers:

        if '@' in id:
            email_reviewers[id] = id
        else:
            profile = requests.get(client.baseurl + '/user/profile?id=' + id, headers = headers)

            if profile:
                email_reviewers[id] = profile.json()['profile']['content']['preferred_email']
            else:
                print 'No profile found for', id
                email_reviewers[id] = 'Not found'

    return email_reviewers.get(id, None)

def get_paper(paper_number):

    notes = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission', number = paper_number)

    if notes and not notes[0].ddate:
        return notes[0]

    return None


def get_data(invitation):

    anon_reviewers = requests.get(client.baseurl+'/groups?id=ICLR.cc/2017/conference/paper.*/AnonReviewer.*', headers = headers)
    current_reviewers = requests.get(client.baseurl+'/groups?id=ICLR.cc/2017/conference/paper.*/reviewers', headers = headers)
    notes = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/' + invitation)

    reviews = {}
    reviewers = {}
    reviewers_by_paper = {}

    for n in notes:
        signature = n.signatures[0]
        reviews[signature] = n.id

    for r in anon_reviewers.json():
        reviewer_id = r['id']
        members = r['members']
        if members:
            reviewers[reviewer_id] = members[0]
        else:
            print 'Reviewer ', reviewer_id, ' has no members'

    for r in current_reviewers.json():
        reviewer_id = r['id']
        members = r['members']
        if members:
            paper_number = int(reviewer_id.split('paper')[1].split('/reviewers')[0])
            if paper_number not in reviewers_by_paper:
                reviewers_by_paper[paper_number] = {}

            for m in members:
                reviewer_name = reviewers.get(m, m)
                reviewers_by_paper[paper_number][reviewer_name] = reviews.get(m, None)

    return reviewers_by_paper

if invitation:

    reviewers_by_paper = get_data(invitation)

    late_reviewers = {}
    print "Collecting users that did not submit their %s" % invitation

    total_complete = 0
    total_missing = 0
    for paper_number in reviewers_by_paper:

        reviewers = reviewers_by_paper[paper_number]

        for reviewer, note_id in reviewers.iteritems():

            if note_id:
                total_complete += 1
            else:
                total_missing += 1
                if paper_number not in late_reviewers:
                    late_reviewers[paper_number] = {}
                late_reviewers[paper_number][reviewer] = get_reviewer_email(reviewer)

    ##print results
    for paper_number in sorted(late_reviewers):

        paper = get_paper(paper_number)
        if paper:
            reviewers = late_reviewers[paper_number]
            for reviewer, email in reviewers.iteritems():
                print str(paper_number) + "," + reviewer + ',' + email
        else:
            print 'Submission not found', paper_number



    print "%s: %s %ss missing" % (invitation,total_missing,args.invitation)
    print "%s: %s %ss complete" % (invitation,total_complete,args.invitation)
else:
    print "Please specify which invitation you would like to check. e.g. 'email-lazy-reviewers.py --invitation <invitation>'"



