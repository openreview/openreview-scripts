#!/usr/bin/python

"""
Updates the PC and reviewers-invited groups

"""

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('-r','--reviewers', help="csv file containing the email addresses of candidate reviewers. Will send invitation email to the addresses on this list.")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

groups = [];

def SingleAssignmentValid(s):
    if not '@' in s:
        return False

    return True

def update_group_members(groupid,assignment):
    new_members = []
    group = openreview.get_group(groupid)
    

    if type(group)==Group:

        if assignment.endswith('.csv'):
            with open(assignment, 'rb') as assignment:
                reader = csv.reader(assignment, delimiter=',', quotechar='|')
                for row in reader:
                    for email in row:
                        if '@' in email:
                            new_members.append(email)
        elif SingleAssignmentValid(assignment):
            new_members.append(assignment)
        else:
            print "Invalid input: ",assignment
            sys.exit()

        print "updating group ",g
        group.members += new_members
    else:
        print "could not find group ",g

    return group


for g,c in [('NIPS.cc/2016/workshop/NAMPI/pcs',args.programchairs),('NIPS.cc/2016/workshop/NAMPI/reviewers-invited',args.reviewers)]:
    if c!=None:
        group = update_group_members(g,c)
        if type(group)==Group:
            openreview.post_group(group)

    
