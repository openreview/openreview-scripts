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
parser.add_argument('-a','--all')
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
    
    if notes:
        note = notes[0]
        message = []
        areachairs = openreview.get_group('ICLR.cc/2017/conference/paper'+str(note.number)+'/areachairs');
        for ac in areachairs.members:
            areachair_wrapper=openreview.get_group(ac)
            areachairNumber = ac.split('paper')[1].split('/areachair')[1]
            
            if areachair_wrapper.members:
                pad = '{:40s}'.format("["+str(areachair_wrapper.members[0])+"] ")
                message.append(pad+"areachair"+areachairNumber+" ("+ac+")")
            else:
                print "Warning: Empty area chair group found. ID",areachair_wrapper.id

        message.sort()
        print 'Areachairs assigned to paper '+args.paper_number+':'
        for m in message:
            print m
    else:
        print "Note number ",args.paper_number,"not found."

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


if args.all != None:

    with open(args.all, 'wb') as outfile:

        csvwriter = csv.writer(outfile, delimiter=',')
        
        areachairs = openreview.get_group('ICLR.cc/2017/areachairs');

        for areachair in areachairs.members:

            assignments = openreview.get_groups(member = areachair, regex = 'ICLR.cc/2017/conference/paper[0-9]+/areachairs')

            if len(assignments) > 0 :

                for a in assignments:
                    row = []
                    paper_number = a.id.split('paper')[1].split('/areachairs')[0]
                    row.append(areachair)
                    row.append(paper_number)
                    csvwriter.writerow(row)
            else:
                row = []
                row.append(areachair)
                row.append('')
                csvwriter.writerow(row)                


