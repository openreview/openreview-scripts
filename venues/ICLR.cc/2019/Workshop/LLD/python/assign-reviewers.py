#!/usr/bin/python

###############################################################################
''' Assigns reviewers to papers - run in same directory as py
 ex. python assign-reviewers.py --baseurl http://localhost:3000
       --username admin --password admin_pw 'reviewer@gmail.com,3'

 Checks paper number valid.
 Check reviewer email is not an author.
 Check reviewer is in the system.
 If reviewer is not in conference reviewers group (CONF/Reviewers), add it.
 If reviewer not already assigned to this paper:
	Determine AnonReviewer number
	Create Paper#/AnonReviewer#  group with this reviewer as a member
    Assign Paper#/AnonReviewer# to the Paper#/Reviewers group and
                                Paper#/Reviewers/NonReaders group for this paper'''
###############################################################################

## Import statements
import argparse
import csv
from openreview import *
from openreview import tools
import config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'reviewer@cs.umass.edu,23'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference = config.get_conference(client)


## This is used to translate from Submission paper numbers
# to Blind_Submission paper numbers
submissions = client.get_notes(invitation=conference.get_id()+'/-/Submission')

bs_iter = conference.get_submissions()
blind_submissions = {}
for bs in bs_iter:
    # blind_submission.original is equal to the submission.id
    blind_submissions[bs.original]=bs.number

def assign_reviewer(reviewer_id, paper_number):
    # check paper_number exists
    notes = [note for note in submissions if str(note.number) == paper_number]
    if not notes:
        print("Error: Paper number " + paper_number + " does not exist")
        return True
    submission = notes[0]

    if reviewer_email in submission.content['authorids']:
        print("Error: Reviewer \"" + reviewer_email + "\" is an author for Paper" + paper_number)
        return True

    conference.set_assignment(reviewer_id, blind_submissions[submission.id])
    return True

# used to clean up mistakes from when I thought blind submissions had same number as reg submissions
def remove_reviewer(email, paper_number):
    if tools.get_group(client, conference.get_id()+'/Paper'+paper_number):
        print("Removing {} from {}".format(email, paper_number))
        tools.remove_assignment(client, paper_number, conference.get_id(), email)
##################################################################

if args.assignments.endswith('.csv'):   
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None) #skip header
        for row in reader:
            paper_number = row[1]
            for i in [4,5]:
                reviewer_email = row[i]
                assign_reviewer(reviewer_email,paper_number)
else:
    reviewer_email = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    if not assign_reviewer(reviewer_email,paper_number):
        print("Invalid input. Need csv file or '<email_address>,<paper#>'")
