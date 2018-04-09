#!/usr/bin/python

###############################################################################
# Homepage setup python script creates/modifies the group homepage on
# OpenReview, including the group.web script that will list submitted (and
# later accepted) papers.  Michael will run this initially.  PCs can edit this
# script and run it again later as they wish, to change home page contents.
###############################################################################

## Import statements
import argparse
import csv
import json
import sys
import openreview

## Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('group', help="the group whose webfield will be replaced")
parser.add_argument('webfield', help="html file that will replace the current group homepage")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


group = client.get_group(args.group)
print group.id

with open(args.webfield) as f:
    group.web = f.read()

group.signatures = [client.signature]

updated_group = client.post_group(group)
