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

submissions = openreview.get_notes(invitation='NIPS.cc/2016/workshop/NAMPI/-/submission')
notes = [note for note in submissions if str(note.number)==str(args.paper_number)]

if args.paper_number!=None:
    
    try:
        note = notes[0]
        message = []
        reviewers = openreview.get_group('NIPS.cc/2016/workshop/NAMPI/paper'+str(note.number)+'/reviewers');
        for rev in reviewers.members:
            reviewer_wrapper=openreview.get_group(rev)
            reviewerNumber = rev.split('paper')[1].split('/reviewer')[1]
            
            pad = '{:32s}'.format("["+str(reviewer_wrapper.members[0])+"] ")
            message.append(pad+"reviewer"+reviewerNumber+" ("+rev+")")

        message.sort()
        print 'Reviewers assigned to paper '+args.paper_number+':'
        for m in message:
            print m
    except IndexError:
        print "Reviewer assignments not found. This submission may not yet have reviewers assigned to it."

if args.user!=None:
    user = args.user
    groups = openreview.get_groups(member=user,regex='NIPS.cc/2016/workshop/NAMPI/paper[0-9]+/reviewer[0-9]+')
    notes = openreview.get_notes(invitation='NIPS.cc/2016/workshop/NAMPI/-/submission')
    notesMap = {}
    for n in notes:
        notesMap[str(n.number)]=n.forum

    print 'Papers assigned to reviewer '+user+":"
    for g in groups:
        paperNumber = g.id.split('paper')[1].split('/reviewer')[0]
        reviewerNumber = g.id.split('paper')[1].split('/reviewer')[1]
        print "["+str(notesMap[str(paperNumber)])+"] reviewer"+str(reviewerNumber)+" ("+g.id+")"

if args.user==None and args.paper_number==None:
    notes = openreview.get_notes(invitation='NIPS.cc/2016/workshop/NAMPI/-/submission')

    rows = []
    for note in notes:
        try:
            reviewers = openreview.get_group('NIPS.cc/2016/workshop/NAMPI/paper'+str(note.number)+'/reviewers');
            if hasattr(reviewers,'members'):
                message = '{:15s}'.format("Paper "+'{:3s}'.format(str(note.number))+" ["+str(note.forum)+"] ")
                for rev in reviewers.members:
                    reviewer_wrapper = openreview.get_group(rev)
                    reviewerNumber = rev.split('paper')[1].split('/reviewer')[1]
                    if hasattr(reviewer_wrapper,'members'):
                        members = reviewer_wrapper.members[0] if len(reviewer_wrapper.members)>0 else ''
                        reviewer_members_pad = '{:32s}'.format(str(members))
                    else:
                        reviewer_members_pad = '{:32s}'.format("[CONFLICT]")
                    message+=(reviewer_members_pad)
                rows.append((message,int(note.number)))

        except IndexError as e:
            print "Error on Paper ",note.number,e
            continue
        except AttributeError as e:
            print "Error on Paper ",note.number,e
            continue
    # rows.sort(sortByPaperNumber)
    for m in sorted(rows, key=lambda row: row[1]) :
        print m[0]


