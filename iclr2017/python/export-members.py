#!/usr/bin/python

###############################################################################
# Exports the members of the given group to the given output csv file.
###############################################################################

## Import statements
import argparse
import csv
import json
import sys
from openreview import *

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('group', help="The group whose members will be exported")
parser.add_argument('output', help="The directory to save the output file")
parser.add_argument('--sort', help="if set to True, sort the list of members alphabetically")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--password')
parser.add_argument('--username')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)


group = openreview.get_group(args.group)

if type(group)==Group:
	members = group.members
	if args.sort!=None and args.sort.lower()=='true':
		members = sorted(members, key=lambda s: s.lower())
	with open(args.output, 'wb') as outfile:
	    csvwriter = csv.writer(outfile, delimiter=',')

	    for m in members:
	    	csvwriter.writerow([m])
else:
	print "Error: Group does not exist"