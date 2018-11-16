#!/usr/bin/python

###############################################################################
''' Assigns reviewers to papers - run in same directory as config.py
 ex. python assign-reviewers.py --baseurl http://localhost:3000
       --username admin --password admin_pw 'reviewer@gmail.com,3'

 Checks paper number is an integer.
 Check reviewer email address or domain is not on the conflicts list.
 Check reviewer is in the system.
 If reviewer is not in conference reviewers group (config.CONF/Reviewers), add it.
 If reviewer not already assigned to this paper:
	Determine AnonReviewer number
	Create Paper#/AnonReviewer#  group with this reviewer as a member
    Assign Paper#/AnonReviewer# to the Paper#/Reviewers group for this paper'''
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

submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
print(client.baseurl)
def assign_decision(decision, paper_number):

    # check paper_number exists
    notes = [note for note in submissions if str(note.number) == paper_number]
    if not notes:
        print("Error: Paper number " + paper_number + " does not exist")
        return True
    note = notes[0]

    decision_note= openreview.Note(
        forum= note.id,
        replyto=note.id,
        invitation= config.CONFERENCE_ID + '/-/Paper' + str(note.number) + '/Decision',
        signatures= [config.CONFERENCE_ID],
        writers= [config.CONFERENCE_ID],
        readers= ['everyone'],
        content= {"title": "Acceptance Decision", "decision":decision}
    )
    client.post_note(decision_note)
    print(note.id+" "+note.content['title'])
    return True

##################################################################


if args.assignments.endswith('.csv'):   
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            paper_number = row[0]
            #decision = row[1]
            assign_decision("accept",paper_number)
else:
    decision = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    if not assign_decision(decision,paper_number):
        print("Invalid input. Need csv file or '<email_address>,<paper#>'")
