#!/usr/bin/python

###############################################################################
# Setup python script takes as input the CSV files above and creates group for 
# ICLR.cc/2016/pc, areachairs, individual ACs, reviewers-invited, and creates 
# reviewers-invited.web Javascript for handling reviewer invitations; if they 
# accept, their email address is added to group ICLR.cc/2016/reviewers.
###############################################################################

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('-u','--baseurl', help="base URL for the server to connect to")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

nips_2016symposiumpc = openreview.get_group('NIPS.cc/2016/Deep_Learning_Symposium/PC')

## Read in a csv file with the names of the program chair(s).
## Each name in the csv will be set as a member of ICLR.cc/2016/pc
if args.programchairs != None:
    program_chairs = []
    
    with open(args.programchairs, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                nips_2016symposiumpc.add_member(email)

openreview.post_group(nips_2016symposiumpc)

