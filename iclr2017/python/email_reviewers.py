#!/usr/bin/python

###############################################################################
# Reviewer invitation python script sends email to all invited reviewers.  PCs 
# can edit the message and run this script themselves.
###############################################################################

## Import statements
import argparse
import csv
import getpass
import json
import sys
sys.path.append('../..')
from client import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-r','--recipients', help="the group that will recieve this message")
parser.add_argument('-s','--subject', help="your email's subject line in string form (e.g. 'this is a subject line')")
parser.add_argument('-m','--message', help="your email's message in string form (e.g. 'this is a message')")
args = parser.parse_args()

## Initialize the client library with username and password
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass()
or3 = Client(username,password)

message = """
Dear invited reviewer,

Thank you for deciding to participate as a reviewer for ICLR 2017! 
You will be notified of further instructions shortly.

Sincerely,
the ICLR 2017 program chairs
...
""" if args.message == None else args.message

subject = 'A message to reviewers' if args.subject == None else args.subject,
recipients = ['ICLR.cc/2017/reviewers'] if args.recipients == None else [args.recipients]

or3.send_mail(subject, recipients, message)