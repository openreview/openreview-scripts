#!/usr/bin/python

###############################################################################
''' Assigns reviewers to papers - run in same directory as config.py
 ex. python assign-reviewers.py --baseurl http://localhost:3000
       --username admin --password admin_pw 'reviewer@gmail.com,3'

 Checks paper number valid.
 Check reviewer email address or domain is not on the conflicts list.
 Check reviewer is in the system.
 If reviewer is not in conference reviewers group (config.CONF/Reviewers), add it.
 If reviewer not already assigned to this paper:
	Determine AnonReviewer number
	Create Paper#/AnonReviewer#  group with this reviewer as a member
    Assign Paper#/AnonReviewer# to the Paper#/Reviewers group and
                                Paper#/Reviewers/NonReaders group for this paper'''
###############################################################################

## Import statements
import argparse
import csv
import config
from openreview import *
from openreview import tools


## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'reviewer@cs.umass.edu,23'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.SUBMISSION)

## checks for valid paper numbers and email addresses
def check_arguments(email_addr, paper_number):
    try:
        int(paper_number)
    except ValueError:
        print "Error: Paper number \"" + paper_number + "\" invalid."
        return False

    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')
    if not valid_email.match(email_addr):
        print "Error: Reviewer \""+email_addr+"\" invalid. Please check for typos and whitespace."
        return False

    return True

# check if reviewer_email or reviewer's domains are on conflict list
def reviewer_conflicts(reviewer_email, paper_number, conflict_list):
    # check reviewer email as a whole is on the conflicts list
    if reviewer_email in conflict_list:
        print "Error: Reviewer \"" + reviewer_email + "\" is an author for Paper" + paper_number
        return True

    # if the reviewer email ends w/ .edu check it is on conflicts list
    name, domain = reviewer_email.split('@')
    if domain.endswith('.edu') and domain in conflict_list:
        print "Error: Reviewer \"" + reviewer_email + "\" email has conflicts for Paper" + paper_number
        return True

    return False

# does some parameter checking, checks for conflicts
# check if reviewer already assigned to paper
# if not then create Anonymous group for the reviewer and add to reviewer group
def assign_reviewer(reviewer_email, paper_number):
    if not check_arguments(reviewer_email, paper_number):
        return False

    # check paper_number exists
    notes = [note for note in submissions if str(note.number) == paper_number]
    if not notes:
        print "Error: Paper number " + paper_number + " does not exist"
        return True
    note = notes[0]

    # create list of conflicts emails and add paper author to it
    # conflict_list is a copy (not a reference) to the submission conflicts
    conflict_list = []
    # If conflicts are a part of a submission, add them here
    if 'conflicts' in note.content:
        conflict_list.extend(note.content['conflicts'][:])
    # authors for this paper are not allowed to be in the reviewers groups
    if 'authorids' in note.content:
        conflict_list += note.content['authorids']

    if reviewer_conflicts(reviewer_email, paper_number, conflict_list):
        return True

    reviewer_id = tools.get_profile(client, reviewer_email)
    if reviewer_id is None:
        reviewer_id = reviewer_email
    else:
        reviewer_id = reviewer_id.id
    tools.assign(client, paper_number, config.CONFERENCE_ID, reviewer_to_add = reviewer_id)
    ## reviewers are blocked from other reviews until complete
    paper_group = config.CONFERENCE_ID + '/Paper' + paper_number
    client.add_members_to_group(client.get_group(paper_group + '/Reviewers/NonReaders'), reviewer_id)
    return True

##################################################################


if args.assignments.endswith('.csv'):   
    with open(args.assignments, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            reviewer_email = row[0]
            paper_number = row[1]
            assign_reviewer(reviewer_email,paper_number)
else:
    reviewer_email = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    if not assign_reviewer(reviewer_email,paper_number):
        print "Invalid input. Need csv file or '<email_address>,<paper#>'"
