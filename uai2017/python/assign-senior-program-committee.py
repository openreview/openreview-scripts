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

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing areachair assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'areachair@cs.umass.edu,23'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
baseurl = client.baseurl

submissions = client.get_notes(invitation='UAI.org/2017/conference/-/submission')

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
        areachair_group = get_areachair_group(areachair, paper_number, [])




def get_areachair_group(areachair, paper_number, conflict_list):

    areachairs = client.get_group('UAI.org/2017/conference/paper'+paper_number+'/Senior_Program_Committee')
    existing_areachairs = areachairs.members
    conference_areachairs = client.get_group('UAI.org/2017/conference/Senior_Program_Committee')

    if not (areachair in conference_areachairs.members):
        client.add_members_to_group(conference_areachairs,areachair)

    N=0
    for a in existing_areachairs:

        reviewer_number = int(a.split('Senior_Program_Committee_Member')[1])
        if reviewer_number > N:
            N = reviewer_number

        existing_areachair = client.get_group(a)
        if hasattr(existing_areachair,'members'):
            if areachair in existing_areachair.members:
                print "areachair " + areachair + " found in " + existing_areachair.id
                return existing_areachair

    new_areachair_id = 'UAI.org/2017/conference/paper'+str(paper_number)+'/Senior_Program_Committee_Member1'+str(N+1)
    new_areachair = create_areachair_group(new_areachair_id, areachair, paper_number, conflict_list)
    client.add_members_to_group(areachairs,new_areachair_id)
    return new_areachair


def create_areachair_group(new_areachair_id, areachair, paper_number, conflict_list):
    print 'Creating areachair: ', new_areachair_id
    new_areachair = openreview.Group(
        new_areachair_id,
        signatures=['UAI.org/2017/conference'],
        writers=['UAI.org/2017/conference'],
        members=[areachair],
        readers=['UAI.org/2017/conference',new_areachair_id,'UAI.org/2017/conference/Program_Co-Chairs'],
        nonreaders=conflict_list,
        signatories=[new_areachair_id])
    client.post_group(new_areachair)
    return new_areachair


##################################################################


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
