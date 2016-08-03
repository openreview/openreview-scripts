#!/usr/bin/python

###############################################################################
# Group dump python script will simply print the contents of any given invitation.  
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
parser.add_argument('-i','--id', help="The desired invitation's id")
parser.add_argument('-v','--invitee', help="the invitations that have this invitee")
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
id = args.id if args.id!=None else None
invitee = args.invitee if args.invitee!=None else None  

invitations = openreview.get_invitations(id=id, invitee=invitee)

if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='json':
        with open(args.output, 'w') as outfile:
            for i in invitations:
                json.dump(i.to_json(), outfile, indent=4, sort_keys=True)

    ##todo: fix rows with lists (e.g. members)
    if ext.lower()=='csv':
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['id','readers','writers','invitees','reply','web','process']
            csvwriter.writerow(fieldnames)

            for count, invitation in enumerate(invitations):
                row = []
                for key in fieldnames:
                    try:
                        row.append(invitation.to_json()[key])
                    except KeyError:
                        row.append('')
                csvwriter.writerow(row)
else:
    for i in invitations:
        print json.dumps(i.to_json(), indent=4, sort_keys=True)