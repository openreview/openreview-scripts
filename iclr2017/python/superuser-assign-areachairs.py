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
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = Client(baseurl=args.baseurl)
baseurl = client.baseurl

submissions = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
conference_areachairs = client.get_group('ICLR.cc/2017/areachairs')

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
    if notes:
        note = notes[0]
        conflicts = list(note.content['conflicts'])
        if 'authorids' in note.content:
            conflicts += note.content['authorids']
            
        areachair_group = get_areachair_group(areachair, paper_number, conflicts)
        areachair_group_id = str(areachair_group.id)

        client.post_invitation(client.get_invitation('ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/public/review').add_noninvitee(areachair_group_id))
        client.post_invitation(client.get_invitation('ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/public/comment').add_noninvitee(areachair_group_id))
    else:
        print "Paper number " + paper_number + " does not exist" 



def get_areachair_group(areachair, paper_number, conflict_list):
    
    areachairs = client.get_group('ICLR.cc/2017/conference/paper'+paper_number+'/areachairs')
    existing_areachairs = areachairs.members

    try:
        areachairgroup = client.get_group(areachair)
        tildegroups = [i for i in areachairgroup.members if re.compile('~.*').match(i)]
        
        if len(tildegroups) > 0:
            member = tildegroups[0]
        else:
            print 'no tilde ids in group',reviewergroup.id,'; continuing assignment with email address';
            member=reviewer
            tilde_found = False
    except OpenReviewException as e:
        print "continuing assignment with email address"
        member=areachair

    if not (areachair in conference_areachairs.members):
        client.add_members_to_group(conference_areachairs,areachair)
    
    for a in existing_areachairs:
        existing_areachair = client.get_group(a)
        if hasattr(existing_areachair,'members'):
            if member in existing_areachair.members:
                print "areachair " + areachair + " found in " + existing_areachair.id
                return existing_areachair

    new_areachair_id = 'ICLR.cc/2017/conference/paper'+str(paper_number)+'/areachair'+str(len(existing_areachairs)+1)
    new_areachair = create_areachair_group(new_areachair_id, member, paper_number, conflict_list)
    client.add_members_to_group(areachairs,new_areachair_id)
    return new_areachair


def create_areachair_group(new_areachair_id, member, paper_number, conflict_list):
    print 'Creating areachair: ', new_areachair_id
    new_areachair = Group(
        new_areachair_id,
        signatures=['ICLR.cc/2017/conference'],
        writers=['ICLR.cc/2017/conference'],
        members=[member],
        readers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/paper'+str(paper_number)+'/areachairs'],
        nonreaders=conflict_list,
        signatories=[new_areachair_id])
    client.post_group(new_areachair)
    return new_areachair


##################################################################


if args.assignments.endswith('.csv'):   
    with open(args.assignments, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            paper_number = row[0]
            areachair = row[1]
            assign_areachair(areachair,paper_number)
elif single_assignment_valid(args.assignments):
    areachair = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    assign_areachair(areachair,paper_number)
else:
    print "Invalid input"
    sys.exit()
