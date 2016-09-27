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
parser.add_argument('--email', metavar='N', type=str, nargs='+', help="emails separated by space")
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


subjectline = "<Insert your subject line here>"

message = """

<Insert your multi-line email message here>

"""


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
			if '@' in m:
				groups.append(m)
	else:
	    print "Error while retrieving group '"+args.group+"'; group may not exist"

if args.email:
	groups.extend(args.email)

response = openreview.send_mail(subjectline, groups, message)
print "Emailed the following users: ",response.json()['groups']


