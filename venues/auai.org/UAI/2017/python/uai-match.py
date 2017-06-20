#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
import csv
import openreview
import match_utils
import openreview_matcher
from collections import defaultdict
from uaidata import *

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-g','--group', help='the ID of the group to match (required)', required=True)
parser.add_argument('-d','--data', help='the .pkl file (with extension) containing existing OpenReview data')
parser.add_argument('-o','--outdir', help='the directory for output .csv files to be saved. Defaults to current directory')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")

args = parser.parse_args()

outdir = '.' if not args.outdir else args.outdir

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

if args.data == None:
    datafile = './metadata.pkl'
else:
    datafile = args.data

try:
    data = match_utils.load_obj(datafile)
    group = data['user_groups'][args.group]
    papers = data['papers']
    paper_metadata = data['paper_metadata']
except:
    print "datafile not found. retrieving data from ", client.baseurl
    group = client.get_group(args.group)
    papers = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
    paper_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Paper/Metadata')

## Settings (move this outside at some point)
matching_configuration = {
    "group": group.id,
    "invitation": 'auai.org/UAI/2017/-/blind-submission',
    "minusers": 3,
    "maxusers": 5,
    "minpapers": 1,
    "maxpapers": 15,
    "weights": {
        "primary_subject_overlap": 0,
        "secondary_subject_overlap": 0,
        "bid_score": 0,
        "ac_recommendation": 0,
        "tfidf": 1
    }
}

## Solve the matcher
matcher = openreview_matcher.Matcher(group=group, papers=papers, metadata=paper_metadata, config=matching_configuration)
assignments = matcher.solve()

## Write assignments to CSV
outfile = outdir + '/uai-assignments-redesigned.csv'
print "writing assignments to ", outfile
with open(outfile, 'w') as o:
    csvwriter = csv.writer(o)
    for a in assignments:
        csvwriter.writerow([a[0].encode('utf-8'),a[1]])

## Post a note with the configuration and assignments for later use
forum_by_number = {n.number: n.forum for n in papers}

assignments_by_forum = defaultdict(list)
for n in assignments:
    user = n[0]
    forum = forum_by_number[n[1]]
    assignments_by_forum[forum].append(user)

assignment_info_by_number = {}
for n in papers:
    assignment_info_by_number['Paper{0}'.format(n.number)] = {
        'title': n.content['title'],
        'forum': n.forum,
        'assigned': assignments_by_forum[n.forum]
    }

assignment_content = {
    "configuration": matching_configuration,
    "assignments": assignment_info_by_number
}

assignment_note = openreview.Note(
        content = assignment_content,
        invitation = 'auai.org/UAI/2017/-/Matching/Assignments',
        readers = ['auai.org/UAI/2017'],
        writers = ['auai.org/UAI/2017'],
        signatures = ['auai.org/UAI/2017']
    )

client.post_note(assignment_note)

