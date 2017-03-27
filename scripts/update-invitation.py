#!/usr/bin/python

###############################################################################
# Modifies the specified invitation webfield
###############################################################################

## Import statements
import argparse
import csv
import json
import sys
from openreview import *

## Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('invitation', help="the invitation whose webfield will be replaced")
parser.add_argument('webfield',   help="html file that will replace the current group homepage")
parser.add_argument('--baseurl',  help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username is not None and args.password is not None:
    openreview = Client(baseurl = args.baseurl, username = args.username, password = args.password)
else:
    openreview = Client(baseurl = args.baseurl)

try:
  invitations = openreview.get_invitations(id=args.invitation)
except Exception as e:
  print "Invitation " + args.invitation + " Not Found"
  exit(1)

if invitations:
    inv = invitations[0]

    with open(args.webfield) as f:
        inv.web = f.read()
        updated_group = openreview.post_invitation(inv)
    print "Invitation " + inv.id + " Updated"

exit(0)
