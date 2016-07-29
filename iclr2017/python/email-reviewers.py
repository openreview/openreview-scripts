#!/usr/bin/python

###############################################################################
# Reviewer invitation python script sends email to all invited reviewers.  PCs 
# can edit the message and run this script themselves.
###############################################################################

## Import statements
import argparse
import csv
import json
import sys
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-r','--recipients', help="the group that will recieve this message")
parser.add_argument('-s','--subject', help="your email's subject line in string form (e.g. 'this is a subject line')")
parser.add_argument('-m','--message', help="your email's message in string form (e.g. 'this is a message')")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)
    
message = """
Dear invited reviewer,

Thank you for deciding to participate as a reviewer for ICLR 2017! 
You will be notified of further instructions shortly.

Sincerely,
the ICLR 2017 program chairs

""" if args.message == None else args.message

if args.subject == None:
	subject = "A message to reviewers" 
else:
	subject = args.subject
	
if args.recipients!=None:
	recipients = [args.recipients]
	openreview.send_mail(subject, recipients, message)
else:
	print "Please specify an OpenReview group to send this message to. (Hint: the group of invited reviewers is ICLR.cc/2017/conference/reviewers-invited)"
	print "\nDEFAULT MESSAGE: "
	print "Subject: "+str(subject)
	print "Message: "+str(message)