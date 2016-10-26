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
parser.add_argument('-f','--forum', help="The desired note's forum id")
parser.add_argument('-i','--invitation', help="the desired note's invitation")
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
forum = args.forum if args.forum!=None else None
invitation = args.invitation if args.invitation!=None else None  

notes = openreview.get_notes(forum=forum, invitation=invitation)

if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='json':
        with open(args.output, 'w') as outfile:
            for n in notes:
                json.dump(n.to_json(), outfile, indent=4, sort_keys=True)

    ##todo: fix rows with lists (e.g. members)
    if ext.lower()=='csv':
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['title','abstract','keywords','authors','authorids','conflicts','forum','invitation','replyto','pdfTransfer','readers','signatures','writers']
            csvwriter.writerow(fieldnames)

            for count, note in enumerate(notes):
                row = []
                for key in fieldnames:
                    try:
                        if key in ['title','abstract','keywords','authors','authorids','conflicts']:
                            row.append(note.to_json()['content'][key])
                        else: 
                            row.append(note.to_json()[key])
                    except KeyError:
                        row.append('')
                csvwriter.writerow(row)
else:
    for n in notes:
        print json.dumps(n.to_json(), indent=4, sort_keys=True)