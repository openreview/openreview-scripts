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
parser.add_argument('-v','--verbose', help="set to true if you want late users listed per-paper")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

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

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
invitation = 'Submit/Review'

verbose = True if args.verbose and args.verbose.lower()=='true' else False


total_missing = 0;
total_complete = 0;

def get_data(invitation):

    headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + client.token}
    anon_reviewers = requests.get(client.baseurl+'/groups?id=auai.org/UAI/2017/Paper.*/AnonReviewer.*', headers = headers)
    current_reviewers = requests.get(client.baseurl+'/groups?id=auai.org/UAI/2017/Paper.*/Reviewers', headers = headers)
    notes = client.get_notes(invitation='auai.org/UAI/2017/-/Paper.*/' + invitation)

    reviews = {}
    reviewers = {}
    all_reviewers = {}
    reviewers_by_paper = {}

    for n in notes:
        signature = n.signatures[0]
        reviews[signature] = n.id

    for r in anon_reviewers.json():
        reviewer_id = r['id']
        members = r['members']
        if members:
            username = members[0]
            if username not in reviewers:
                reviewers[username] = []
            reviewers[username].append(reviewer_id)
        # else:
        #     print 'Reviewer ', reviewer_id, ' has no members'

    for r in current_reviewers.json():
        reviewers_id = r['id']
        members = r['members']
        if members:
            all_reviewers[reviewers_id] = members

    for submission in submissions:
        paper_number = submission.number
        paper_data = {}

        paper_reviewers = all_reviewers['auai.org/UAI/2017/Paper' + str(paper_number) + '/Reviewers']

        for r in paper_reviewers:
            anon_groups = reviewers.get(r, [])
            anon_group = next(g for g in anon_groups if 'Paper' + str(paper_number) in g)
            paper_data[r] = reviews.get(anon_group, None)

        reviewers_by_paper[paper_number] = paper_data

    return reviewers_by_paper


## Main
reviewers_by_paper = get_data(invitation)

late_users = set()
print "Collecting users that did not submit their %s" % invitation

total_complete = 0
total_missing = 0
for paper_number in sorted(reviewers_by_paper):

    reviewers = reviewers_by_paper[paper_number]

    for reviewer, note_id in reviewers.iteritems():

        if note_id:
            total_complete += 1
        else:
            total_missing += 1
            if verbose:
                print "late reviewers on paper %s: %s" % (paper_number, reviewer)
            late_users.add(reviewer)

# Comment this out to send the emails
# response = client.send_mail(subjectline, list(late_users), message)
# print "Emailing the following users:"
# print response['groups']

print "%s: %s missing" % (invitation,total_missing)
print "%s: %s complete" % (invitation,total_complete)




