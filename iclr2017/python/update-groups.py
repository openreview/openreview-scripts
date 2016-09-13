#!/usr/bin/python

"""
Setup python script takes as input the CSV files above and adds them as
members to the groups ICLR.cc/2017/pc, areachairs, and reviewers-invited.

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

groups = [];


def update_group_members(groupid,csvfile):
    new_members = []
    group = openreview.get_group(groupid)
    if csvfile!=None and type(group)==Group:
        with open(csvfile, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for email in row:
                    new_members.append(email)
        group.members += new_members

    return group



for g,c in [('ICLR.cc/2017/pcs',args.programchairs),('ICLR.cc/2017/areachairs',args.areachairs),('ICLR.cc/2017/conference/reviewers-invited',args.reviewers)]:
    group = update_group_members(g,c)
    if c!=None:
        print "updating group ",g
        openreview.post_group(group)

    
