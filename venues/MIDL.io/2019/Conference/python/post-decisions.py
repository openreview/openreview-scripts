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

iterator = client.get_notes(invitation=conference.get_submission_id())
submissions = {}
for paper in iterator:
    submissions[paper.number]=paper

def create_decision_invite():
    ## Decision

    for key in submissions.keys():
        paperinv = conference.get_id() + '/-/Paper' + str(key) + '/Decision'

        decision_reply = {
            'forum': submissions[key].id,
            'replyto': submissions[key].id,
            'writers': {'values': [conference.get_id()]},
            'signatures': {'values': [conference.get_program_chairs_id()]},
            'readers': {
                'values': ['everyone'],
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {
                'title': {
                    'order': 1,
                    'value': 'Acceptance Decision'
                },
                'decision': {
                    'order': 2,
                    'value-radio': [
                        'Accept',
                        'Reject'
                    ],
                    'required': True
                },
                'presentation': {
                    'order': 3,
                    'value-radio': [
                        'Oral',
                        'Poster',
                    ],
                    'required': False
                }
            }
        }

        decision_parameters = {
            'readers': ['everyone'],
            'writers': [conference.get_id()],
            'signatures': [conference.get_id()],
            'duedate': tools.timestamp_GMT(2019, month=2, day= 22, hour=23, minute=59),
            'invitees': [conference.get_program_chairs_id()],
            'reply': decision_reply
        }

        invite = openreview.Invitation(paperinv, **decision_parameters)
        client.post_invitation(invite)

def remove_if_rejected(paper_num, decision):
    if int(paper_num) not in submissions.keys():
        # already removed
        return True
    else:
        paper = submissions[int(paper_num)]
        if decision == "Reject" and paper.content.get('remove if rejected', False):
            # this is actually the time now here as though it were GMT so it's off by 5 hours.
            paper.ddate = tools.datetime_millis(datetime.datetime.now())
            client.post_note(paper)
            print("Remove note: " + paper_num)
            return True
    return False

def post_decision(paper_num, decision):
    if (decision == "Reject") or (decision == "Accept"):
        paperinv = conference.get_id() + '/-/Paper' + paper_num + '/Decision'
        decision_note= openreview.Note(
            invitation= paperinv,
            forum= submissions[int(paper_num)].id,
            signatures= [conference.get_program_chairs_id()],
            writers= [conference.get_id()],
            readers= ['everyone'],
            content= {'title':'Acceptance Decision',
                      'decision':decision}
        )
        client.post_note(decision_note)
        print("Post note: "+paper_num)
    elif decision:
        print("Decision invalid: <"+decision+">")

##################################################################

create_decision_invite()
if args.assignments.endswith('.csv'):
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # skip header row
        next(reader,None)
        for row in reader:
            paper_number = row[1]
            if len(row) >= 12:
                decision = row[11]
                if not remove_if_rejected(paper_number,decision):
                    post_decision(paper_number, decision)
else:
    paper_number = args.assignments.split(',')[1]
    decision = args.assignments.split(',')[0]
    if not remove_if_rejected(paper_number, decision):
        post_decision(paper_number, decision)
