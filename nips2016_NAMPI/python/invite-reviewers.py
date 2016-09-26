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
parser.add_argument('-r','--reviewers', help="a csv file containing the list of reviewers with rows in the following format: 'firstname,lastname,emailaddress'")
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

Dear %s %s,

We would like to invite you to serve on the Program Committee for the Neural Abstract Machines & Program Induction (NAMPI) workshop at NIPS 2016. The workshop will broadly focus on neural approaches to computation, program induction, algorithm learning, abstract machines and data structures, and their relation to established learning and non-learning methods in the field. More details can be found here: https://uclmr.github.io/nampi/

The NAMPI workshop will be held in Barcelona, Spain on December 10th, 2016.

The Program Committee will review up to 4-page (not including references) submissions, and will consist of experts in various fields of interest for the workshop. Realising your busy schedule, we will try to keep the load as low as possible.

We would be grateful if you could confirm your acceptance or refusal of the participation in the NAMPI committee clicking on one of the links below.

To ACCEPT the invitation, please click on the link below:
%s

To DECLINE the invitation, please click on the link below:
%s

(Rough) Workshop deadlines:
Paper submission: October 14th
Possible extension: October 21st
Notification of acceptance: November 13th
Final Papers Due: December 1st
Deadlines are at 11:59pm PDT.

NAMPI will be organized as a single-blind review with open comments on OpenReview.net.

In case you accept the invitation, we will soon send you further instructions on how to proceed with the reviewing duties.

Please confirm your participation as soon as possible. We know that we will make NAMPI a big success with your help.



Kind regards,
Arvind, Matko, Nando, Scott, Sebastian, Tejas, Tim


"""

def update_group_members(groupid,assignment):
    new_members = []
    group = openreview.get_group(groupid)
    reviewers = []

    if type(group)==Group:

        if assignment.endswith('.csv'):
            with open(assignment, 'rb') as assignment:
                reader = csv.reader(assignment, delimiter=',', quotechar='|')
                for row in reader:
                    reviewer = {'firstname':row[0],'lastname':row[1],'email':row[2]}
                    new_members.append(reviewer['email'])
                    reviewers.append(reviewer)
        else:
            print "Invalid input: ",assignment
            sys.exit()

        print "updating group ",groupid
        group.members += new_members
    else:
        print "could not find group ",groupid

    return group,reviewers


def sendMail(reviewers):
    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    for reviewer in reviewers:
        
        firstname = reviewer['firstname']
        lastname = reviewer['lastname']
        email = reviewer['email']

        print "Sending message to "+email

        hashkey = openreview.get_hash(reviewer['email'], "4813408173804203984")
        url = openreview.baseurl+"/invitation?id=NIPS.cc/2016/workshop/NAMPI/-/reviewer_invitation&email=" + email + "&key=" + hashkey + "&response="


        openreview.send_mail("Reviewer Invitation for NIPS 2016 Workshop: NAMPI", [email], message %(firstname, lastname, url + "Yes", url + "No"))




if args.reviewers!=None:
    reviewers_invited,reviewers = update_group_members('NIPS.cc/2016/workshop/NAMPI/reviewers-invited',args.reviewers)
    if type(reviewers_invited)==Group:
        openreview.post_group(reviewers_invited)

    reviewers_emailed = openreview.get_group("NIPS.cc/2016/workshop/NAMPI/reviewers-emailed")

    if type(reviewers_emailed)==Group:
        recipients = [reviewer for reviewer in reviewers if reviewer['email'] not in reviewers_emailed.members]
        recipient_emails = [reviewer['email'] for reviewer in reviewers if reviewer['email'] not in reviewers_emailed.members]
        sendMail(recipients)
        reviewers_emailed.members = reviewers_emailed.members+recipient_emails
        openreview.post_group(reviewers_emailed)
    else:
        print "Error while retrieving NIPS.cc/2016/workshop/NAMPI/reviewers-invited; group may not exist"



