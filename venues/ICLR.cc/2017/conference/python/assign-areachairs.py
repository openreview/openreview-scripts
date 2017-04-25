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
parser.add_argument('assignments', help="either (1) a csv file containing areachair assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'areachair@cs.umass.edu,23'")
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

submissions = openreview.get_notes(invitation='ICLR.cc/2017/conference/-/submission')

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

def assign_areachair(areachair,paper_number):
    notes = [note for note in submissions if str(note.number)==str(paper_number)]
    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')

    if not notes:
        print "Paper number " + paper_number + " does not exist" 
    elif not valid_email.match(areachair):
        print "Area chair \""+areachair+"\" invalid. Please check for typos and whitespace."
    else:
        conflicts = [note.content['conflicts'] for note in notes]
        conflict_list = []
        if conflicts:
            for c in conflicts:
                conflict_list+=c

        if 'authorids' in note.content:
            conflict_list.append(note.content['authorids'])
            
        areachair_group = get_areachair_group(areachair, paper_number, conflict_list)
        areachair_group_id = str(areachair_group.id)




def get_areachair_group(areachair, paper_number, conflict_list):
    
    areachairs = openreview.get_group('ICLR.cc/2017/conference/paper'+paper_number+'/areachairs')
    existing_areachairs = areachairs.members
    conference_areachairs = openreview.get_group('ICLR.cc/2017/areachairs')

    if not (areachair in conference_areachairs.members):
        openreview.add_members_to_group(conference_areachairs,areachair)
    
    N=0
    for a in existing_areachairs:

        reviewer_number = int(a.split('areachair')[1])
        if reviewer_number > N:
            N = reviewer_number

        existing_areachair = openreview.get_group(a)
        if hasattr(existing_areachair,'members'):
            if areachair in existing_areachair.members:
                print "areachair " + areachair + " found in " + existing_areachair.id
                return existing_areachair

    new_areachair_id = 'ICLR.cc/2017/conference/paper'+str(paper_number)+'/areachair'+str(N+1)
    new_areachair = create_areachair_group(new_areachair_id, areachair, paper_number, conflict_list)
    openreview.add_members_to_group(areachairs,new_areachair_id)
    return new_areachair


def create_areachair_group(new_areachair_id, areachair, paper_number, conflict_list):
    print 'Creating areachair: ', new_areachair_id
    new_areachair = Group(
        new_areachair_id,
        signatures=['ICLR.cc/2017/conference'],
        writers=['ICLR.cc/2017/conference'],
        members=[areachair],
        readers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/paper'+str(paper_number)+'/areachairs'],
        nonreaders=conflict_list,
        signatories=[new_areachair_id])
    openreview.post_group(new_areachair)
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
