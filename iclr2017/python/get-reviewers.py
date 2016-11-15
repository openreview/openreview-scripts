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
    notes = openreview.get_notes(invitation = 'ICLR.cc/2017/conference/-/submission', number = paper_number)
    
    if len(notes) > 0: 
        note = notes[0]
        message = []
        reviewers = openreview.get_group('ICLR.cc/2017/conference/paper' + str(note.number) + '/reviewers');
        for rev in reviewers.members:
            reviewer_wrapper=openreview.get_group(rev)

            if len(reviewer_wrapper.members) > 0:
                reviewerNumber = rev.split('paper')[1].split('/AnonReviewer')[1]
                pad = '{:32s}'.format(reviewer_wrapper.members[0].encode('utf-8'))
                message.append(pad+("reviewer"+reviewerNumber+" ("+str(rev)+")").encode('utf-8'))
            else:
                print "Reviewer group has no members", reviewer_wrapper.id
        message.sort()
        
        print 'Reviewers assigned to paper '+paper_number+':'
        for m in message:
            print m
    else:
        print "Paper number not found", paper_number

if args.user != None:

    user = args.user
    try:
        reviewers = openreview.get_groups(member = user, regex = 'ICLR.cc/2017/conference/paper[0-9]+/reviewers')
    
        if len(reviewers):
            print 'Papers assigned to reviewer ' + user + ":"
            for reviewer in reviewers:
                paperNumber = reviewer.id.split('paper')[1].split('/reviewers')[0]
                print "[" + str(paperNumber) + "] reviewer " + str(user) + " (" + reviewer.id + ")"
        else:
            print "No paper assigned to reviewer", user
    except Exception as ex:
        print "Can not the groups for", user



