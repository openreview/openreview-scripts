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



def sendMail(reviewers_invited):
    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    for count, reviewer in enumerate(reviewers_invited):
        print "Sending message to "+reviewer
        hashkey = openreview.get_hash(reviewer, "4813408173804203984")
        url = openreview.baseurl+"/invitation?id=ICLR.cc/2017/conference/-/reviewer_invitation&email=" + reviewer + "&key=" + hashkey + "&response="
        message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
        message = message+ "To ACCEPT the invitation, please click on the following link: \n\n"
        message = message+ url + "Yes\n\n"
        message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
        message = message+ url + "No\n\n" + "Thank you"

        openreview.send_mail("OpenReview invitation response", [reviewer], message)

reviewers_invited = openreview.get_group("ICLR.cc/2017/conference/reviewers-invited")

if type(reviewers_invited)==Group:
    sendMail(reviewers_invited.members)