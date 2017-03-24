#!/usr/bin/python

###############################################################################
# Group dump python script will simply print the contents of any given note.
# PCs can run this as they wish to inspect the system.
###############################################################################

## Import statements
import argparse
import csv
import json
import sys
from openreview import *

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', help="The directory to save the output file")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

params = {}

notes = openreview.get_notes(invitation='ICLR.cc/2017/workshop/-/submission')
conference_acceptances = openreview.get_notes(invitation = 'ICLR.cc/2017/conference/-/paper.*/acceptance')
conference_decision_dict = {n.forum: n.content['decision'] for n in conference_acceptances}
workshop_acceptances = openreview.get_notes(invitation = 'ICLR.cc/2017/workshop/-/paper.*/acceptance')
workshop_decision_dict = {n.forum: n.content['decision'] for n in workshop_acceptances}

if args.output!=None:
    ext = args.output.split('.')[-1]
    ##todo: fix rows with lists (e.g. members)
    if ext.lower()=='csv':
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['id', 'number', 'original', 'conference_decision', 'workshop_decision', 'date', 'title', 'TL;DR', 'abstract','keywords','authors','authorids','conflicts']
            csvwriter.writerow(fieldnames)

            for note in notes:
                conference_decision = conference_decision_dict[note.original] if note.original else None
                workshop_decision = workshop_decision_dict.get(note.id)
                if not workshop_decision and conference_decision == 'Invite to Workshop Track':
                    workshop_decision = 'Accept'
                row = []
                row.append('https://openreview.net/forum?id=%s' % note.id)
                row.append(note.number)
                row.append('https://openreview.net/forum?id=%s' % note.original if note.original else None)
                row.append(conference_decision)
                row.append(workshop_decision)
                row.append(note.tcdate)
                row.append(note.content['title'].encode('UTF-8'))
                row.append(note.content['TL;DR'].encode('UTF-8'))
                row.append(note.content['abstract'].encode('UTF-8'))
                row.append(', '.join(note.content['keywords']).encode('UTF-8'))
                row.append(', '.join(note.content['authors']).encode('UTF-8'))
                row.append(', '.join(note.content['authorids']).encode('UTF-8'))
                row.append(', '.join(note.content['conflicts']).encode('UTF-8'))
                csvwriter.writerow(row)
else:
    for n in notes:
        print json.dumps(n.to_json(), indent=4, sort_keys=True)
