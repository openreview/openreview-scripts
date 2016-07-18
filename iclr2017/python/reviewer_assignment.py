#!/usr/bin/python

###############################################################################
# Not to spec
###############################################################################


## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
args = parser.parse_args()

import os, sys
import requests

sys.path.append('../..')
from client import *

## Initialize the client library with username and password
or3 = Client(args.username,args.password)

reviewers = or3.get_group({'id':'ICLR.cc/2017/reviewers'}).json()['groups'][0]['members']

reviewer1 = Group('ICLR.cc/2017/conference/paper444/reviewer1', writers=['ICLR.cc/2017/conference'], readers=['ICLR.cc/2017/areachair1'], members=[reviewers[0]], signatories=[reviewers[0]])

or3.set_group(reviewer1.body)