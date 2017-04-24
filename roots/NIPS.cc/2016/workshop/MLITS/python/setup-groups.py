#!/usr/bin/python

###############################################################################
# Setup script for NIPS 2016: Machine Learning for Intelligent Transportation Systems 
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

## NIPS.cc group already exists in beta
## NIPS.cc/2016 group already exists in beta
## NIPS.cc/2016/workshop group already exists in beta

nips2016workshop_MLITS = Group('NIPS.cc/2016/workshop/MLITS',
    signatories = ['NIPS.cc/2016/workshop/MLITS'], 
    writers     = ['NIPS.cc/2016/workshop'], 
    members     = [],
    readers     = ['everyone'],
    web			= '../webfield/MLITS-webfield.html', 
    signatures  = ['NIPS.cc/2016/workshop'])

## Program Chair members initially set with only Erran Li
nips2016workshop_MLITS_PC = Group('NIPS.cc/2016/workshop/MLITS/PC',
    signatories = ['NIPS.cc/2016/workshop/MLITS/PC'], 
    writers     = ['NIPS.cc/2016/workshop/MLITS'], 
    members     = ['erranlli@gmail.com'],
    readers     = ['NIPS.cc/2016/workshop/MLITS'], 
    signatures  = ['NIPS.cc/2016/workshop/MLITS'])

groups = [nips2016workshop_MLITS,nips2016workshop_MLITS_PC]

for i in groups:
	print "posting group: "+i.id
	openreview.post_group(i)

## Add the workshop to the host page
openreview.post_group(openreview.get_group('host').add_member(nips2016workshop_MLITS))