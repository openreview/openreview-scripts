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
Email first line

Email second line

To ACCEPT the invitation, please click on the following link:

%s

To DECLINE the invitation, please click on the following link:

%s

Here's a timeline
X
Y
Z

Sincerely,
UAI Program Chairs

"""

def sendMail(spc_invited):
    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    for count, spc_member in enumerate(spc_invited):
        print "Sending message to "+reviewer
        hashkey = openreview.get_hash(reviewer, "2810398440804348173")
        url = openreview.baseurl+"/invitation?id=UAI.org/2017/conference/-/spc_invitation&email=" + reviewer + "&key=" + hashkey + "&response="

        openreview.send_mail("[UAI2017] Invitation to serve on the Sr. Program Committee", [reviewer], message %(url + "Yes", url + "No"))


if openreview.exists("UAI.org/2017/conference/SrProgramCommittee/invited") and openreview.exists("UAI.org/2017/conference/SrProgramCommittee/emailed"):
    reviewers_invited = openreview.get_group("UAI.org/2017/conference/SrProgramCommittee/invited")
    reviewers_emailed = openreview.get_group("UAI.org/2017/conference/SrProgramCommittee/emailed")
    recipients = [reviewer for reviewer in reviewers_invited.members if reviewer not in reviewers_emailed.members]
    sendMail(recipients)
    reviewers_emailed.members = reviewers_emailed.members+recipients
    openreview.post_group(reviewers_emailed)
else:
    print "Error while retrieving UAI.org/2017/conference/reviewers-invited; group may not exist"


