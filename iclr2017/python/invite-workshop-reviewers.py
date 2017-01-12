#!/usr/bin/python

"""

"""

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)


message = """
WORKSHOP INVITATION TEXT

To ACCEPT the invitation, please click on the following link:

%s

To DECLINE the invitation, please click on the following link:

%s

We'd appreciate an answer within 10 days.

If you accept, please make sure to either update your Toronto Paper Matching System (TPMS) account, or create one if you do not have one already. We will be using TPMS to assign reviewers to papers, and having an account that reflects your expertise will be crucial for you to receive papers for which you are suited. Also please make sure your OpenReview account lists the email you are using for your TPMS account.

Here's a tentative timeline for the ICLR reviewing process:

TIMELINE

If you have any question, please contact the program chairs at iclr2017.programchairs@gmail.com .

We are looking forward to your reply, and are grateful if you accept this invitation and help make ICLR 2017 a success!

Cheers!

Marc'Aurelio Ranzato, Senior Program Chair
Hugo Larochelle, Program Chair
Tara Sainath, Program Chair
Oriol Vinyals, Program Chair
Yoshua Bengio, General Chair
Yann Lecun, General Chair

"""

def sendMail(reviewers_invited):
    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    for count, reviewer in enumerate(reviewers_invited):
        print "Sending message to "+reviewer
        hashkey = openreview.get_hash(reviewer, "4813408173804203984")
        url = openreview.baseurl+"/invitation?id=ICLR.cc/2017/workshop/-/reviewer_invitation&email=" + reviewer + "&key=" + hashkey + "&response="

        openreview.send_mail("Reviewer Invitation for ICLR 2017", [reviewer], message %(url + "Yes", url + "No"))


if openreview.exists("ICLR.cc/2017/conference/reviewers") and openreview.exists("ICLR.cc/2017/workshop/reviewers-emailed"):
    reviewers = openreview.get_group("ICLR.cc/2017/conference/reviewers")
    reviewers_emailed = openreview.get_group("ICLR.cc/2017/workshop/reviewers-emailed")
    recipients = [reviewer for reviewer in reviewers.members if reviewer not in reviewers_emailed.members]
    sendMail(recipients)
    reviewers_emailed.members = reviewers_emailed.members+recipients
    openreview.post_group(reviewers_emailed)
else:
    print "Error while retrieving ICLR.cc/2017/workshop/reviewers-invited; group may not exist"


