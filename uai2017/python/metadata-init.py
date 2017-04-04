#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
import csv
import sys
import openreview

from uaidata import *

# Handle the arguments and initialize openreview client
# .............................................................................
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client()

# Main Script
# .............................................................................

print "Obtaining submission data..."
overwrite = args.overwrite and args.overwrite.lower()=='true'

submissions = client.get_notes(invitation=CONFERENCE+"/-/blind-submission")

existing_paper_metadata = client.get_notes(invitation=CONFERENCE + "/-/Paper/Metadata")
metadata_by_forum = {n.forum: n for n in existing_paper_metadata}

# Pre-populate all the paper metadata notes
print "Overwriting paper metadata..." if overwrite else "Generating Paper Metadata..."
for n in submissions:
    if n.forum not in metadata_by_forum:
        metadata = openreview.Note(
          invitation = CONFERENCE + "/-/Paper/Metadata",
          readers = [COCHAIRS, CONFERENCE],
          forum = n.id,
          writers = [CONFERENCE],
          content = {'reviewers':[], 'areachairs':[], 'papers':[]},
          signatures = [CONFERENCE]
        )
        client.post_note(metadata)
    elif overwrite:
        metadata = metadata_by_forum[n.forum]
        metadata.content['reviewers'] = []
        metadata.content['areachairs'] = []
        metadata.content['papers'] = []
        client.post_note(metadata)

# Pre-populate all the reviewer metadata notes
reviewers = client.get_group(PC).members
existing_reviewer_metadata = client.get_notes(invitation = CONFERENCE + "/-/Reviewer/Metadata")
metadata_by_reviewer = {u.content['name']: u for u in existing_reviewer_metadata}

print "Overwriting reviewer metadata..." if overwrite else "Generating reviewer metadata..."
for r in reviewers:
    if r not in metadata_by_reviewer:
        metadata = openreview.Note(
            invitation=CONFERENCE + "/-/Reviewer/Metadata",
            readers=[COCHAIRS, CONFERENCE],
            writers=[CONFERENCE],
            content={'name':r, 'reviewers':[]},
            signatures=[CONFERENCE]
        )
        client.post_note(metadata)
    elif overwrite:
        metadata = metadata_by_reviewer[r]
        metadata.content['reviewers'] = []
        client.post_note(metadata)


# Pre-populate all the area chair metadata notes
areachairs = client.get_group(SPC).members
existing_areachair_metadata = client.get_notes(invitation = CONFERENCE + "/-/Area_Chair/Metadata")
metadata_by_areachair = {u.content['name']: u for u in existing_areachair_metadata}

print "Overwriting areachair metadata..." if overwrite else "Generating areachair metadata..."
for a in areachairs:
    if a not in metadata_by_areachair:
        metadata = openreview.Note(
            invitation=CONFERENCE + "/-/Area_Chair/Metadata",
            readers=[COCHAIRS, CONFERENCE],
            writers=[CONFERENCE],
            content={'name':a, 'areachairs':[]},
            signatures=[CONFERENCE]
        )
        client.post_note(metadata)
    elif overwrite:
        metadata = metadata_by_areachair[a]
        metadata.content['areachairs'] = []
        client.post_note(metadata)
