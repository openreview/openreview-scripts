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
parser.add_argument('-n', '--paper_number', help="the id of the paper to assign this areachair to")
parser.add_argument('-u', '--user',help="the user whose areachair assignments you would like to see")
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


submissions = openreview.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
notes = [note for note in submissions if str(note.number)==str(args.paper_number)]

if args.paper_number!=None:
    
    try:
        note = notes[0]
        message = []
        areachairs = openreview.get_group('ICLR.cc/2017/conference/paper'+str(note.number)+'/areachairs');
        for ac in areachairs.members:
            areachair_wrapper=openreview.get_group(ac)
            areachairNumber = ac.split('paper')[1].split('/areachair')[1]
            
            pad = '{:40s}'.format("["+str(areachair_wrapper.members[0])+"] ")
            message.append(pad+"areachair"+areachairNumber+" ("+ac+")")

        message.sort()
        print 'Areachairs assigned to paper '+args.paper_number+':'
        for m in message:
            print m
    except IndexError:
        print "Areachair assignments not found. This submission may not yet have areachairs assigned to it."

if args.user!=None:
    user = args.user
    groups = openreview.get_groups(member=user,regex='ICLR.cc/2017/conference/paper[0-9]+/areachair[0-9]+')
    notes = openreview.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
    notesMap = {}
    for n in notes:
        notesMap[str(n.number)]=n.forum

    print 'Papers assigned to areachair '+user+":"
    for g in groups:
        paperNumber = g.id.split('paper')[1].split('/areachair')[0]
        areachairNumber = g.id.split('paper')[1].split('/areachair')[1]
        print "["+str(notesMap[str(paperNumber)])+"] areachair"+str(areachairNumber)+" ("+g.id+")"

if args.user==None and args.paper_number==None:
    notes = openreview.get_notes(invitation='ICLR.cc/2017/conference/-/submission')

    rows = []
    for note in notes:
        try:
            areachairs = openreview.get_group('ICLR.cc/2017/conference/paper'+str(note.number)+'/areachairs');
            if hasattr(areachairs,'members'):
                message = '{:15s}'.format("Paper "+str(note.number)+" ["+str(note.forum)+"] ")
                for ac in areachairs.members:
                    areachair_wrapper = openreview.get_group(ac)
                    areachairNumber = ac.split('paper')[1].split('/areachair')[1]
                    if hasattr(areachair_wrapper,'members'):
                        members = areachair_wrapper.members[0] if len(areachair_wrapper.members)>0 else ''
                        reviewer_members_pad = '{:40s}'.format(str(members))
                    else:
                        reviewer_members_pad = '{:40s}'.format("[CONFLICT]")
                    message+=(reviewer_members_pad)
                rows.append(message)

        except IndexError as e:
            print "Error on Paper ",note.number,e
            continue
        except AttributeError as e:
            print "Error on Paper ",note.number,e
            continue
    rows.sort()
    for m in rows:
        print m


