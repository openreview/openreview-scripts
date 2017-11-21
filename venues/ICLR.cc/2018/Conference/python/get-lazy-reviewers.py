#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
from openreview import *
import requests
import config

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)


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

headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + client.token}
total_missing = 0
total_complete = 0
email_reviewers = {}

# return reviewer email for given id, or None if profile doesn't exist
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

# return specified paper if not deleted
def get_paper(paper_number):

    notes = client.get_notes(invitation=config.SUBMISSION, number = paper_number)

    if notes and not notes[0].ddate:
        return notes[0]

    return None

# create dictionary for reviewers_by_paper[paper_number][reviewer_tilde_id] = review note id
def get_data(invitation):

    paper_inv = config.CONF+'/Paper.*'
    anon_reviewers = client.get_groups(id = paper_inv+'/AnonReviewer.*')
    current_reviewers = client.get_groups(id =paper_inv+'/Reviewers')
    notes = client.get_notes(invitation=config.CONF+'/-/Paper.*/' + invitation)

    reviews = {}
    reviewers = {}
    reviewers_by_paper = {}

    for n in notes:
        signature = n.signatures[0]
        reviews[signature] = n.id

    for r in anon_reviewers:
        reviewer_id = r.id
        paper_number = reviewer_id.split('Paper')[1].split('/AnonReviewer')[0]
        members = r.members
        if members:
            reviewers[paper_number+ '_' + members[0]] = reviewer_id
        # otherwise the reviewer was removed

    for r in current_reviewers:
        reviewer_id = r.id
        members = r.members
        if members:
            paper_number = int(reviewer_id.split('Paper')[1].split('/Reviewers')[0])
            if paper_number not in reviewers_by_paper:
                reviewers_by_paper[paper_number] = {}

            for m in members:
                reviewer_id = reviewers.get(str(paper_number) + '_' + m, m)
                reviewers_by_paper[paper_number][m] = reviews.get(reviewer_id, None)

    return reviewers_by_paper


## Main ##
invitation = 'Official_Review'
# reviewers_by_paper[paper_number][reviewer_tilde_id] = review note id
reviewers_by_paper = get_data(invitation)

# late_reviewers[paper_number][reviewer_tilde_id] = reviewer_email
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

print "%s: %s missing" % (invitation,total_missing)
print "%s: %s complete" % (invitation,total_complete)


