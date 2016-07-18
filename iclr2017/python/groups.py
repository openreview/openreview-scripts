#!/usr/bin/python

###############################################################################
# Group dump python script will simply print the contents of any given group.  
# PCs can run this as they wish to inspect the system.
###############################################################################

import sys
import requests
import json
sys.path.append('../..')
from client import *

## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="Your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="Your OpenReview password (e.g. abcd1234)")
parser.add_argument('group', help="The group (or regex expression for a set of groups) to examine. (Example: ICLR.cc/2017/.* searches for all groups starting with ICLR.cc/2017/)")
parser.add_argument('--output', help="the directory to save the output csv")
args = parser.parse_args()


## Initialize the client library with username and password
or3 = Client(args.username, args.password)

group = or3.get_group({'regex':args.group})

if args.output!=None:
    with open(args.output, 'w') as outfile:
        json.dump(json.loads(group.text), outfile, indent=4, sort_keys=True)
else:
    print json.dumps(json.loads(group.text), indent=4, sort_keys=True)

