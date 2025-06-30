#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import csv
import sys
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
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

#################################################
#                                               #
#   EDIT YOUR MESSAGE AND SUBJECT LINE BELOW    #
#                                               #
#################################################


subjectline = "RSS 2017: Robot Communication in the Wild (RCW) paper review assignment"

def get_message(url):
	message = """Dear RSS 2017: Robot Communication in the Wild (RCW) workshop committee member,

	The attached paper {0} has been submitted for possible presentation at our upcoming workshop (https://rss2017-rcw.mit.edu/). We would greatly appreciate your help in evaluating the submission by June 27, 2017, 11:59:59pm Anywhere on Earth time (UTC -12).

	We would like to remind reviewers that the Poster Track submissions are non-archival and are meant to foster a wide exchange of ideas between many people (i.e., old/incremental/weird work is OK). By contrast, Proceedings Track submissions should be more mature. Given the short time constraints, please keep this in mind and use your discretion to minimize review workload. For details on the openreview process, please see our website https://rss2017-rcw.mit.edu/.

	Reviewer instructions:
	- Please confirm to organizing committee member shayegan@mit.edu that you received this email.
	- To submit a review, log into https://openreview.net. Select \"Tasks\" under the dropdown menu under your name.  Select a paper that you've been assigned to review and press the Official Review button.'
	- Please complete the review by the indicated deadline using the online submission and review system.

	Thank you for your help on evaluating this paper. The success of our workshop is to a large extent due to the efforts of our committee members.

	Sincerely, the organizing committee,
	Robert Fitch
	Don Sofge
	Geoffrey Hollinger
	Karthik Dantu
	Michael Otte
	Shayegan Omidshafiei""".format(url)

	return message


#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################
groups = []

if args.group:
	groupToMail = openreview.get_group(args.group)
	if type(groupToMail)==Group:
		for m in groupToMail.members:
			message = get_message(url)
			response = openreview.send_mail(subjectline, [m], message)

	else:
	    print "Error while retrieving group '"+args.group+"'; group may not exist"