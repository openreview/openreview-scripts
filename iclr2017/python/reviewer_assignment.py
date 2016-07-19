#!/usr/bin/python

###############################################################################
# Not to spec
###############################################################################

## Import statements
import argparse
import csv
import getpass
import sys
sys.path.append('../..')
from client import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
args = parser.parse_args()

## Initialize the client library with username and password
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass()
or3 = Client(username,password)



reviewers = or3.get_group({'id':'ICLR.cc/2017/reviewers'}).json()['groups'][0]['members']

reviewer1 = Group('ICLR.cc/2017/conference/paper444/reviewer1', writers=['ICLR.cc/2017/conference'], readers=['ICLR.cc/2017/areachair1'], members=[reviewers[0]], signatories=[reviewers[0]])

or3.set_group(reviewer1.body)