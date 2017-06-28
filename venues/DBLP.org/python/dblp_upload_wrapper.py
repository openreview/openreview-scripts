#!/usr/bin/python

"""

This script reads in DBLP JSON data and inserts a new
record or a revision to an existing record.

"""

## Import statements
import argparse
import csv
import sys
from openreview import *
import update_records
import json
import os
import traceback

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite',
                    help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--json', help="File containint a list of DBLP JSON objects.")

args = parser.parse_args()
## Initialize the client library with username and password
if args.username != None and args.password != None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

dblp_inv = openreview.get_invitation('DBLP.org/-/paper')

data = json.loads(open(args.json).read())

count = 0
for d in data:
    count += 1
    try:

        ## Use the post_or_update function to post a new record
        dblp_record = update_records.post_or_update(openreview, d, verbose=True)
    except :
        print "Error in : " + args.json + " : " + str(d)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # get the json file name
        fp = args.json.split('/')
        f = open("./" + fp.pop() + ".err",  "a", 0)
        f.write("line: " + str(count) + " : " + str(d) + os.linesep)
        traceback.print_tb(exc_traceback, None, file=f)
        f.write(os.linesep)
        f.close()

    print count
