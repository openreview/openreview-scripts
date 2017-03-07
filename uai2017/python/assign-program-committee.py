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
import openreview
import requests
from uaidata import *

# Argument handling and initialization
# .............................................................................
parser = argparse.ArgumentParser()
parser.add_argument('-a','--assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<openreview_id>,<paper#>' e.g. '~Alan_Turing1,23'")
parser.add_argument('-o','--overwrite', help="if true, erases existing assignments before assigning")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
baseurl = client.baseurl

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')

# Function definitions
# .............................................................................
def single_assignment_valid(s):
    try:
        reviewer = s.split(',')[0]
        paper_number = s.split(',')[1]

        try:
            int(paper_number)
        except ValueError:
            return False

        if not '~' in reviewer and not '@' in reviewer:
            return False

        return True
    except IndexError:
        return False

def assign_reviewer(reviewer,paper_number):
    notes = [note for note in submissions if str(note.number)==str(paper_number)]
    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')
    valid_tilde = re.compile('~.+')
    if not notes:
        print "Paper number " + paper_number + " does not exist"
    elif not valid_email.match(reviewer) and not valid_tilde.match(reviewer):
        print "Program Committee Member \""+reviewer+"\" invalid. Please check for typos and whitespace."
    else:
        #need to incorporate conflicts. get them from public profile? confirm this with UAI documentation
        reviewer_group = get_reviewer_group(reviewer, paper_number, [])


def get_next_reviewer_id(reviewer, paper_number):

    headers = {
    'User-Agent': 'test-create-script',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + client.token
    }

    response = requests.get(client.baseurl + '/groups?id=auai.org/UAI/2017/Paper' + paper_number + '/AnonReviewer.*', headers=headers)
    reviewers = [openreview.Group.from_json(g) for g in response.json()]
    if len(reviewers) > 0:
        empty_reviewer_ids = []
        for existing_reviewer in reviewers:
            if reviewer in existing_reviewer.members:
                print "reviewer " + reviewer + " found in " + existing_reviewer.id
                return None

            if len(existing_reviewer.members) == 0:
                empty_reviewer_ids.append(existing_reviewer.id)

        if len(empty_reviewer_ids) > 0:
            next_empty_reviewer = sorted(empty_reviewer_ids)[0]
        else:
            reviewer_ids = [r.id for r in reviewers]
            last_reviewer_number = sorted(reviewer_ids)[-1].split('AnonReviewer')[1]
            next_empty_reviewer = CONFERENCE+"/Paper%s/AnonReviewer%s" % (paper_number, last_reviewer_number)

        print "existing reviewer " + next_empty_reviewer + " is empty"

        return next_empty_reviewer

    else:
        return CONFERENCE + "/Paper%s/AnonReviewer1" % paper_number


def get_reviewer_group(reviewer, paper_number, conflict_list):

    reviewers = client.get_group('auai.org/UAI/2017/Paper'+paper_number+'/Reviewers')
    nonreaders_reviewers = client.get_group('auai.org/UAI/2017/Paper'+paper_number+'/Reviewers/NonReaders')
    existing_reviewers = reviewers.members
    conference_reviewers = client.get_group(PC)

    reviewer_profile = client.get_profile(reviewer)

    if not (reviewer_profile.id in conference_reviewers.members):
        client.add_members_to_group(conference_reviewers, [reviewer_profile.id])

    next_reviewer = get_next_reviewer_id(reviewer_profile.id, paper_number)

    if next_reviewer:
        new_reviewer = create_reviewer_group(next_reviewer, reviewer_profile.id, paper_number, conflict_list)
        client.add_members_to_group(reviewers, [reviewer_profile.id])
        client.add_members_to_group(nonreaders_reviewers, new_reviewer.id) # what is /Reviewers/NonReaders actually used for?
        return new_reviewer


def create_reviewer_group(new_reviewer_id, reviewer, paper_number, conflict_list):
    print 'Creating reviewer: ', new_reviewer_id
    new_reviewer = openreview.Group(
        new_reviewer_id,
        signatures=['auai.org/UAI/2017'],
        writers=['auai.org/UAI/2017'],
        members=[reviewer],
        readers=[CONFERENCE, COCHAIRS, SPC, PC],
        nonreaders=conflict_list,
        signatories=[new_reviewer_id])
    client.post_group(new_reviewer)
    return new_reviewer

def clear_assignments():
    program_committee = client.get_group(PC)
    for p in program_committee.members:
        assignments = [g for g in client.get_groups(member = p) if re.compile('auai.org/UAI/2017/Paper.*/(AnonReviewer.*|Reviewers)').match(g.id)]
        for a in assignments:
            client.remove_members_from_group(a, a.members)

# Main script
# .............................................................................
if args.overwrite and args.overwrite.lower() == 'true':
    clear_assignments()

if args.assignments:
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
