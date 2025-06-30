#!/usr/bin/python

import argparse
import csv
import openreview


parser = argparse.ArgumentParser()
parser.add_argument('unassignments', help="either (1) a csv file containing reviewer unassignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'reviewer@cs.umass.edu,25'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
baseurl = client.baseurl


def unassign_reviewer(member, paper_number):

    reviewers_id = 'ICLR.cc/2017/workshop/paper%s/reviewers' % paper_number
    reviewers = client.get_group(reviewers_id)
    if reviewers:
        anonreviewer_groups = client.get_groups(member = member, regex = 'ICLR.cc/2017/workshop/paper' + str(paper_number) + '/AnonReviewer[1-9]*')
        if anonreviewer_groups and len(anonreviewer_groups) > 0:
            reviewer = anonreviewer_groups[0]
            client.remove_members_from_group(reviewers, [reviewer.id])
            client.remove_members_from_group(reviewer, reviewer.members)
            print "Member", member, "removed from", reviewers.id, "and", reviewer.id
        else:
            print "Member not found in the assignment: ", member
    else:
        print "Reviewers group not found", reviewers_id

if args.unassignments.endswith('.csv'):
    with open(args.unassignments, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            member = row[0]
            paper_number = row[1]
            unassign_reviewer(member, paper_number)
else:
    reviewer = args.unassignments.split(',')[0]
    paper_number = args.unassignments.split(',')[1]
    unassign_reviewer(reviewer,paper_number)

