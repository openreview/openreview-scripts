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
import requests

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'reviewer@cs.umass.edu,23'")
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

submissions = openreview.get_notes(invitation='ICLR.cc/2017/workshop/-/submission')

def single_assignment_valid(s):
    try:
        areachair = s.split(',')[0]
        paper_number = s.split(',')[1]

        try:
            int(paper_number)
        except ValueError:
            return False

        if not '@' in areachair:
            return False

        return True
    except IndexError:
        return False

def assign_reviewer(reviewer,paper_number):
    notes = [note for note in submissions if str(note.number)==str(paper_number)]

    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')

    if not notes:
        print "Paper number " + paper_number + " does not exist"
    elif not valid_email.match(reviewer):
        print "Reviewer \""+reviewer+"\" invalid. Please check for typos and whitespace."
    else:
        conflicts = [note.content['conflicts'] for note in notes]
        conflict_list = []
        if conflicts:
            for c in conflicts:
                conflict_list+=c

        if 'authorids' in note.content:
            conflict_list+=note.content['authorids']

        reviewer_group = get_reviewer_group(reviewer, paper_number, conflict_list)
        reviewer_group_id = str(reviewer_group.id)
        review_invitation = 'ICLR.cc/2017/workshop/-/paper'+str(paper_number)+'/official/review'
        print "Assigned reviewer", reviewer_group_id, "to invitation ", review_invitation


def create_reviewer_group(new_reviewer_id, reviewer, paper_number, conflict_list):
    print 'Creating reviewer: ', new_reviewer_id
    new_reviewer = Group(
        new_reviewer_id,
        signatures=['ICLR.cc/2017/workshop'],
        writers=['ICLR.cc/2017/workshop'],
        members=[reviewer],
        readers=['ICLR.cc/2017/workshop','ICLR.cc/2017/pcs',new_reviewer_id],
        nonreaders=conflict_list,
        signatories=[new_reviewer_id])
    openreview.post_group(new_reviewer)
    return new_reviewer


def get_reviewer_group(reviewer, paper_number, conflict_list):

    reviewers = openreview.get_group('ICLR.cc/2017/workshop/paper'+paper_number+'/reviewers')
    existing_reviewers = reviewers.members

    workshop_reviewers = openreview.get_group('ICLR.cc/2017/workshop/reviewers')
    workshop_reviewers_emailed = openreview.get_group('ICLR.cc/2017/workshop/reviewers-emailed')

    if not (reviewer in workshop_reviewers_emailed.members):
        print "WARNING: You have not sent an email invitation to user ",reviewer," asking whether or not they would like to participate in the WORKSHOP."
        cont = raw_input("Would you like to continue? (y/n) [default: NO] ")
        if cont.lower()!='y' and cont.lower()!='yes':
            print "Aborting"
            sys.exit()
        openreview.add_members_to_group(workshop_reviewers_emailed,reviewer)

    if not (reviewer in workshop_reviewers.members):
        openreview.add_members_to_group(workshop_reviewers,reviewer)

    reviewer_tilde = requests.get(openreview.baseurl+'/user/profile', params={'email':reviewer}, headers=openreview.headers).json()['profile']['id']

    if '~' not in reviewer_tilde:
        print "Something went wrong with reviewer at ",reviewer
        print "reviewer_tilde = ",reviewer_tilde.id

    N = 0;
    for r in existing_reviewers:
        existing_reviewer = openreview.get_group(r)

        reviewer_number = int(r.split('AnonReviewer')[1])
        if reviewer_number > N:
            N = reviewer_number

        if hasattr(existing_reviewer,'members'):
            if reviewer in existing_reviewer.members:
                print "Reviewer " + reviewer + " found in " + existing_reviewer.id
                return existing_reviewer
            if reviewer_tilde in existing_reviewer.members:
                print "Reviewer " + reviewer_tilde + " found in " + existing_reviewer.id
                return existing_reviewer

    new_reviewer_id = 'ICLR.cc/2017/workshop/paper'+str(paper_number)+'/AnonReviewer'+str(N+1)


    new_reviewer = create_reviewer_group(new_reviewer_id, reviewer_tilde, paper_number, conflict_list)
    openreview.add_members_to_group(reviewers,new_reviewer_id)
    openreview.add_members_to_group(openreview.get_group('ICLR.cc/2017/workshop/paper'+str(paper_number)+'/review-nonreaders'),new_reviewer_id)
    return new_reviewer


##################################################################


if args.assignments.endswith('.csv'):
    with open(args.assignments, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            reviewer = row[0]
            paper_number = row[1]
            assign_reviewer(reviewer,paper_number)
elif single_assignment_valid(args.assignments):
    reviewer = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    assign_reviewer(reviewer,paper_number)
else:
    print "Invalid input"
    sys.exit()
