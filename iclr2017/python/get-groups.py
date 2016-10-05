#!/usr/bin/python

###############################################################################
# Group dump python script will simply print the contents of any given group.  
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
parser.add_argument('-g','--group', help="The group to examine.")
parser.add_argument('-p','--prefix', help="The prefix for the set of groups to examine")
parser.add_argument('-o','--output', help="The directory to save the output file")
parser.add_argument('-a','--add', help="a member to add to this group or set of groups")
parser.add_argument('-r','--remove',help="a member to remove from this group or set of groups")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--password')
parser.add_argument('--username')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

if args.group and args.prefix:
    print "Please specify either a group or a prefix, not both"

if args.group!=None:
    groups = [openreview.get_group(args.group)]
if args.prefix!=None:    
    groups = openreview.get_groups(prefix=args.prefix)
if args.add!=None:
    for g in groups:
        openreview.add_member_to_group(g,args.add)
if args.remove!=None:
    for g in groups:
        openreview.remove_member_from_group(g,args.remove)

if args.output!=None:
    ext = args.output.split('.')[-1]
    if ext.lower()=='json':
        with open(args.output, 'w') as outfile:
            for g in groups:
                json.dump(g.to_json(), outfile, indent=4, sort_keys=True)

    ##todo: fix rows with lists (e.g. members)
    if ext.lower()=='csv':
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['signatures','nonreaders','readers','origId','id','writers','members','signatories','active','emailable','tauthors','tcdate']
            csvwriter.writerow(fieldnames)

            for count, group in enumerate(groups):
                row = []
                for key in fieldnames:
                    try:
                        row.append(group.to_json()[key])
                    except KeyError:
                        row.append('')
                csvwriter.writerow(row)
elif groups!=[None]:
    for g in groups:
        print json.dumps(g.to_json(), indent=4, sort_keys=True)