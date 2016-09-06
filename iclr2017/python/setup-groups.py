#!/usr/bin/python

"""
Setup python script takes as input the CSV files above and creates group for 
ICLR.cc/2017/pc, areachairs, individual ACs, reviewers-invited, and creates 
reviewers-invited.web Javascript for handling reviewer invitations; if they 
accept, their email address is added to group ICLR.cc/2017/reviewers.

"""

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

groups = []

iclr2017programchairs = openreview.get_group('ICLR.cc/2017/pcs')

## Read in a csv file with the names of the program chair(s).
## Each name in the csv will be added as a member of ICLR.cc/2017/pc
if args.programchairs != None: 
    new_program_chairs = []
    with open(args.programchairs, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                new_program_chairs.append(email)
    iclr2017programchairs.members += new_program_chairs
    groups.append(iclr2017programchairs)


iclr2017areachairs = openreview.get_group('ICLR.cc/2017/areachairs')
## Read in a csv file with the names of the area chairs.
new_areachair_members = []
if args.areachairs != None:
    with open(args.areachairs, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                new_areachair_members.append(email)
    iclr2017areachairs.members += new_areachair_members
    groups.append(iclr2017areachairs)

## Read in a csv file with the names of the reviewers.
## Each name will be set as a member of ICLR.cc/2017/reviewers-invited.
## groups for 'reviewers' and for 'reviewers-declined' are also generated, but are not yet populated with members.

iclr2017reviewersinvited = openreview.get_group('ICLR.cc/2017/conference/reviewers-invited')

if args.reviewers != None:    
    reviewers_invited = []
    with open(args.reviewers, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                reviewers_invited.append(email)
    iclr2017reviewersinvited.members += reviewers_invited;
    groups.append(iclr2017reviewersinvited)


## Post the groups
for g in groups:
    print "Updating group: "+g.id
    openreview.post_group(g)

