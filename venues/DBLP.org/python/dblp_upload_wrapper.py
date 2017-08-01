#!/usr/bin/python

"""
mcz - August 2017
This script reads in DBLP XML data and inserts a new
record or a revision to an existing record.

It processes all .xml files for the file path passed in.

The DBLP data can be downloaded from : http://dblp.dagstuhl.de/xml/

Which is a LARGE file. To process, split the XML using xml_split so there is one
record per file:

    xml_split dblp.xml

The xml_split command creates a file that allows xml_merge to recreate the
original XML, we don't want to process that file so remove it:

    rm dblp-00.xml

Then created sub-folders and put 10K files in each folder.

To create the folders:

    for i in {0..600}; do mkdir $i; done;

To move the files, 10k at a time:

    for i in {1..600}; do mv dblp-$i????.xml ./$i; done;

then move the stragglers:

    mv dblp-*.xml ./0

"""

## Import statements
import argparse
import sys
from openreview import *
import os
import traceback
import glob

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--dir', help="Folder containing XML files, all will be processed.");

args = parser.parse_args()
## Initialize the client library with username and password
if args.username != None and args.password != None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

count = 0
error_count = 0
for file in glob.glob(args.dir + "/*.xml"):
    count += 1
    try:
        f = open(file)
        xml = f.read()
        rec = openreview.post_dblp_record({'dblp' : xml})
        # print rec
        if rec.get('message'):
            print rec['message']
        elif rec.get('referent'):
            print 'Created reference for: ' + rec['content']['paperhash']
        else:
            print 'New note for: ' + rec['content']['paperhash']


    except :
        # write the error out with a ".err" extension.
        error_count += 1
        print "Error in : " + file + " : " + xml
        exc_type, exc_value, exc_traceback = sys.exc_info()
        f = open(file + ".err",  "a", 0)
        f.write(str(xml) + os.linesep)
        traceback.print_tb(exc_traceback, None, file=f)
        f.write(os.linesep)
        f.close()

    if not (count % 100):
        print count

print
print str(count) + " files read."
print "There were " + str(error_count) + " error(s)."

