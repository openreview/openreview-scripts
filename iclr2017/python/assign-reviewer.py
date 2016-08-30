#!/usr/bin/python

###############################################################################
# Not to spec
###############################################################################

## Import statements
import argparse
import csv
import getpass
import sys
import re
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('reviewer', help="the reviewer email address to assign")
parser.add_argument('paper_number', help="the number of the paper to assign this reviewer to")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)
baseurl = openreview.baseurl

reviewer = args.reviewer
paper_number = args.paper_number

reviewers = openreview.get_group('ICLR.cc/2017/conference/paper'+paper_number+'/reviewers')
existing_reviewers = reviewers.members

reviewer_number = len(existing_reviewers)+1

for r in existing_reviewers:
    existing_reviewer = openreview.get_group(r)
    print existing_reviewer
    if reviewer in existing_reviewer.members:
        print "reviewer found in existing_reviewers.members"
        reviewer_number = existing_reviewers.index(r)+1
        break

print reviewer_number

new_reviewer_id = 'ICLR.cc/2017/conference/paper'+str(paper_number)+'/reviewer'+str(reviewer_number)
new_reviewer = Group(
    new_reviewer_id,
    signatures=['ICLR.cc/2017/conference'],
    writers=['ICLR.cc/2017/conference'],
    members=[reviewer],
    readers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs',reviewer],
    signatories=['ICLR.cc/2017/conference',reviewer]
)
openreview.post_group(new_reviewer)
openreview.post_group(reviewers.add_member(new_reviewer.id))
openreview.post_group(openreview.get_group('ICLR.cc/2017/conference/paper'+str(paper_number)+'/review-nonreaders').add_member(new_reviewer_id))

openreview.post_invitation(openreview.get_invitation('ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/public/review').add_noninvitee(new_reviewer_id))
openreview.post_invitation(openreview.get_invitation('ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/public/comment').add_noninvitee(new_reviewer_id))











