#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Email decisions to paper authors
"""

## Import statements
import argparse
import csv
import openreview

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ifile')
args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

def load_decisions(client):
    decisions = client.get_notes(invitation='ICLR.cc/2018/Workshop/-/Acceptance_Decision')
    print len(decisions)
    dec_info = {}
    for decision in decisions:
        dec_info[decision.forum] =decision.content['decision']
    return dec_info

def load_file():
    csv_info = []
    if args.ifile:
        with open(args.ifile) as f:
            reader = csv.reader(f)
            csv_info = [r[0] for r in reader]
    return csv_info



subjects = {}
subjects['Accept'] = "ICLR 2018 Workshop track: final decision - poster"
subjects['Reject'] = "ICLR 2018 Workshop track: final decision - rejection"

messages = {}
messages['Accept'] = """Dear Author,

We are pleased to inform you that your ICLR 2018 submission to the Workshop Track
{0} - {1}
has been accepted to the Workshop Track as a poster presentation.

Please don't forget to make your travel arrangements if you haven’t already. Information about the conference is at https://iclr.cc/ -- please use the contact form there for questions about registration or logistics.

At least one author for each poster must be registered for ICLR 2018.

We received 346 Workshop Track submissions! Out of these we accepted 196 workshop submissions for poster presentation in the Workshop Track (57%).

Congratulations and thank you for your contribution.

We look forward to seeing you in Vancouver, Canada!

Tara, Marc’Aurelio, Iain and Oriol -- the ICLR 2018 program committee

"""

messages['Reject'] = """Dear Author,

We are writing to inform you that your ICLR 2018 Workshop Track submission
{0} - {1}
was not accepted.

We received 346 Workshop Track submissions, around double last year. Out of these we could only accept around half as posters at the meeting. However, if you wish, please feel free to continue to discuss the paper, and post any updates on OpenReview.

Thank you for your interest in the conference, and we hope you'll nevertheless consider joining us in Vancouver, Canada.

Tara, Marc’Aurelio, Iain and Oriol -- the ICLR 2018 program committee

"""


submissions = client.get_notes(invitation='ICLR.cc/2018/Workshop/-/Submission')
decision_info = load_decisions(client)
# csv_info is a list of forums where the email was already sent
# in case script doesn't finish in one go
csv_info = load_file()
subject = "ICLR decision"
for note in submissions:
    if note.forum in decision_info and note.forum not in csv_info:
        if decision_info[note.forum] in messages:
            message = messages[decision_info[note.forum]].format(note.number, note.content['title'].encode('utf-8'))
            client.send_mail(subjects[decision_info[note.forum]], note.content['authorids'], message)
            #print "{0}, {1}".format(note.number,decision_info[note.forum])
            print note.forum
        else:
            print "ERROR Decision: <" + {0} + "> for paper {1}".format(decision_info[note.forum], note.number)