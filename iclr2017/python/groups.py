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
import sys
sys.path.append('../..')
from client import *

## Import statements and argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-g','--group', help="The group (or regex expression for a set of groups) to examine. (Example: ICLR.cc/2017/.* searches for all groups starting with ICLR.cc/2017/)")
parser.add_argument('-o','--output', help="The directory to save the output file")
parser.add_argument('-f','--format', help="The file format to save. Choose either json or csv.")
args = parser.parse_args()

## Initialize the client library with username and password
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass()
or3 = Client(username,password)


groups = json.loads(or3.get_group({'regex':args.group}).text)['groups']
print groups
print groups[0]
if args.output!=None and args.format.lower()=="json":
    with open(args.output, 'w') as outfile:
        json.dump(groups, outfile, indent=4, sort_keys=True)
else:
    print json.dumps(groups, indent=4, sort_keys=True)


if args.output!=None and args.format.lower()=="csv":
    with open(args.output, 'w') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['original_id, members, readers, nonreaders'])
        fmt = '%s%25s%25s%25s'
        for count, group in enumerate(groups):
            csvwriter.writerow(fmt % (groups[count]['origId'], groups[count]['members'], groups[count]['readers'],groups[count]['nonreaders']))

# with open(write_dir, 'wb') as csvfile:
#        csvwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#        for observation in data_to_write:
#                csvwriter.writerow([observation.time,observation.feature_vector])