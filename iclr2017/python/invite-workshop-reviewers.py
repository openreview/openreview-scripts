#!/usr/bin/python

"""

"""

## Import statements
import argparse
import csv
import sys
import openreview

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


message = """
Dear Reviewer,

Thank you for your help thus far in reviewing for the main ICLR conference. We are writing to inform you that the Workshop Track review process for ICLR will begin on February 17th. Workshop papers include late-breaking developments, very novel ideas and position papers. The focus of the Workshop Track is to stimulate discussion of new ideas and directions.

The review process for Workshop Track abstracts will be much lighter than for regular Conference Track submissions. Submissions are shorter (2-3 page abstract) compared to regular ICLR submissions. The review process consists of just a short review submitted by the reviewer, with optional discussion at the reviewer's and authors' discretion. We are planning to keep the load low and assign at most 4 abstracts per reviewer.

Here's a tentative timeline for the ICLR Workshop Track review process:

February 17: workshop author submission deadline
March 10: full review deadline

The success of ICLR depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers.

If you are *NOT* able to review for the Workshop Track, please click on the link below:

%s

Otherwise, a few Workshop Track reviews will be assigned to you in your OpenReview account a few days after the February 17th deadline.

If you have any question, please contact the program chairs at iclr2017.programchairs@gmail.com .

Thank you for helping us make ICLR 2017 a success!

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
        hashkey = client.get_hash(reviewer, "4813408173804203984")
        url = client.baseurl+"/invitation?id=ICLR.cc/2017/workshop/-/reviewer_invitation&email=" + reviewer + "&key=" + hashkey + "&response="

        client.send_mail("Reviewer Invitation for ICLR 2017: Workshop Track", [reviewer], message % (url+"No"))


if client.exists("ICLR.cc/2017/conference/reviewers") and client.exists("ICLR.cc/2017/workshop/reviewers-emailed"):
    conference_reviewers = client.get_group("ICLR.cc/2017/conference/reviewers")
    workshop_reviewers_emailed = client.get_group("ICLR.cc/2017/workshop/reviewers-emailed")
    recipients = [reviewer for reviewer in conference_reviewers.members if reviewer not in workshop_reviewers_emailed.members]
    sendMail(recipients)
    client.add_members_to_group(workshop_reviewers_emailed,recipients)
else:
    print "Error while retrieving the groups. \nICLR.cc/2017/conference/reviewers exists? %s\nICLR.cc/2017/workshop/reviewers-emailed exists? %s" % (client.exists("ICLR.cc/2017/conference/reviewers"), client.exists("ICLR.cc/2017/workshop/reviewers-emailed"))


