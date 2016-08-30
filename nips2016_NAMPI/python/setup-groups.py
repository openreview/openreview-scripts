#!/usr/bin/python

###############################################################################
# Setup groups script for NIPS 2016 workshop: NAMPI
###############################################################################

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('-a','--areachairs', help="csv file containing the email addresses of the area chairs")
parser.add_argument('-r','--reviewers', help="csv file containing the email addresses of the candidate reviewers")
parser.add_argument('-u','--baseurl', help="base URL for the server to connect to")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

nips2016_workshop = Group('NIPS.cc/2016/workshop',
    signatories = ['NIPS.cc/2016/workshop'],
    writers     = ['NIPS.cc/2016','NIPS.cc/2016/workshop'],
    members     = [],
    readers     = ['everyone'],
    signatures  = ['NIPS.cc/2016'])

nips2016_workshop_NAMPI = Group('NIPS.cc/2016/workshop/NAMPI', 
    signatories = ['NIPS.cc/2016/workshop/NAMPI'], 
    writers     = ['NIPS.cc/2016/workshop','NIPS.cc/2016/workshop/NAMPI'],
    members     = [],
    readers     = ['everyone'], 
    web         = '../webfield/NAMPI-webfield.html',
    signatures  = ['NIPS.cc/2016/workshop'])


groups = [nips2016_workshop,nips2016_workshop_NAMPI]

## Post the groups
for g in groups:
    print "Posting group: "+g.id
    openreview.post_group(g)

## Add the conference group to the host page
## NOTE: Should this be refactored into a "save to homepage" function or something like that?
openreview.post_group(openreview.get_group('host').add_member(nips2016_workshop_NAMPI))
