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


subjectline = "<Insert your subject line here>"

message = """

<Insert your multi-line email message here>

"""


#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################

recipients = args.group if args.group!=None else ""

groupToMail = openreview.get_group(recipients)

if type(groupToMail)==Group:
    response = openreview.send_mail(subjectline, [groupToMail.id], message)
    print "Emailed the following users: ",response.json()['groups']
else:
    print "Error while retrieving group '"+recipients+"'; group may not exist"


