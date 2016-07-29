#!/usr/bin/python

###############################################################################
# Group dump python script will simply print the contents of any given group.  
# PCs can run this as they wish to inspect the system.
###############################################################################

## Import statements
import argparse
import csv
import getpass
import json
import pydash
import sys
sys.path.append('../..')
from client import *

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-g','--group', help="The group (or regex expression for a set of groups) to examine. (Example: ICLR.cc/2017/.* searches for all groups starting with ICLR.cc/2017/)")
parser.add_argument('-o','--output', help="The directory to save the output file")
parser.add_argument('-f','--format', help="The file format to save. Choose either json or csv.")
parser.add_argument('--baseurl', help="base url")
args = parser.parse_args()

## Initialize the client library with username and password
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass()
or3 = Client(username,password, base_url=args.baseurl)


groups = json.loads(or3.get_group({'regex':args.group}).text)['groups']

if args.output!=None and args.format==None:
    print "Output file not saved: please specify a format."

if args.format !=None:
    if args.output!=None and args.format.lower()=="json":
        with open(args.output, 'w') as outfile:
            json.dump(groups, outfile, indent=4, sort_keys=True)

    ##todo: fix rows with lists (e.g. members)
    if args.output!=None and args.format.lower()=="csv":
        with open(args.output, 'wb') as outfile:
            csvwriter = csv.writer(outfile, delimiter=',')
            fieldnames = ['signatures','nonreaders','readers','origId','id','writers','members','signatories','active','emailable','tauthors','tcdate']
            csvwriter.writerow(fieldnames)

            for count, group in enumerate(groups):
                row = []
                for key in fieldnames:
                    row.append(group[key])
                csvwriter.writerow(row)

print json.dumps(groups, indent=4, sort_keys=True)