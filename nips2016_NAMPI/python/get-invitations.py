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
parser.add_argument('-i','--id', help="return invitations with the given id")
parser.add_argument('-v','--invitee', help="return invitations that have this group as an invitee")
parser.add_argument('-p','--replytoNote', help="return invitations that have this note as the invitation's parent")
parser.add_argument('-r','--replyForum', help="return invitations whose reply corresponds to the given forum id")
parser.add_argument('-s','--signature', help="return invitations signed by the given user")
parser.add_argument('-n','--note', help = "return invitations that the given note responds to")
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

id        = args.id if args.id != None else None
invitee   = args.invitee if args.invitee != None else None
replytoNote= args.replytoNote if args.replytoNote != None else None
replyForum= args.replyForum if args.replyForum != None else None
signature = args.signature if args.signature != None else None
note      = args.note if args.note != None else None

invitations = openreview.get_invitations(id=id, invitee=invitee, replytoNote=replytoNote, replyForum=replyForum, signature=signature, note=note)

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