#!/usr/bin/python

"""
This is the initialization script for a legacy conference.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
from openreview import *
from subprocess import call

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

groups = []
overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False
def overwrite_allowed(groupid):
    if not openreview.exists(groupid) or overwrite==True:
        return True
    else:
        return False

if openreview.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################

    argsString = "--baseurl=" + args.baseurl + " --username=" + args.username + " --password=" + args.password + " --overwrite=" + args.overwrite

    # set up the "sub conferences"...
    os.system("./superuser-init-inferning.py " + argsString)
    os.system("./superuser-init-peer-review.py " + argsString)

else:
    print "Aborted. User must be Super User."