#!/usr/bin/python

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('invitation', help="invitation to update")
parser.add_argument('--process', help="process file")
parser.add_argument('--webfield', help="html file that will replace the current ICLR 2017 homepage")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)


invitation = openreview.get_invitation(args.invitation)

if type(invitation) == Invitation: 
	
	if(args.process):
		with open(args.process) as f:
			invitation.process = f.read()

	if(args.webfield):
		with open(args.webfield) as f:
			invitation.web = f.read()

	updated_invitation = openreview.post_invitation(invitation)
	print "Updated invitation",updated_invitation.to_json().get('id')
else:
    print "Invitation not found"
    
