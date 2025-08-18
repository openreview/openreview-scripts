#!/usr/bin/python

###############################################################################
# Add oral/poster to decisions
###############################################################################

## Import statements
import argparse
import csv
import config
import datetime
from openreview import *
from openreview import tools



## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing submission decisions or (2) a string of the format '<paper#>,<decision>' e.g. '23,Reject'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connecting to "+client.baseurl)
conference = config.get_conference(client)

all_decisions = client.get_notes(invitation=conference.get_id() + '/-/Paper.*/Decision')
decisions = {}
for note in all_decisions:
    paper_num = note.invitation.split('/Paper')[1].split('/')[0]
    decisions[paper_num] = note

##############################################################################

def add_oral_poster_to_decision(paper_num, presentation):
    print(paper_num)
    decision = decisions[paper_num]
    if decision.content['decision'] == 'Accept':
        decision.content['presentation'] = presentation
        client.post_note(decision)
    else:
        print(decision.content)

##################################################################
if args.assignments.endswith('.csv'):
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # skip header row
        next(reader,None)
        for row in reader:
            paper_number = row[1]
            presentation = row[14]
            if presentation:
                add_oral_poster_to_decision(paper_number, presentation)
else:
    paper_number = args.assignments.split(',')[1]
    accept_type = args.assignments.split(',')[0]
    add_oral_poster_to_decision(paper_number, accept_type)
