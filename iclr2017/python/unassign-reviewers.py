#!/usr/bin/python

import argparse
import csv
from openreview import *


parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing reviewer unassignments or (2) a string of the format '<paper#>, <email_address>' e.g. '23,reviewer@cs.umass.edu'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)
baseurl = openreview.baseurl


def unassign_reviewer(member, paper_number):

    reviewers_id = 'ICLR.cc/2017/conference/paper' + str(paper_number)+ '/reviewers'
    reviewers = openreview.get_group(reviewers_id)
    if reviewers:
        result = openreview.get_groups(member= member, regex = 'ICLR.cc/2017/conference/paper' + str(paper_number) + '/AnonReviewer[1-9]*')
        if result and len(result) > 0:
            reviewer = result[0]
            res = openreview.remove_members_from_group(reviewers, [reviewer.id])
            print "Member", member, "removed from", reviewers.id
        else:
            print "Member not found in the assignment", member
    else:
        print "Reviewers group not found", reviewers_id

if args.assignments.endswith('.csv'):   
    with open(args.assignments, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            paper_number = row[0]
            member = row[1]
            unassign_reviewer(member, paper_number)
else:
    paper_number = args.assignments.split(',')[0]
    reviewer = args.assignments.split(',')[1]
    unassign_reviewer(reviewer,paper_number)

