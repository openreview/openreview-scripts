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
parser.add_argument('-a','--assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<openreview_id>,<paper#>' e.g. '~Alan_Turing1,23'", required=True)
parser.add_argument('-o','--overwrite', help="if true, erases existing assignments before assigning")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()


client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
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

def get_nonreaders(paper_number):
    # nonreaders are:
    # (1) all authors of the paper
    # (2) all domain groups of the authors of the paper

    authors = client.get_group('auai.org/UAI/2017/Paper%s/Authors' % paper_number)
    conflicts = set()
    for author in authors.members:
        try:
            author_profile = client.get_profile(author)
            conflicts.update([p.split('@')[1] for p in author_profile.content['emails']])
        except openreview.OpenReviewException:
            pass

    if 'gmail.com' in conflicts: conflicts.remove('gmail.com')

    return list(conflicts)

def assign_reviewer(reviewer,paper_number,conflict_list):
    notes = [note for note in submissions if str(note.number)==str(paper_number)]
    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')
    valid_tilde = re.compile('~.+')
    if not notes:
        print "Paper number " + paper_number + " does not exist"
    elif not valid_email.match(reviewer) and not valid_tilde.match(reviewer):
        print "Program Committee Member \""+reviewer+"\" invalid. Please check for typos and whitespace."
    else:
        reviewer_group = get_reviewer_group(reviewer, paper_number, conflict_list)


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
                print "Reviewer " + reviewer + " found in " + existing_reviewer.id
                return None

            if len(existing_reviewer.members) == 0:
                empty_reviewer_ids.append(existing_reviewer.id)

        if len(empty_reviewer_ids) > 0:
            next_empty_reviewer = sorted(empty_reviewer_ids)[0]
        else:
            reviewer_ids = [r.id for r in reviewers]
            last_reviewer_number = sorted(reviewer_ids)[-1].split('AnonReviewer')[1]
            next_empty_reviewer = CONFERENCE+"/Paper%s/AnonReviewer%s" % (paper_number, int(last_reviewer_number) + 1)

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

    reviewers.nonreaders = conflict_list
    client.post_group(reviewers)

    if next_reviewer:
        new_reviewer = create_reviewer_group(next_reviewer, reviewer_profile.id, paper_number, conflict_list)
        client.add_members_to_group(reviewers, [reviewer_profile.id])
        client.add_members_to_group(nonreaders_reviewers, new_reviewer.id)
        print "Reviewer %s assigned to paper%s" % (reviewer, paper_number)

        return new_reviewer


def create_reviewer_group(new_reviewer_id, reviewer, paper_number, conflict_list):
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

def assign(assignments):
    for a in assignments:
        reviewer = a[0]
        paper_number = a[1]
        conflict_list = get_nonreaders(paper_number)

        members = set([g.id for g in client.get_groups(member=reviewer)])
        assignee_conflicts = members.intersection(set(conflict_list))

        user_continue = True
        if len(assignee_conflicts) > 0:
            print 'This assignment has the following conflicts: %s' % assignee_conflicts
            user_continue = raw_input("Remove conflicts and continue? y/[n]: ").lower() == 'y'

        if user_continue:
            [conflict_list.remove(conflict) for conflict in assignee_conflicts]
            assign_reviewer(reviewer, paper_number, conflict_list)
        else:
            print "Paper %s not assigned" % paper_number


if args.assignments.endswith('.csv'):
    if args.overwrite and args.overwrite.lower() == 'true':
        clear_assignments()

    with open(args.assignments, 'rb') as csvfile:
        assignments = csv.reader(csvfile, delimiter=',', quotechar='|')
        assign(assignments)

elif single_assignment_valid(args.assignments):
    reviewer = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    assignments = [(reviewer, paper_number)]
    assign(assignments)

else:
    print "Invalid input"
    sys.exit()
