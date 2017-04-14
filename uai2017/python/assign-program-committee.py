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
import assignment_utils
from uaidata import *

# Argument handling and initialization
# .............................................................................
parser = argparse.ArgumentParser()
parser.add_argument('-a','--add', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<user_id>,<paper#>' e.g. '~Reviewer1,23'")
parser.add_argument('-r','--remove', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<user_id>,<paper#>' e.g. '~Reviewer1,23'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()


client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
baseurl = client.baseurl

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')

headers = {
    'User-Agent': 'test-create-script',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + client.token
}

# Function definitions
# .............................................................................

def assign_reviewer(reviewer, paper_number, conflict_list):
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

    conflict_list += ['auai.org/UAI/2017/Paper%s/Authors' % paper_number]
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
        readers=[CONFERENCE, COCHAIRS, 'auai.org/UAI/2017/Paper%s/Area_Chair' % paper_number, new_reviewer_id],
        nonreaders=conflict_list,
        signatories=[new_reviewer_id])
    client.post_group(new_reviewer)
    return new_reviewer

def assign(assignments):
    for a in assignments:
        reviewer, paper_number = a
        conflict_list = assignment_utils.get_nonreaders(paper_number, client)

        reviewer_domains = assignment_utils.get_user_domains(reviewer, client)
        assignee_conflicts = reviewer_domains.intersection(conflict_list)

        user_continue = True
        if len(assignee_conflicts) > 0:
            print 'This assignment has the following conflicts: %s' % assignee_conflicts
            user_continue = raw_input("Remove conflicts and continue? y/[n]: ").lower() == 'y'

        if user_continue:
            [conflict_list.remove(conflict) for conflict in assignee_conflicts]
            assign_reviewer(reviewer, paper_number, list(conflict_list))
        else:
            print "Paper %s not assigned" % paper_number


def unassign(assignments):
    for a in assignments:
        reviewer, paper_number = a

        # remove reviewer from AnonReviewer group
        response = requests.get(client.baseurl + '/groups?id=auai.org/UAI/2017/Paper' + paper_number + '/AnonReviewer.*', headers=headers)
        anon_reviewers = [openreview.Group.from_json(g) for g in response.json()]

        for r in anon_reviewers:
            if reviewer in r.members:
                print "removing member %s from group %s" % (reviewer, r.id)
                client.remove_members_from_group(r, [reviewer])

        # remove reviewer from Paper#/Reviewers group
        reviewers_group = client.get_group('auai.org/UAI/2017/Paper%s/Reviewers' % paper_number)
        if reviewer in reviewers_group.members:
            print "removing member %s from group %s" % (reviewer, reviewers_group.id)
            client.remove_members_from_group(reviewers_group, [reviewer])

# Main script
# .............................................................................

if args.remove:
    if args.remove.endswith('.csv'):
        with open(args.remove, 'rb') as csvfile:
            unassignments = csv.reader(csvfile, delimiter=',', quotechar='|')

    elif assignment_utils.single_assignment_valid(args.remove):
        reviewer, paper_number = args.remove.split(',')
        unassignments = [(reviewer, paper_number)]

    else:
        print "Invalid input: ", args.remove
        sys.exit()

    unassign(unassignments)

if args.add:
    if args.add.endswith('.csv'):
        with open(args.add, 'rb') as csvfile:
            assignments = csv.reader(csvfile, delimiter=',', quotechar='|')

    elif assignment_utils.single_assignment_valid(args.add):
        reviewer, paper_number = args.add.split(',')
        assignments = [(reviewer, paper_number)]

    else:
        print "Invalid input: ", args.add
        sys.exit()

    conflicts = assign(assignments)
    print "conflicts found: ",conflicts
