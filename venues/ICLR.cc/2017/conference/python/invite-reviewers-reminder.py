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
We are writing to invite you to be a reviewer for the 5th International Conference on Learning Representations (ICLR 2017); see call for papers at: www.iclr.cc. As a recognized researcher by the ICLR community, we hope you can contribute to the review process of ICLR 2017.

Our plan is to keep the reviewing load low and assign at most 4 papers to each reviewer.  The reviewing period will start around November 4th for conference submissions. Workshop submissions on the other hand will only be received in early 2017 and reviewed a few months before the conference. 

This year, the review process will include an earlier deadline for reviewers to submit short questions to authors, ahead of having to submit a complete and rated evaluation. This step was suggested during the ICLR 2016 town hall meeting, as an attempt to prevent reviewers from cementing their appreciation of a paper before having all of the information needed. Reviewers will then submit a full review, followed by a rebuttal and discussion period, as usual. We will be using OpenReview throughout the review process, which we hope will make the review process more engaging and allow us to more effectively leverage the whole ICLR community.

The success of ICLR depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you can accept our invitation and help make ICLR thrive. 

To ACCEPT the invitation, please click on the following link:

%s

To DECLINE the invitation, please click on the following link:

%s

We'd appreciate an answer within 10 days.

If you accept, please make sure to either update your Toronto Paper Matching System (TPMS) account, or create one if you do not have one already. We will be using TPMS to assign reviewers to papers, and having an account that reflects your expertise will be crucial for you to receive papers for which you are suited. Also please make sure your OpenReview account lists the email you are using for your TPMS account.

Here's a tentative timeline for the ICLR reviewing process:

Aug: reviewer recruitment
Nov 4: conference submission deadline
Dec 2: pre-review questions deadline 
Dec 16: full review deadline
Dec 17-Jan 20: rebuttal and discussion period
Jan 20-Jan 27: area chairs finalize their decisions
Feb 3: final decisions for conference papers sent to authors

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
        url = openreview.baseurl+"/invitation?id=ICLR.cc/2017/conference/-/reviewer_invitation&email=" + reviewer + "&key=" + hashkey + "&response="

        openreview.send_mail("Reminder: Reviewer Invitation for ICLR 2017", [reviewer], message %(url + "Yes", url + "No"))

reviewers_invited = openreview.get_group("ICLR.cc/2017/conference/reviewers-invited").members
reviewers_accepted = openreview.get_group("ICLR.cc/2017/conference/reviewers").members
reviewers_declined = openreview.get_group("ICLR.cc/2017/conference/reviewers-declined").members

recipients = []
for r in reviewers_invited:
    if(r not in reviewers_accepted and r not in reviewers_declined):
        print "Send reminder to: ", r
        recipients.append(r)

print "send mails to", len(recipients), " reviewers"
#sendMail(recipients)



