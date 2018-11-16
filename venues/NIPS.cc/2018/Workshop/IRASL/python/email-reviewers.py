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


subjectline = "NIPS'18 IRASL workshop reviews"

message = """
Dear Reviewer,

We would like to sincerely thank you for taking your time to review for the IRASL workshop.

When possible, we tried to do our best to assign manuscripts according to the preferences specified in the reviewer form.

We would kindly ask you to review the following papers:
    {0}
    {1}
    {2}
    {3}

We ask you to submit your review through Openreview by November,12, 2018.

To submit a review, log into https://openreview.net with the email address that you receive this email. If you do not have an OpenReview account, please sign up with the email address that you receive this email. Select "Tasks" from the top menubar.  Select "Show pending tasks", then select a task to see the papers that have been assigned to you and the review forms.

Feel free to contact us at irasl@googlegroups.com for any questions or concerns.

Regards,

The IRASL committee
"""

late_message = """
Dear Reviewer,

This is a reminder that your NIPS IRASL paper reviews are due by Monday, November 12, 2018.

To submit a review, log into https://openreview.net with the email address that you receive this email. If you do not have an OpenReview account, please sign up with the email address that you receive this email. Select "Tasks" from the top menubar.  Select "Show pending tasks", then select a task to see the papers that have been assigned to you and the review forms.

Feel free to contact us at irasl@googlegroups.com for any questions or concerns.

Regards,

The IRASL committee
"""

#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################

notes = client.get_notes(invitation=config.BLIND_SUBMISSION)
title_by_number = {}
for note in notes:
    title_by_number[str(note.number)]=note.content['title']

## send email to each reviewer
email_addrs = {}
with open(args.assignments, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if row[1] not in email_addrs.keys():
            email_addrs[row[1]]= []
        email_addrs[row[1]].append(row[0])
'''
email_titles = {}
for key in email_addrs.keys():
    #print(key)
    titles = []
    for number in email_addrs[key]:
        titles.append(title_by_number[number])
    # pad number of titles out to 4
    for num in range(len(titles),4):
        titles.append('')
    email_titles[key]=titles
'''
for key in email_addrs.keys():
    #response = client.send_mail(subjectline, [key], message.format(email_titles[key][0],
    #               email_titles[key][1],email_titles[key][2],email_titles[key][3]))
    response = client.send_mail(subjectline, [key], late_message)
    print(response)
