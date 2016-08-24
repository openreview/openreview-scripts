#!/usr/bin/python

###############################################################################
# Not to spec
###############################################################################

## Import statements
import argparse
import csv
import getpass
import sys
import re
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('areachair', help="the area chair email address to assign")
parser.add_argument('paper_number', help="the number of the paper to assign this areachair to")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)
baseurl = openreview.baseurl

areachair = args.areachair
paper_number = args.paper_number

areachairs = openreview.get_group('ICLR.cc/2017/conference/paper'+paper_number+'/areachair')
existing_areachairs = areachairs.members

areachair_number = len(existing_areachairs)+1

for a in existing_areachairs:
    existing_areachair = openreview.get_group(a)
    print existing_areachair
    if areachair in existing_areachair.members:
        print "areachair found in existing_areachairs.members"
        areachair_number = existing_areachairs.index(a)+1
        break

print areachair_number

new_areachair_id = 'ICLR.cc/2017/conference/paper'+str(paper_number)+'/areachair'+str(areachair_number)
new_areachair = Group(
    new_areachair_id,
    signatures=['ICLR.cc/2017/conference'],
    writers=['ICLR.cc/2017/conference'],
    members=[areachair],
    readers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs',areachair],
    signatories=['ICLR.cc/2017/conference',areachair]
)
openreview.post_group(new_areachair)
openreview.post_group(areachairs.add_member(new_areachair.id))

conference_areachairs = openreview.get_group('ICLR.cc/2017/areachairs')
openreview.post_group(conference_areachairs.add_member(new_areachair.id));






