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

subject_line = "MIDL Submission decision"
message = {}
message['Reject']='''Dear Author,

put text here
Sincerely,
Program Chairs for MIDL 2019.'''


message['Accept'] = '''Dear Author,

put text here

Sincerely,
Program Chairs for MIDL 2019
'''


iterator = client.get_notes(invitation='MIDL.io/2020/Conference/-/Blind_Submission')
submissions = {}
for paper in iterator:
    submissions[paper.number]=paper


def post_decision(paper_num, decision, add_text):
    if (decision == "Reject") or (decision == "Accept"):
        paper = submissions[int(paper_num)]

        # post decision note as Accept or Reject
        paperinv = 'MIDL.io/2020/Conference/-/Blind_Submission/-/Paper' + paper_num + '/Decision'
        decision_note= openreview.Note(
            invitation= paperinv,
            forum= submissions[int(paper_num)].id,
            signatures= ['MIDL.io/2020/Conference/Program_Chairs'],
            writers= ['MIDL.io/2020/Conference'],
            readers= ['everyone'],
            content= {
                'title':'Decision',
                'decision':decision
            }
        )
        client.post_note(decision_note)

        print("Post note: "+paper_num+decision)

        client.post_message(subject_line, paper.content['authorids'],
                            message[decision])

    else:
        print("Decision invalid: <"+decision+">")

##################################################################



if args.assignments.endswith('.csv'):
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # skip header row
        next(reader,None)
        for row in reader:
            paper_number = row[1]
            if len(row) >= 13:
                decision = row[12]
            if len(row) >= 14:
                add_text = row[13]
            else:
                add_text = ""
            post_decision(paper_number, decision, add_text)
