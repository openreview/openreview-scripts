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
parser.add_argument('-i', '--paper_id', help="the id of the paper to assign this areachair to")
parser.add_argument('-u', '--user',help="the user whose reviewing assignments you would like to see")
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


if args.paper_id!=None:
    paper_id = args.paper_id
    
    try:
        note = openreview.get_note(paper_id)
        message = []
        reviewers = openreview.get_group('ICLR.cc/2017/conference/paper'+str(note.number)+'/reviewers');
        for rev in reviewers.members:
            reviewer_wrapper=openreview.get_group(rev)
            reviewerNumber = rev.split('paper')[1].split('/reviewer')[1]
            
            pad = '{:50s}'.format("["+str(reviewer_wrapper.members[0])+"] ")
            message.append(pad+"reviewer"+reviewerNumber+" ("+rev+")")

        message.sort()
        print 'Reviewers assigned to paper '+paper_id+':'
        for m in message:
            print m
    except IndexError:
        print "Reviewer assignments not found. This submission may not yet have reviewers assigned to it."

if args.user!=None:
    user = args.user
    groups = openreview.get_groups(member=user,regex='ICLR.cc/2017/conference/paper[0-9]+/reviewer[0-9]+')
    notes = openreview.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
    notesMap = {}
    for n in notes:
        notesMap[str(n.number)]=n.forum

    print 'Papers assigned to reviewer '+user+":"
    for g in groups:
        paperNumber = g.id.split('paper')[1].split('/reviewer')[0]
        reviewerNumber = g.id.split('paper')[1].split('/reviewer')[1]
        print "["+str(notesMap[str(paperNumber)])+"] reviewer"+str(reviewerNumber)+" ("+g.id+")"
