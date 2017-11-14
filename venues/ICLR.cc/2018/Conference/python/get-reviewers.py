#!/usr/bin/python

###############################################################################
#
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
parser.add_argument('-n', '--paper_number', help="the number of the paper to assign this reviewer to")
parser.add_argument('-u', '--user',help="the user whose reviewing assignments you would like to see")
parser.add_argument('-a', '--all',help="specify an output file to save all the reviewer assignments")
parser.add_argument('-p', '--papers',help="specify an output file to save all paper numbers and assigned reviewers for each")
parser.add_argument('-r', '--reviewers',help="specify an output file to save all reviewers and his/her paper assignments")
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


if args.paper_number != None:

    paper_number = args.paper_number
    notes = openreview.get_notes(invitation = 'ICLR.cc/2018/Conference/-/Blind_Submission', number = paper_number)

    if len(notes) > 0:
        note = notes[0]
        reviewers = openreview.get_group('ICLR.cc/2018/Conference/Paper' + str(note.number) + '/Reviewers');

        print reviewers.members

    else:
        print "Paper number not found", paper_number

if args.user != None:

    user = args.user
    try:
        reviewers = openreview.get_groups(member = user, regex = 'ICLR.cc/2018/Conference/Paper[0-9]+/Reviewers')

        if len(reviewers):
            for reviewer in reviewers:
                paperNumber = reviewer.id.split('Paper')[1].split('/Reviewers')[0]
                print paperNumber
        else:
            print "No paper assigned to reviewer", user
    except Exception as ex:
        print "Can not the groups for", user


if args.all != None:
    # print paper number and reviewer id on each line
    with open(args.all, 'wb') as outfile:

        csvwriter = csv.writer(outfile, delimiter=',')

        notes = openreview.get_notes(invitation = 'ICLR.cc/2018/Conference/-/Blind_Submission')
        assignments = openreview.get_groups(id = 'ICLR.cc/2018/Conference/Paper.*/Reviewers')

        assignments_by_paper = {}
        for a in assignments:
            paper_number = a.id.split('Paper')[1].split('/Reviewers')[0]
            assignments_by_paper[paper_number] = a.members

        for n in notes:
            key = str(n.number)
            if key in assignments_by_paper.keys():
                reviewers = assignments_by_paper[key]
                for reviewer in reviewers:
                    row = []
                    row.append(key)
                    row.append(reviewer.encode('utf-8'))
                    csvwriter.writerow(row)
            else:
                row = []
                row.append(n.number)
                row.append('None')
                csvwriter.writerow(row)

if args.papers:
    # print paper number, number of reviewers and lists reviewers
    with open(args.papers, 'wb') as outfile:

        csvwriter = csv.writer(outfile, delimiter=',')

        notes = openreview.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
        assignments = openreview.get_groups(id='ICLR.cc/2018/Conference/Paper.*/Reviewers')

        assignments_by_paper = {}
        for a in assignments:
            paper_number = a.id.split('Paper')[1].split('/Reviewers')[0]
            assignments_by_paper[paper_number] = a.members

        # print paper, number of reviewers, reviewer ids
        row = ['Paper #','Number of Reviewers','Reviewer1', 'Reviewer2', 'Reviewer3']
        csvwriter.writerow(row)
        for n in notes:
            key = str(n.number)
            row = []
            row.append(key)
            if key in assignments_by_paper.keys():
                reviewers = assignments_by_paper[key]
                row.append(len(reviewers))
                for reviewer in reviewers:
                    row.append(reviewer.encode('utf-8'))
            else:
                row.append('0')

            csvwriter.writerow(row)

if args.reviewers:
    # print to file reviewer, number of papers assigned and list of paper numbers
    with open(args.reviewers, 'wb') as outfile:

        csvwriter = csv.writer(outfile, delimiter=',')

        notes = openreview.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
        assignments = openreview.get_groups(id='ICLR.cc/2018/Conference/Paper.*/Reviewers')

        papers_by_reviewer = {}
        for a in assignments:
            paper_number = a.id.split('Paper')[1].split('/Reviewers')[0]
            for reviewer in a.members:
                if reviewer not in papers_by_reviewer:
                    papers_by_reviewer[reviewer] = []
                papers_by_reviewer[reviewer].append(paper_number)

        # print reviewer, number of papers
        row = ['Reviewer','Number of Papers', 'Paper #']
        csvwriter.writerow(row)
        for key in papers_by_reviewer.keys():
            row = []
            row.append(key.encode('utf-8'))
            row.append(len(papers_by_reviewer[key]))
            row.extend(papers_by_reviewer[key])
            csvwriter.writerow(row)




