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
import getpass
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
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass()
if args.baseurl != None:
    or3 = Client(username,password, base_url=args.baseurl)
else:
    or3 = Client(username,password)


get_request = or3.get_group({'id':args.group})
get_request.raise_for_status()

group = json.loads(get_request.content)['groups'][0]
with open(args.webfield) as f: 
    group['web'] = f.read()
    post_request = or3.set_group(group)
    post_request.raise_for_status()