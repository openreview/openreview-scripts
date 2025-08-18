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
groups = [
    'ICLR.cc/2017/conference/reviewers',
    'ICLR.cc/2017/conference/authors',
    'ICLR.cc/2017/workshop/reviewers',
    'ICLR.cc/2017/workshop/authors',
    'ICLR.cc/2017/areachairs'
]

response = openreview.send_mail(subjectline, groups, message)
print "Emailed the following users: ",response['groups']


