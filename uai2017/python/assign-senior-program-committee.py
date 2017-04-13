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
import assignment_utils
from uaidata import *

# Argument handling and initialization
# .............................................................................
parser = argparse.ArgumentParser()
parser.add_argument('-a','--add', help="either (1) a csv file containing areachair assignments or (2) a string of the format '<user_id>,<paper#>' e.g. '~Area_Chair1,23'")
parser.add_argument('-r','--remove', help="either (1) a csv file containing areachair assignments or (2) a string of the format '<user_id>,<paper#>' e.g. '~Area_Chair1,23'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()


client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

baseurl = client.baseurl

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')

# Function definitions
# .............................................................................


def assign_areachair(areachair, paper_number, conflict_list):
    notes = [note for note in submissions if str(note.number)==str(paper_number)]
    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')
    valid_tilde = re.compile('~.+')
    if not notes:
        print "Paper number " + paper_number + " does not exist"
    elif not valid_email.match(areachair) and not valid_tilde.match(areachair):
        print "Senior Program Committee Member \""+areachair+"\" invalid. Please check for typos and whitespace."
    else:
        spc = client.get_group(SPC)

        areachair_profile = client.get_profile(areachair)

        if areachair_profile.id not in spc.members:
            print "%s not yet a member of the Senior Program Committee; adding them now" % areachair_profile.id
            client.add_members_to_group(spc, str(areachair_profile.id))

        acgroup = client.get_group('auai.org/UAI/2017/Paper%s/Area_Chair' % (paper_number) )
        acgroup.members = [areachair_profile.id]
        acgroup.nonreaders = conflict_list
        client.post_group(acgroup);
        print "Area chair %s assigned to paper%s" % (areachair_profile.id, paper_number)

def assign(assignments):
    for a in assignments:
        areachair = a[0]
        paper_number = a[1]
        conflict_list = assignment_utils.get_nonreaders(paper_number, client)

        members = set([g.id for g in client.get_groups(member=areachair)])
        assignee_conflicts = members.intersection(set(conflict_list))

        user_continue = True
        if len(assignee_conflicts) > 0:
            print 'This %s has the following conflicts on paper %s: %s' % (areachair, paper_number, assignee_conflicts)
            user_continue = raw_input("Remove conflicts and continue? y/[n]: ").lower() == 'y'

        if user_continue:
            [conflict_list.remove(conflict) for conflict in assignee_conflicts]
            assign_areachair(areachair, paper_number, conflict_list)
        else:
            print "Paper %s not assigned" % paper_number

def unassign(assignments):
    for a in assignments:
        areachair, paper_number = a

        acgroup = client.get_group('auai.org/UAI/2017/Paper%s/Area_Chair' % (paper_number) )

        if areachair in acgroup.members:
            print "removing area chair %s from group %s" % (areachair, acgroup.id)
            client.remove_members_from_group(acgroup,[areachair])
        else:
            print "area chair %s not found in group %s" % (areachair, acgroup.id)

# Main script
# .............................................................................

if args.remove:
    if args.remove.endswith('.csv'):
        with open(args.remove, 'rb') as csvfile:
            unassignments = csv.reader(csvfile, delimiter=',', quotechar='|')

    elif assignment_utils.single_assignment_valid(args.remove):
        areachair, paper_number = args.remove.split(',')
        unassignments = [(areachair, paper_number)]

    else:
        print "Invalid input"
        sys.exit()

    unassign(unassignments)

if args.add:
    if args.add.endswith('.csv'):
        with open(args.add, 'rb') as csvfile:
            assignments = csv.reader(csvfile, delimiter=',', quotechar='|')

    elif assignment_utils.single_assignment_valid(args.add):
        areachair, paper_number = args.add.split(',')
        assignments = [(areachair, paper_number)]

    else:
        print "Invalid input"
        sys.exit()

    assign(assignments)


