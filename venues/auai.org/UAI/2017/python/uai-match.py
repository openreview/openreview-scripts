#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
import csv
import openreview
import match_utils
import openreview_matcher
from uaidata import *

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-i','--data', help='the .pkl file (with extension) containing existing OpenReview data. Defaults to ./metadata.pkl')
parser.add_argument('-o','--outdir', help='the directory for output .csv files to be saved. Defaults to current directory.')

parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")

args = parser.parse_args()

outdir = '.' if not args.outdir else args.outdir

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

if args.data:
    datapath = args.data
else:
    datapath = './metadata.pkl'

try:
    data = match_utils.load_obj(datapath)
except IOError as e:
    raise Exception("local metadata file not found. Please run uai-metadata.py first.")


## Main processing

matching_configuration = {
    "minusers": 1,
    "maxusers": 4,
    "minpapers": 1,
    "maxpapers": 15,
    "weights": [5, 3, 1]
}



matching_args = {
    'group': data['user_groups']['auai.org/UAI/2017/Program_Committee'],
    'papers': data['papers_to_match'],
    'metadata': data['paper_metadata'],
    'config': matching_configuration
}

matcher = openreview_matcher.Matcher(**matching_args)
assignments = matcher.solve()

with open(outdir + '/uai-assignments-redesigned.csv', 'w') as outfile:
    csvwriter = csv.writer(outfile)
    for a in assignments:
        csvwriter.writerow([a[0].encode('utf-8'),a[1]])


