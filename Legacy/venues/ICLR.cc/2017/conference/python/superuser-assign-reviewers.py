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
parser.add_argument('assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'reviewer@cs.umass.edu,23'")
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
conference_reviewers = client.get_group('ICLR.cc/2017/conference/reviewers')
conference_reviewers_invited = client.get_group('ICLR.cc/2017/conference/reviewers-invited')

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
    if notes:
        conflicts = list(notes[0].content['conflicts'])

        if 'authorids' in note.content:
            conflicts += note.content['authorids']

        reviewer_group, invited, tilde_found = get_reviewer_group(reviewer, paper_number, conflicts)
        
        reviewer_group_id = str(reviewer_group.id)
        
        preview_question_invitation = 'ICLR.cc/2017/conference/-/paper'+str(paper_number)+'/pre-review/question'

        return invited, tilde_found
    else:
        print "Paper number " + paper_number + " does not exist" 


def create_reviewer_group(new_reviewer_id, member, paper_number, conflict_list):
    print 'Creating reviewer: ', new_reviewer_id

    new_reviewer = Group(
        new_reviewer_id,
        signatures=['ICLR.cc/2017/conference'],
        writers=['ICLR.cc/2017/conference'],
        members=[member],
        readers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs',new_reviewer_id,'ICLR.cc/2017/conference/paper'+str(paper_number)+'/areachairs'],
        nonreaders=conflict_list,
        signatories=[new_reviewer_id])
    client.post_group(new_reviewer)
    return new_reviewer

    

def get_reviewer_group(reviewer, paper_number, conflict_list):
    
    invited = True
    if not (reviewer in conference_reviewers_invited.members):
        # print "WARNING: You have not sent an email invitation to user ",reviewer," asking whether or not they would like to participate."
        # cont = raw_input("Would you like to continue? (y/n) [default: NO] ")
        # if cont.lower()!='y' and cont.lower()!='yes':
        #     print "Aborting"
        #     sys.exit()
        invited = False
        client.add_members_to_group(conference_reviewers_invited,reviewer)

    if not (reviewer in conference_reviewers.members):
        client.add_members_to_group(conference_reviewers,reviewer)
    
    #could move out this call to the top
    reviewers = client.get_group('ICLR.cc/2017/conference/paper'+paper_number+'/reviewers')
    existing_reviewers = reviewers.members
    
    tilde_found = True

    try:
        user_email_group = client.get_group(reviewer)
        tildegroups = [i for i in user_email_group.members if re.compile('~.*').match(i)]

        if len(tildegroups) > 0:
            member = tildegroups[0]
        else:
            print 'no tilde ids in group',user_email_group.id,'; continuing assignment with email address';
            member=reviewer
            tilde_found = False
    except OpenReviewException as e:
        print "continuing assignment with email address"
        member=reviewer
        tilde_found = False

    N=0
    for r in existing_reviewers:
        existing_reviewer = client.get_group(r)

        reviewer_number = int(r.split('AnonReviewer')[1])
        if reviewer_number > N:
            N = reviewer_number

        if hasattr(existing_reviewer,'members'):
            if member in existing_reviewer.members:
                print "Reviewer " + member + " found in " + existing_reviewer.id
                return existing_reviewer,invited,tilde_found
    
    new_reviewer_id = 'ICLR.cc/2017/conference/paper'+str(paper_number)+'/AnonReviewer'+str(N+1)
    new_reviewer = create_reviewer_group(new_reviewer_id, member, paper_number, conflict_list)
    client.add_members_to_group(reviewers,new_reviewer_id)
    client.add_members_to_group(client.get_group('ICLR.cc/2017/conference/paper'+str(paper_number)+'/review-nonreaders'),new_reviewer_id)
    
    return new_reviewer,invited,tilde_found


##################################################################

if args.assignments.endswith('.csv'):   
    reviewers_not_invited = []
    tilde_groups_not_found = []
    with open(args.assignments, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            paper_number = row[0]
            reviewer = row[1]
            invited,tilde_found = assign_reviewer(reviewer,paper_number)
            reviewers_not_invited.append(reviewer)
            tilde_groups_not_found.append(reviewer)
    print "Reviewers who were not previously invited: ",reviewers_not_invited
    print "Reviewers whose tilde groups were not found: ",tilde_groups_not_found
elif single_assignment_valid(args.assignments):
    reviewer = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    invited,tilde_found = assign_reviewer(reviewer,paper_number)
    if not invited:
        print "reviewer ",reviewer," was not previously invited via email. Please be sure that this reviewer is aware of his or her request to review."
    if not tilde_found:
        print "an account name for reviewer ",reviewer," could not be found. their email address has been added as a member of their reviewer group instead."
else:
    print "Invalid input"
    sys.exit()
