#!/usr/bin/python

###############################################################################
# Assigns reviewers to papers
# ex. python assign-reviewers.py --baseurl http://localhost:3000
#       --username pmandler --password supersecret --track Proceedings 'reviewer@gmail.com,3'
###############################################################################

## Import statements
import argparse
import csv
import getpass
import sys
import re
import openreview
import requests
from rssdata import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'reviewer@cs.umass.edu,23'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--track', help="'Poster' or 'Proceedings'")
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
baseurl = client.baseurl

if args.track != 'Poster' and args.track != 'Proceedings':
    print("set --track to either Poster or Proceedings")
    sys.exit()
TRACK = CONFERENCE+"/"+args.track
submissions = client.get_notes(invitation=TRACK+'/-/Submission')

## parses command line assignments - looks for pairs of emails and paper numbers
def single_assignment_valid(s):
    try:
        reviewer = s.split(',')[0]
        paper_number = s.split(',')[1]

        try:
            int(paper_number)
        except ValueError:
            return False

        if not '@' in reviewer:
            return False

        return True
    except IndexError:
        return False

# does some parameter checking before handing off to get_reviewer_group
# which really does the assigning
def assign_reviewer(reviewer,paper_number):
    notes = [note for note in submissions if str(note.number)==str(paper_number)]

    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')

    if not notes:
        print "Paper number " + paper_number + " does not exist in "+args.track
    elif not valid_email.match(reviewer):
        print "Reviewer \""+reviewer+"\" invalid. Please check for typos and whitespace."
    else:
        # create list of conflicts emails and add paper author to it
        conflicts = [note.content['conflicts'] for note in notes]
        conflict_list = []
        if conflicts:
            for c in conflicts:
                conflict_list+=c

        if 'authorids' in note.content:
            conflict_list+=note.content['authorids']

        reviewer_group = get_reviewer_group(reviewer, paper_number, conflict_list)


def create_reviewer_group(new_reviewer_id, reviewer, conflict_list):
    new_reviewer = openreview.Group(
        new_reviewer_id,
        signatures=[TRACK],
        writers=[TRACK],
        members=[reviewer],
        readers=[TRACK, COCHAIRS, new_reviewer_id],
        nonreaders=conflict_list,
        signatories=[new_reviewer_id])
    client.post_group(new_reviewer)
    print "assigned user %s to group %s" % (reviewer, new_reviewer_id)
    return new_reviewer

# gets reviewers for given paper
# adds the given reviewer to the workshop reviewers if not already there
def get_reviewer_group(reviewer, paper_number, conflict_list):

    reviewers = client.get_group(TRACK+'/Paper'+paper_number+'/Reviewers')
    existing_reviewers = reviewers.members

    workshop_reviewers = client.get_group(TRACK+'/Reviewers')

    if not (reviewer in workshop_reviewers.members):
        client.add_members_to_group(workshop_reviewers,reviewer)

    reviewer_tilde = requests.get(client.baseurl+'/user/profile', params={'email':reviewer}, headers=client.headers).json()['profile']['id']

    if '~' not in reviewer_tilde:
        print "Something went wrong with reviewer at ",reviewer
        print "reviewer_tilde = ",reviewer_tilde.id

    # determine what number AnonReviewer this new reviewer should be
    # by searching for largest AnonReviewer so far
    N = 0;
    for r in existing_reviewers:
        existing_reviewer = client.get_group(r)
        # check if reviewer is already in the group by looking for given reviewer email, or associated ~name
        if hasattr(existing_reviewer,'members'):
            if reviewer in existing_reviewer.members:
                print "Reviewer " + reviewer + " found in " + existing_reviewer.id
                return existing_reviewer
            if reviewer_tilde in existing_reviewer.members:
                print "Reviewer " + reviewer_tilde + " found in " + existing_reviewer.id
                return existing_reviewer
        # r isn't the given reviewer - check for the Anon number
        reviewer_number = int(r.split('AnonReviewer')[1])
        if reviewer_number > N:
            N = reviewer_number

    # reviewer not in current group
    # create new group for this new reviewer with Anon name
    # add that to the existing reviewers group
    new_reviewer_id = TRACK+'/Paper'+str(paper_number)+'/AnonReviewer'+str(N+1)

    new_reviewer = create_reviewer_group(new_reviewer_id, reviewer_tilde, conflict_list)
    client.add_members_to_group(reviewers,new_reviewer_id)
    reviewers_incomplete = client.get_group(TRACK+'/Paper'+paper_number+'/Reviewers/Incomplete')
    client.add_members_to_group(reviewers_incomplete, new_reviewer_id)
    #client.add_members_to_group(client.get_group(TRACK+'/Paper'+str(paper_number)+'/review-nonreaders'),new_reviewer_id)
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
