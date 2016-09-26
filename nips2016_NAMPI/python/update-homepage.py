#!/usr/bin/python

###############################################################################
# Homepage setup python script creates/modifies ICLR 2017 homepage on 
# OpenReview, including the group.web script that will list submitted (and 
# later accepted) papers.  Michael will run this initially.  PCs can edit this 
# script and run it again later as they wish, to change home page contents.
###############################################################################

## Import statements
import argparse
import csv
import json
import sys
from openreview import *

## Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('group', help="the group whose webfield will be replaced (default: ICLR.cc/2017/conference)")
parser.add_argument('webfield', help="html file that will replace the current ICLR 2017 homepage")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)



group = openreview.get_group(args.group)
print "Updated homepage of group ",group

with open(args.webfield) as f: 
    group.web = f.read()
    #group.signatures=[openreview.user['id']]
    updated_group = openreview.post_group(group)
