#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import csv
import sys
import openreview

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-g','--group', help="group whose members will receive the email")
parser.add_argument('-e','--email', metavar='N', type=str, nargs='+', help="emails separated by space")
parser.add_argument('-q','--quiet', action='store_true', help='if present, does not print email output')
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

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
    if client.exists(args.group):
        groupToMail = client.get_group(args.group)
        for m in groupToMail.members:
            if '@' in m:
                groups.append(m)
    else:
        print "Error while retrieving group '"+args.group+"'; group may not exist"

if args.email:
    groups.extend(args.email)

response = client.send_mail(subjectline, groups, message)

if not args.quiet:
    print "Emailed the following users: "
    for e in response['groups']:
        print e


