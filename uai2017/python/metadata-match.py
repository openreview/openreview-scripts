import argparse
import sys
import os
import csv
import numpy as np
import openreview
import openreview_matcher
from collections import defaultdict
from uaidata import *
import match_utils

# Parse the arguments for user authentication
# .............................................................................
parser = argparse.ArgumentParser()
parser.add_argument('--mode', help="choose either \"reviewers\" or \"areachairs\"")
parser.add_argument('--minusers', help="the minimum number of users assigned per paper (default 1)")
parser.add_argument('--maxusers', help="the maximum number of users assigned per paper (default 3)")
parser.add_argument('--minpapers', help="the minimum number of papers assigned per user (default 0)")
parser.add_argument('--maxpapers', help="the maximum number of papers assigned per user (default 5)")
parser.add_argument('-o','--outdir', help="directory to write uai_assignments.csv")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()
if args.username != None and args.password != None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)

# Set the parameters
# .............................................................................

params = {'minusers': None, 'maxusers': None}
mode = args.mode.lower() if args.mode else 'reviewers'

params['minusers'] = int(args.minusers) if args.minusers else 1
params['maxusers'] = int(args.maxusers) if args.maxusers else 3
params['minpapers'] = int(args.minpapers) if args.minpapers else 0
params['maxpapers'] = int(args.maxpapers) if args.maxpapers else 5

if mode == 'reviewers':
    user_group = client.get_group(PC)
    params['metadata_group'] = 'reviewers'
    user_metadata_notes = client.get_notes(invitation = CONFERENCE+"/-/Reviewer/Metadata")

if mode == 'areachairs':
    user_group = client.get_group(SPC)
    params['metadata_group'] = 'areachairs'
    user_metadata_notes = client.get_notes(invitation = CONFERENCE+"/-/Area_Chair/Metadata")

blind_submissions = client.get_notes(invitation = CONFERENCE+"/-/blind-submission")
paper_metadata_notes = client.get_notes(invitation = CONFERENCE+"/-/Paper/Metadata")

matcher = openreview_matcher.Matcher(user_group, blind_submissions, user_metadata_notes, paper_metadata_notes, params)
assignments = matcher.solve()

outdir = args.outdir if args.outdir else '.'

print 'Writing %s/uai_%s_match.csv' % (outdir, mode)
with open('%s/uai_%s_match.csv' % (outdir, mode), 'w') as outfile:
    csvwriter = csv.writer(outfile)
    for a in assignments:
        csvwriter.writerow([a[0],a[1]])
print "Done"

