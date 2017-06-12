import openreview
from uaidata import *
import csv
import argparse

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')

def read_decisions(filename):
    with open(filename) as f:
        csvreader = csv.reader(f)
        decisions = [int(row[0].replace('Paper','')) for row in csvreader]
    return decisions

oral = read_decisions('../data/oral.csv')
poster = read_decisions('../data/poster.csv')
reject = read_decisions('../data/reject.csv')

for n in submissions:
    print "posting decision for Paper%s" % str(n.number)
    decision_invitation = client.get_invitation(CONFERENCE + '/-/Paper' + str(n.number) + '/Acceptance/Decision')
    decision = None
    if n.number in oral:
        decision = 'Accept (Oral)'
    if n.number in poster:
        decision = 'Accept (Poster)'
    if n.number in reject:
        decision = 'Reject'

    if decision != None:
        client.post_note(openreview.Note(
                forum=n.forum,
                replyto=n.forum,
                readers=['~UAI_Admin1', COCHAIRS],
                writers=['~UAI_Admin1', COCHAIRS],
                signatures=['~UAI_Admin1'],
                invitation=decision_invitation.id,
                content={
                    'title': 'Paper%s Acceptance Decision' % str(n.number),
                    'decision': decision
                        }

            ))
    else:
        print "Paper%s not found." % str(n.number)


