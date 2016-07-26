#!/usr/bin/python

###############################################################################
# Note dump python script will simply print the contents of papers/reviews/
# comments matching certain criteria. PCs can run this as they wish to inspect 
# the system.
###############################################################################

## Import statements
import argparse
import csv
import getpass
import sys
sys.path.append('../..')
from client import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-i','--id', help="Id of the note to examine")
parser.add_argument('-v','--invitation', help="Notes that respond to this invitation")
parser.add_argument('-o','--output', help="the directory to save the output csv")
parser.add_argument('-f','--format', help="The file format to save. Choose either json or csv.")
parser.add_argument('--baseurl', help="base url")
args = parser.parse_args()

## Initialize the client library with username and password
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass()
if args.baseurl != None:
    or3 = Client(username,password, base_url=args.baseurl)
else:
    or3 = Client(username,password)


data = {}

if args.id != None:
	data['id']=args.id
if args.invitation != None:
	data['invitation']=args.invitation

note = or3.get_note(data)

if args.output!=None and args.format==None:
    print "Output file not saved: please specify a format."

if args.format!=None:
    if args.output!=None and args.format.lower()=="json":
        with open(args.output, 'w') as outfile:
            json.dump(json.loads(note.text), outfile, indent=4, sort_keys=True)


else:
	print json.dumps(json.loads(note.text), indent=4, sort_keys=True)
