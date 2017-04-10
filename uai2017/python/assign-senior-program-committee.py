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
from uaidata import *

# Argument handling and initialization
# .............................................................................
parser = argparse.ArgumentParser()
parser.add_argument('-a','--assignments', help="either (1) a csv file containing areachair assignments or (2) a string of the format '<user_id>,<paper#>' e.g. '~Area_Chair1,23'")
parser.add_argument('-o','--overwrite', help="if true, erases existing assignments before assigning")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client()
baseurl = client.baseurl

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')

# Function definitions
# .............................................................................
def single_assignment_valid(s):
    try:
        areachair = s.split(',')[0]
        paper_number = s.split(',')[1]

        try:
            int(paper_number)
        except ValueError:
            return False

        if not '@' in areachair and not '~' in areachair:
            return False

        return True
    except IndexError:
        return False

def assign_areachair(areachair,paper_number):
    notes = [note for note in submissions if str(note.number)==str(paper_number)]
    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')
    valid_tilde = re.compile('~.+')
    if not notes:
        print "Paper number " + paper_number + " does not exist"
    elif not valid_email.match(areachair) and not valid_tilde.match(areachair):
        print "Senior Program Committee Member \""+areachair+"\" invalid. Please check for typos and whitespace."
    else:
        #need to incorporate conflicts
        #areachair_group = get_areachair_group(areachair, paper_number, [])

        spc = client.get_group(SPC)

        areachair_profile = client.get_profile(areachair)

        if areachair_profile.id not in spc.members:
            print "%s not yet a member of the Senior Program Committee; adding them now" % areachair_profile.id
            client.add_members_to_group(spc, str(areachair_profile.id))

        acgroup = client.get_group('auai.org/UAI/2017/Paper%s/Area_Chair' % (paper_number) )
        acgroup.members = [areachair_profile.id]
        client.post_group(acgroup);
        print "Area chair %s assigned to paper%s" %(areachair_profile.id,paper_number)

def clear_assignments():
    senior_program_committee = client.get_group(SPC)
    for p in senior_program_committee.members:
        assignments = [g for g in client.get_groups(member = p) if re.compile('auai.org/UAI/2017/Paper.*/Area_Chair').match(g.id)]
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
                areachair = row[0]
                paper_number = row[1]
                assign_areachair(areachair,paper_number)
    elif single_assignment_valid(args.assignments):
        areachair = args.assignments.split(',')[0]
        paper_number = args.assignments.split(',')[1]
        assign_areachair(areachair,paper_number)
    else:
        print "Invalid input"
        sys.exit()
