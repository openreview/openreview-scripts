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

submissions = client.get_notes(invitation=conference.get_submission_id())

## checks for valid paper numbers and email addresses
def check_arguments(email_addr, paper_number):
    try:
        int(paper_number)
    except ValueError:
        print("Error: Paper number \"" + paper_number + "\" invalid.")
        return False

    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')
    if not valid_email.match(email_addr):
        print("Error: Reviewer \""+email_addr+"\" invalid. Please check for typos and whitespace.")
        return False

    return True

# does some parameter checking, checks for conflicts
# check if reviewer already assigned to paper
# if not then create Anonymous group for the reviewer and add to reviewer group
def assign_reviewer(reviewer_email, paper_number):
    print(reviewer_email)
    if not check_arguments(reviewer_email, paper_number):
        return False

    # check paper_number exists
    notes = [note for note in submissions if str(note.number) == paper_number]
    if not notes:
        print("Error: Paper number " + paper_number + " does not exist")
        return True
    note = notes[0]

    if reviewer_email in note.content['authorids']:
        print("Error: Reviewer \"" + reviewer_email + "\" is an author for Paper" + paper_number)
        return True

    tools.assign(client, paper_number, conference.get_id(), reviewer_to_add = reviewer_email)
    return True

##################################################################
reviewers = openreview.Group(conference.get_id()+'/Reviewers',
    readers=[conference.get_id(), conference.get_program_chairs_id()],
    writers=[conference.get_id(), conference.get_program_chairs_id()],
    signatories= [conference.get_id(), conference.get_program_chairs_id()],
    signatures= [conference.get_id()]
)

if args.assignments.endswith('.csv'):   
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None) #skip header
        for row in reader:
            paper_number = row[1]
            for i in [2,3,4]:
                reviewer_email = row[i].lower()
                reviewers.members.append(reviewer_email)
                assign_reviewer(reviewer_email,paper_number)
else:
    reviewer_email = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    if not assign_reviewer(reviewer_email,paper_number):
        print("Invalid input. Need csv file or '<email_address>,<paper#>'")

client.post_group(reviewers)