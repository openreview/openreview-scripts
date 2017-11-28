#!/usr/bin/python

"""
Lists all reviewers that have not submitted official reviews.

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

# create dictionary for reviewers_by_paper[paper_number][reviewer_tilde_id] = review note id
def get_data(invitation):

    paper_inv = config.CONF+'/Paper.*'
    anon_reviewers = client.get_groups(id = paper_inv+'/AnonReviewer.*')
    current_reviewers = client.get_groups(id =paper_inv+'/Reviewers')
    notes = []
    offset = 0
    notes_call_finished = False
    while not notes_call_finished:
        notes_batch = client.get_notes(invitation=config.CONF+'/-/Paper.*/' + invitation, offset=offset)
        notes += notes_batch
        offset += 2000
        if len(notes_batch) < 2000:
            notes_call_finished = True

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
reviewer_set = set()
for paper_number in reviewers_by_paper:

    reviewers = reviewers_by_paper[paper_number]

    for reviewer, note_id in reviewers.iteritems():

        if note_id:
            total_complete += 1
        else:
            total_missing += 1
            if paper_number not in late_reviewers:
                late_reviewers[paper_number] = []
            late_reviewers[paper_number].append(reviewer.encode('UTF-8'))
            reviewer_set.add(reviewer.encode('UTF-8'))

##print results

print "All late reviewers by paper"
for paper_number in sorted(late_reviewers):
    print "{0} {1}".format(paper_number, ','.join(late_reviewers[paper_number]))

print ""
print "All late reviewers {0}".format(len(reviewer_set))
print ','.join(reviewer_set)
print ""
print "%s: %s missing" % (invitation,total_missing)
print "%s: %s complete" % (invitation,total_complete)


