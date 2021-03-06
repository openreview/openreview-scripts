#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import config
import csv

from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="a csv file containing reviewer assignments ")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
	client = Client(baseurl=args.baseurl)

print(client.baseurl)
#################################################
#                                               #
#   EDIT YOUR MESSAGE AND SUBJECT LINE BELOW    #
#                                               #
#################################################


subjectline = "Title: NIPS'18 Spatiotemporal workshop - review reminder (second round)"
def reviewer_email_message():
    message = """Dear Reviewer,

We are organizing a workshop on Modeling and Decision-Making in the Spatiotemporal Domain at the Thirty-second Conference on Neural Information Processing Systems (NIPS), December 07, 2018, Montreal, Canada. Considering your expertise in the area, we would like to seek your assistance in the review process. We would highly appreciate if you could provide the reviews for the assigned manuscripts before 11.59 pm on October 19, 2018 AOE.

Rating (only visible to the program chairs):
    Please rate the paper (very high, high, borderline, low, very low) on:
    1. Relevance to the workshop
    2. Novelty
    3. Potential impact

Overall evaluation (visible to the authors and public):
    Please write a few sentences summarizing the paper and its main contributions, then your overall evaluation of the paper. As the submitted manuscripts are for a workshop, please be aware that most of them are based on the work under progress.  Try to include comments about the positive aspects of the paper as well as advice about how the paper could be improved—we hope for the review process to be beneficial for authors!

Specific questions (please provide short answers):
    1. What did you learn from reading this paper that you did not know before?
    2. What was the most exciting part of the work?
    3. What in your opinion makes this work stand apart from other papers in this area?
    4. Does the paper fit into the scope of the workshop?
    5. Are you aware of relevant literature that you may want to make the authors aware of?


Reviewer instructions:
    To submit a review, log into https://openreview.net. Select \"Tasks\" from the top menubar.  Select \"Show pending tasks\", then select a task to see the paper and the review form.

Please note that your reviews under overall evaluation will be anonymously visible to the public in January 2019. More information about the objective and scope of the workshop can be found: https://sites.google.com/site/nips18spatiotemporal/

We would be most grateful for your assistance.

Best Regards,
Ransalu Senanayake, The University of Sydney (rsen4557@uni.sydney.edu.au)
Neal Jean, Stanford University (nealjean@stanford.edu)
Fabio Ramos, The University of Sydney and NVIDIA Research (fabio.ramos@sydney.edu.au)
Girish Chowdhary, University of Illinois Urbana-Champaign (girishc@illinois.edu)"""
    return message


reminder_message = """Dear Reviewers,

This is a friendly reminder about the NIPS'18 Workshop on Modeling and Decision-Making in the Spatiotemporal Domain. Kindly submit the reviews before 11.59 pm on October 31, 2018 AOE.

To submit a review, log into https://openreview.net with the email address that you receive this email. If you do not have an OpenReview account, please sign up with the email address that you receive this email. Select "Tasks" from the top menubar.  Select "Show pending tasks", then select a task to see the papers that have been assigned to you and the review forms. Please fill-in the "Overall Evaluation" and "Confidential Review" sections of each paper. Additionally, if you want to send a private message to the other reviewers and PCs, fill-in the "Official Comment" section.

Regarding "Overall Evaluation", please write a few sentences summarizing the paper and its main contributions, then your overall evaluation of the paper. Try to include comments about the positive aspects of the paper as well as advice about how the paper could be improved—we hope for the review process to be beneficial for authors! Providing short answers to the following questions will help the authors to improve their paper.
    1. What did you learn from reading this paper that you did not know before?
    2. What was the most exciting part of the work?
    3. What in your opinion makes this work stand apart from other papers in this area?
    4. Does the paper fit into the scope of the workshop?
    5. Are you aware of relevant literature that you may want to make the authors aware of?

Please note that your reviews under overall evaluation will be anonymously visible to the public in December 2018. More information about the objective and scope of the workshop can be found: https://sites.google.com/site/nips18spatiotemporal/ .

Feel free to contact us if you have any questions regarding the review process or the OpenReview system. We would be most grateful for your assistance.

Best Regards,
Ransalu Senanayake, The University of Sydney (rsen4557@uni.sydney.edu.au)
Neal Jean, Stanford University (nealjean@stanford.edu)
Fabio Ramos, The University of Sydney and NVIDIA Research (fabio.ramos@sydney.edu.au)
Girish Chowdhary, University of Illinois Urbana-Champaign (girishc@illinois.edu)"""

sorry_message = """Dear Reviewers,

There was a delay in assigning your reviews.  Sorry for any inconvenience, they are now available.

To submit a review, log into https://openreview.net with the email address that you receive this email. If you do not have an OpenReview account, please sign up with the email address that you receive this email. Select "Tasks" from the top menubar.  Select "Show pending tasks", then select a task to see the papers that have been assigned to you and the review forms. Please fill-in the "Overall Evaluation" and "Confidential Review" sections of each paper. Additionally, if you want to send a private message to the other reviewers and PCs, fill-in the "Official Comment" section.

Sincerely,
OpenReview
"""
#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################


## send email to each reviewer
email_addrs = []
with open(args.assignments, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        email_addrs.append(row[0])
email_set = set(email_addrs)
email_addrs = list(email_set)

#print(email_addrs)

response = client.send_mail(subjectline, email_addrs, reminder_message)
print(response)