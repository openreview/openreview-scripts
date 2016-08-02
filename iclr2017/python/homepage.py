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
sys.path.append('../..')
from client import *

## Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-g','--group', help="the group whose webfield will be replaced (default: ICLR.cc/2017/conference)")
parser.add_argument('-w','--webfield', help="html file that will replace the current ICLR 2017 homepage")
parser.add_argument('--baseurl', help="base url")
args = parser.parse_args()

## Initialize the client library with username and password
openreview = Client(base_url=args.baseurl)


group = openreview.get_group(args.group)
print group.id

with open(args.webfield) as f: 
    group.web = f.read()
    updated_group = openreview.save_group(group)