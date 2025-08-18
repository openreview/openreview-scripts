#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

## Import statements
from __future__ import print_function
import argparse
import csv
import sys
import re
import openreview
import config

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="a csv file containing the email addresses of the reviewers")
parser.add_argument('-e', '--email', metavar='N', type=str, nargs='+', help="emails separated by space")
parser.add_argument('-g', '--group', help='send this message to all members of the given group')
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

subject = "Reviewing Committee for ICLR 2018 Workshop Track (opt-out)"

message = """Dear Reviewer,

Thank you for your help thus far in reviewing for the main ICLR conference. We are writing to inform you that the Workshop Track review process for ICLR will begin on February 12th. Workshop papers include late-breaking developments, very novel ideas and position papers. The focus of the Workshop Track is to stimulate discussion of new ideas and directions.

The review process for Workshop Track abstracts will be much lighter than for regular Conference Track submissions. Submissions are shorter (2-3 page abstract) compared to regular ICLR submissions. The review process consists of just a short review submitted by the reviewer, with optional discussion at the reviewer’s and authors’ discretion. We are planning to keep the load very low.

Here’s a tentative timeline for the ICLR Workshop Track review process:

February 12: workshop author submission deadline
March 10: full review deadline

The success of ICLR depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. If you are not able to review for the Workshop Track, please click on the link below. Otherwise, a few Workshop Track reviews will be assigned to you in your OpenReview account a few days after the February 12th deadline. Also, if you have a chance, ensure that the conflicts of interests of your OpenReview account are up to date, and your institutional email address is in your profile: https://openreview.net/profile?mode=edit

If you are NOT available to participate in the workshop reviewing process, please click on the following link:

{0}

If you have any question, please contact the program chairs at iclr2018.programchairs@gmail.com .

Thank you for helping us make ICLR 2018 a success!

Cheers!
Tara, Oriol, Iain and Marc’Aurelio - ICLR 2018 program chairs


"""

def sendMail(user):
    invitation = config.RECRUIT_REVIEWERS

    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    hashkey = client.get_hash(user, "2810398440804348173")
    url = client.baseurl + "/invitation?id=" + invitation + "&username=" + user + "&key=" + hashkey + "&response="
    response = client.send_mail(subject, [user], message.format(url + "No"))
    print("Mail response: ", response)

if client.exists(config.REVIEWERS_INVITED) and client.exists(config.REVIEWERS_EMAILED):

    reviewers_invited = client.get_group(config.REVIEWERS_INVITED)
    reviewers_emailed = client.get_group(config.REVIEWERS_EMAILED)

    if args.file:
        with open(args.file, 'rb') as csvfile:
            # This assumes a csv file with rows formatted as follows:
            # email_address,~tilde_name1
            reviewer_list = [row[0] for row in csv.reader(csvfile)]

    if args.email:
        reviewer_list = args.email

    if args.group:
        recipient_group = client.get_group(args.group)
        reviewer_list = recipient_group.members

    for reviewer in reviewer_list:
        reviewer = reviewer.encode('utf-8')
        print('reviewer:', reviewer)
        client.add_members_to_group(reviewers_invited, reviewer)

        if reviewer not in reviewers_emailed.members:
            sendMail(reviewer)
            client.add_members_to_group(reviewers_emailed, reviewer)
        else:
            print("{0} found in {1}".format(reviewer, config.REVIEWERS_EMAILED))

else:
    print("Error while retrieving groups")
    print(config.REVIEWERS_INVITED, "exists:", client.exists(config.REVIEWERS_INVITED))
    print(config.REVIEWERS_EMAILED, "exists:", client.exists(config.REVIEWERS_EMAILED))


