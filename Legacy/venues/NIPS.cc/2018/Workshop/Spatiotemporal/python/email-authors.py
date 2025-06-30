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


subjectline = "NIPS 2018: Spatiotemporal Workshop attendance"

reminder_message = """Dear authors,

If you are planning to attend the workshop, kindly fill in the following form:
https://goo.gl/forms/MWMfbY39mybjrXnH2
If you have already done so, please ignore this email.

Kindly note that we have only a very limited number of tickets.

Thanks!

Regards,
-organizing committee"""

#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################


## send email to each author
notes = client.get_notes(invitation="NIPS.cc/2018/Workshop/Spatiotemporal/-/Submission")
authors=[]
for note in notes:
    authors.append("NIPS.cc/2018/Workshop/Spatiotemporal/Paper"+str(note.number)+"/Authors")

response = client.send_mail(subjectline, authors, reminder_message)
print(response)