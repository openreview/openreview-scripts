#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import config
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--group', help="group whose members will receive the email")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
	client = Client(baseurl=args.baseurl)

#################################################
#                                               #
#   EDIT YOUR MESSAGE AND SUBJECT LINE BELOW    #
#                                               #
#################################################


subjectline = "NIPS 2017: MLITS Workshop paper review assignment"
def reviewer_email_message(paper_id):
    message = """Dear Reviewer,

    The linked paper https://openreview.net/pdf?id={0} has been submitted for possible presentation at our upcoming workshop (https://nips.cc/Conferences/2017/Schedule?showEvent=8755). We would greatly appreciate your help in evaluating the submission by November 10th.

    Reviewer instructions:
    - Please confirm to organizing committee member erranlli@gmail.com that you received this email.
    - To submit a review, log into https://openreview.net. Select \"Tasks\" under the dropdown menu under your name.  Select a paper that you've been assigned to review and press the Official Review button.'
    - Please complete the review by the indicated deadline using the online submission and review system.

    Thank you for your help on evaluating this paper. The success of our workshop is to a large extent due to the efforts of our committee members.

    Sincerely, the organizing committee,

    Li Erran Li
    Anca Dragan
    Juan Carlos Niebles
    Silvio Savarese""".format(paper_id)
    return message

#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################


## send email to each reviewer
notes = client.get_notes(invitation=config.SUBMISSION)
for note in notes:
    print note.number
    paper_number = str(note.number)
    group_id = config.CONF + '/Paper' + paper_number+"/Reviewers"
    anon_group = client.get_group(group_id)
    msg = reviewer_email_message(note.id)
    for anon in anon_group.members:
        reviewers = client.get_group(anon)
        for reviewer in reviewers.members:
            if reviewer.find('@')!=-1:
                email_addr = reviewer
            else:
                profile = client.get_profile(reviewer)
                email_addr = profile.content['preferred_email']
                print "Email from profile is:"+email_addr

            response = client.send_mail(subjectline, [email_addr], msg)