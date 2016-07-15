#!/usr/bin/python

###############################################################################
# Homepage setup python script creates/modifies ICLR 2017 homepage on 
# OpenReview, including the group.web script that will list submitted (and 
# later accepted) papers.  Michael will run this initially.  PCs can edit this 
# script and run it again later as they wish, to change home page contents.
###############################################################################

import sys
sys.path.append('../..')
from client import *
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
parser.add_argument('webfield', help="html file that will replace the current ICLR 2017 homepage")
parser.add_argument('-g','--group', help="the group whose webfield will be replaced (default: ICLR.cc/2017/conference)")
args = parser.parse_args()

or3 = Client(args.username, args.password)

if args.group:
    group = args.group
else:
    group = 'ICLR.cc/2017/conference'
get_request = or3.get_group({'id':group})
get_request.raise_for_status()
iclr2017conference = json.loads(get_request.content)['groups'][0]
with open(args.webfield) as f: 
    iclr2017conference['web'] = f.read()
    post_request = or3.set_group(iclr2017conference)
    post_request.raise_for_status()