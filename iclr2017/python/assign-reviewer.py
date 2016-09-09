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

def create_reviewer_group(openreview, new_reviewer_id, reviewer, paper_number, conflict_list):
    print 'Create reviewer: ', new_reviewer_id
    new_reviewer = Group(
        new_reviewer_id,
        signatures=['ICLR.cc/2017/conference'],
        writers=['ICLR.cc/2017/conference'],
        members=[reviewer],
        readers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/paper'+str(paper_number)+'/reviewers',reviewer],
        nonreaders=conflict_list,
        signatories=['ICLR.cc/2017/conference',reviewer])
    openreview.post_group(new_reviewer)
    return new_reviewer
    

def get_reviewer_group(openreview, reviewer, paper_number, conflict_list):
    
    reviewers = openreview.get_group('ICLR.cc/2017/conference/paper'+paper_number+'/reviewers')
    existing_reviewers = reviewers.members

    for r in existing_reviewers:
        existing_reviewer = openreview.get_group(r)
        if hasattr(existing_reviewer,'members'):
            if reviewer in existing_reviewer.members:
                print "Reviewer " + reviewer + " found in " + existing_reviewer.id
                return existing_reviewer
    new_reviewer_id = 'ICLR.cc/2017/conference/paper'+str(paper_number)+'/reviewer'+str(len(existing_reviewers)+1)
    new_reviewer = create_reviewer_group(openreview, new_reviewer_id, reviewer, paper_number, conflict_list)
    openreview.post_group(reviewers.add_member(new_reviewer.id))
    openreview.post_group(openreview.get_group('ICLR.cc/2017/conference/paper'+str(paper_number)+'/review-nonreaders').add_member(new_reviewer_id))
    conference_reviewers = openreview.get_group('ICLR.cc/2017/conference/reviewers')
    conference_reviewers_invited = openreview.get_group('ICLR.cc/2017/conference/reviewers-invited')

    if not (reviewer in conference_reviewers.members):
        openreview.post_group(conference_reviewers.add_member(reviewer))

    if not (reviewer in conference_reviewers_invited.members):
        openreview.post_group(conference_reviewers_invited.add_member(reviewer))
    return new_reviewer


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

conflicts = [note.content['conflicts'] for note in openreview.get_notes(invitation='ICLR.cc/2017/conference/-/submission') if str(note.number)==str(paper_number)]
conflict_list = []
if conflicts:
    for c in conflicts[0].split(';'):
        if str(c.strip()):
            conflict_list.append(str(c.strip()))
user_conflict = None
for c in conflict_list:
    group = openreview.get_group(c)
    if group.members and openreview.user['id'] in group.members:
        user_conflict = c    

if user_conflict==None:
    reviewer_group = get_reviewer_group(openreview, reviewer, paper_number, conflict_list)
    reviewer_group_id = str(reviewer_group.id)
    official_invitation = 'ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/official/review'
    print "Assigned reviewer", reviewer_group_id, "to invitation ", official_invitation
    openreview.post_invitation(openreview.get_invitation(official_invitation).add_invitee(reviewer_group_id))
    openreview.post_invitation(openreview.get_invitation('ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/public/review').add_noninvitee(reviewer_group_id))
    openreview.post_invitation(openreview.get_invitation('ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/public/comment').add_noninvitee(reviewer_group_id))
else:
    print "Aborted. User "+ openreview.user['id']+" has conflict of interest on this paper for the domain ["+user_conflict+"]."

            








