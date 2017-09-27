#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

## Import statements
import argparse
import csv
import sys
import re
import openreview
import config

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('file', help="a csv file containing the email addresses of the reviewers")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


message = """

Dear Reviewer,

We are writing to invite you to be a reviewer for the 6th International Conference on Learning Representations (ICLR 2018); see call for papers at: www.iclr.cc. As a recognized researcher by the ICLR community, we hope you can contribute to the review process of ICLR 2018.

The reviewing period will start around October 27th for conference submissions. A tentative timeline for the ICLR reviewing process is:

Oct 27: conference submission deadline
Nov 27: full review deadline
Nov 27 - Jan 5: rebuttal and discussion period
Jan 5 - Jan 12: discussion among reviewers and area chairs
Jan 29: final decisions for conference papers sent to authors

Please, make sure you are available during the review and discussion period before accepting.

This year, the review process will not include a pre-review question period like last year. Instead, reviewers will submit a full review, followed by a rebuttal and discussion period. We will be using OpenReview throughout the review process, which we hope will make the review process more engaging and allow us to more effectively leverage the whole ICLR community.

The success of ICLR depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you can accept our invitation and help make ICLR thrive.

To ACCEPT the invitation, please click on the following link:

{0}

To DECLINE the invitation, please click on the following link:

{1}

We'd appreciate an answer within 10 days.

If you accept, please make sure to either update your Toronto Paper Matching System (TPMS) account, or create one if you do not have one already: http://torontopapermatching.org/webapp/profileBrowser/login/. We will be using TPMS to assign reviewers to papers, and having an account that reflects your expertise will be crucial for you to receive papers for which you are suited. Also please make sure your OpenReview account lists the email you are using for your TPMS account.

If you have any question, please contact the program chairs at iclr2018.programchairs@gmail.com .

We are looking forward to your reply, and are grateful if you accept this invitation and help make ICLR 2018 a success!

Cheers!

Tara Sainath, Senior Program Chair
Iain Murray, Program Chair
Marc’Aurelio Ranzato, Program Chair
Oriol Vinyals, Program Chair
Hugo Larochelle, Steering Committee
Aaron Courville, Steering Committee
Yoshua Bengio, General Chair
Yann Lecun, General Chair



"""

def sendMail(user):
    invitation = config.RECRUIT_REVIEWERS

    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    hashkey = client.get_hash(user.encode('utf-8'), "2810398440804348173")
    url = client.baseurl + "/invitation?id=" + invitation + "&username=" + user + "&key=" + hashkey + "&response="
    response = client.send_mail("Reviewing Committee Invitation for ICLR 2018", [user], message.format(url + "Yes", url + "No"))
    print "Mail response: ", response

if client.exists(config.REVIEWERS_INVITED) and client.exists(config.REVIEWERS_EMAILED):

    reviewers_invited = client.get_group(config.REVIEWERS_INVITED)
    reviewers_emailed = client.get_group(config.REVIEWERS_EMAILED)

    with open(args.file, 'rb') as csvfile:
        for row in csv.reader(csvfile):
            # This assumes a csv file with rows formatted as follows:
            # email_address,~tilde_name1
            reviewer = row[0]
            print 'reviewer:', reviewer
            client.add_members_to_group(reviewers_invited, reviewer)

            if reviewer not in reviewers_emailed.members:
                sendMail(reviewer)
                client.add_members_to_group(reviewers_emailed, reviewer)

else:
    print "Error while retrieving groups"
    print config.REVIEWERS_INVITED, "exists:", client.exists(config.REVIEWERS_INVITED)
    print config.REVIEWERS_EMAILED, "exists:", client.exists(config.REVIEWERS_EMAILED)


