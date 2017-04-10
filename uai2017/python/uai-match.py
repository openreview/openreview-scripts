#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
import csv
import sys
import json
import numpy as np
from collections import defaultdict

import openreview
import openreview_matcher
import match_utils

from uaidata import *

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-i','--data', help='the name of the .pkl file (without extension) containing existing OpenReview data. Defaults to ./metadata.pkl')
parser.add_argument('-o','--outdir', help='the directory for output .csv files to be saved. Defaults to current directory.')
parser.add_argument('-c','--config', help='the .json file (WITH extension) containing the match configuration.', required=True)
parser.add_argument('-m','--mode', help="choose either \"reviewers\" or \"areachairs\"", required=True)

parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")

args = parser.parse_args()

mode = args.mode
outdir = '.' if not args.outdir else args.outdir

with open(args.config) as data_file:
    config = json.load(data_file)

if args.data:
    datapath = args.data
else:
    datapath = './metadata'

try:
    data = match_utils.load_obj(datapath)
except IOError as e:
    raise Exception("local metadata file not found. Please run uai-metadata.py first.")


# Data should look like this:
#
# {
#     'reviewers_group': reviewers_group,
#     'areachairs_group': areachairs_group,
#     'papers_by_forum': papers_by_forum,
#     'originals_by_forum': originals_by_forum,
#     'originalforum_by_paperforum': originalforum_by_paperforum,
#     'metadata_by_forum': metadata_by_forum,
#     'metadata_by_reviewer': metadata_by_reviewer,
#     'metadata_by_areachair': metadata_by_areachair,
#     'domains_by_user': domains_by_user,
#     'domains_by_email': domains_by_email,
#     'bids_by_forum': bids_by_forum,
#     'recs_by_forum': recs_by_forum,
#     'registered_expertise_by_reviewer': registered_expertise_by_reviewer
#     'registered_expertise_by_ac': registered_expertise_by_ac
# }

reviewers_group = data['reviewers_group']
areachairs_group = data['areachairs_group']
papers_by_forum = data['papers_by_forum']
originals_by_forum = data['originals_by_forum']
originalforum_by_paperforum = data['originalforum_by_paperforum']
metadata_by_forum = data['metadata_by_forum']
metadata_by_reviewer = data['metadata_by_reviewer']
metadata_by_areachair = data['metadata_by_areachair']
domains_by_user = data['domains_by_user']
domains_by_email = data['domains_by_email']
bids_by_forum = data['bids_by_forum']
recs_by_forum = data['recs_by_forum']
registered_expertise_by_reviewer = data['registered_expertise_by_reviewer']
registered_expertise_by_ac = data['registered_expertise_by_ac']

missing_reviewer_expertise = set()
missing_areachair_expertise = set()
conflicts = set()

# .............................................................................
#
# Initialize Metadata
#
# Initialize the metadata in OpenReview by creating notes
# .............................................................................

# Pre-populate all the paper metadata notes

empty_paper_note_content = {
    'reviewers': [],
    'areachairs': [],
    'papers': []
}

print "Resetting Paper Metadata"
for n in papers_by_forum.values():
    if n.forum not in metadata_by_forum:
        metadata_by_forum[n.forum] = openreview.Note(
          invitation = CONFERENCE + "/-/Paper/Metadata",
          readers = [COCHAIRS, CONFERENCE],
          forum = n.forum,
          writers = [CONFERENCE],
          content = empty_paper_note_content,
          signatures = [CONFERENCE]
        )
    else:
        metadata_by_forum[n.forum].content = empty_paper_note_content

# Pre-populate all the reviewer metadata notes

print "Resetting Reviewer Metadata"
for r in reviewers_group.members:

    empty_reviewer_note_content = {
        'name': r,
        'reviewers': []
    }

    if r not in metadata_by_reviewer:
        metadata_by_reviewer[r] = openreview.Note(
            invitation=CONFERENCE + "/-/Reviewer/Metadata",
            readers=[COCHAIRS, CONFERENCE],
            writers=[CONFERENCE],
            content= empty_reviewer_note_content,
            signatures=[CONFERENCE]
        )
    else:
        metadata_by_reviewer[r].content = empty_reviewer_note_content

# Pre-populate all the area chair metadata notes
print "Resetting Areachair Metadata"
for a in areachairs_group.members:

    empty_areachair_note_content = {
        'name': a,
        'areachairs': []
    }

    if a not in metadata_by_areachair:
        metadata_by_areachair[a] = openreview.Note(
            invitation=CONFERENCE + "/-/Area_Chair/Metadata",
            readers=[COCHAIRS, CONFERENCE],
            writers=[CONFERENCE],
            content=empty_areachair_note_content,
            signatures=[CONFERENCE]
        )
    else:
        metadata_by_areachair[a].content = empty_areachair_note_content

# .............................................................................
#
# Populate Paper Metadata
#
# .............................................................................

# Populate Paper metadata notes
print "Populating paper metadata..."

for n in papers_by_forum.values():
    forum = n.forum
    reviewer_metadata = []
    areachair_metadata = []
    paper_metadata = []
    paper_note = n
    original_note = originals_by_forum[originalforum_by_paperforum[forum]]

    for bid in bids_by_forum[forum]:
        if bid.signatures[0] in reviewers_group.members:
            reviewer_metadata.append({
                'user': bid.signatures[0],
                'score': config['bid_score_map'][bid.tag],
                'source': 'ReviewerBid'
            })
        if bid.signatures[0] in areachairs_group.members:
            areachair_metadata.append({
                'user': bid.signatures[0],
                'score': config['bid_score_map'][bid.tag],
                'source': 'AreachairBid'
            })

    for bid in recs_by_forum[forum]:
        reviewer_metadata.append({
            'user': bid.tag,
            'score': config['recommendation_score'],
            'source': 'AreachairRec'
        })

    # Compute paper-paper affinity by subject area overlap
    for m in papers_by_forum.values():
        paper_subjects_A = paper_note.content['subject areas']
        paper_subjects_B = m.content['subject areas']
        paper_paper_affinity = match_utils.subject_area_overlap(paper_subjects_A, paper_subjects_B)

        if paper_paper_affinity > 0:
            paper_metadata.append({
                'submissionId': paper_note.number,
                'score': paper_paper_affinity,
                'source': 'SubjectAreaOverlap'
            })

    # Get paper-reviewer affinity scores
    for reviewer in reviewers_group.members:
        if reviewer in registered_expertise_by_reviewer.keys():
            paper_subjects = paper_note.content['subject areas']
            primary_subjects = registered_expertise_by_reviewer[reviewer].get('primary area', [])
            secondary_subjects = registered_expertise_by_reviewer[reviewer].get('additional areas', [])

            primary_affinity = match_utils.subject_area_overlap(primary_subjects, paper_subjects)
            secondary_affinity = match_utils.subject_area_overlap(secondary_subjects, paper_subjects)

            reviewer_affinity = (primary_affinity * config['reviewer_primary_weight']) + (secondary_affinity * (1-config['reviewer_primary_weight']))

            if reviewer_affinity > 0:
                reviewer_metadata.append({
                    'user': reviewer,
                    'score': reviewer_affinity,
                    'source': 'SubjectAreaOverlap'
                })
        else:
            missing_reviewer_expertise.update([reviewer])

    # Get paper-areachair affinity scores
    for areachair in areachairs_group.members:
        if areachair in registered_expertise_by_ac.keys():
            paper_subjects = paper_note.content['subject areas']
            primary_subjects = registered_expertise_by_ac[areachair].get('primary area', [])
            secondary_subjects = registered_expertise_by_ac[areachair].get('additional areas', [])

            primary_affinity = match_utils.subject_area_overlap(primary_subjects, paper_subjects)
            secondary_affinity = match_utils.subject_area_overlap(secondary_subjects, paper_subjects)

            ac_affinity = (primary_affinity * config['areachair_primary_weight']) + (secondary_affinity * (1-config['areachair_primary_weight']))

            if ac_affinity > 0:
                areachair_metadata.append({
                    'user': areachair,
                    'score': ac_affinity,
                    'source': 'SubjectAreaOverlap'
                })
        else:
            missing_areachair_expertise.update([a])

    # Get conflicts of interest

    # ... for authors
    author_emails = original_note.content['authorids']
    author_domain_set = set()
    for e in author_emails:
        author_domain_set.update(domains_by_email[e])

    # ... for reviewers
    for reviewer in reviewers_group.members:

        reviewer_domain_set = set()
        reviewer_domain_set.update(domains_by_user[reviewer])

        for exception in config['conflict_exceptions']:
            if exception in author_domain_set: author_domain_set.remove(exception)
            if exception in reviewer_domain_set: reviewer_domain_set.remove(exception)

        intersection = int(len(reviewer_domain_set & author_domain_set))

        if intersection > 0:
            conflicts.update([(reviewer, paper_note.number)])
            reviewer_metadata.append({
                'user': reviewer,
                'score': config['conflict_score'],
                'source': 'ConflictOfInterest'
            })

    # ... for areachairs
    for areachair in areachairs_group.members:
        areachair_domain_set = set()
        areachair_domain_set.update(domains_by_user[areachair])

        for exception in config['conflict_exceptions']:
            if exception in author_domain_set: author_domain_set.remove(exception)
            if exception in areachair_domain_set: areachair_domain_set.remove(exception)

        intersection = int(len(areachair_domain_set & author_domain_set))

        if intersection > 0:
            conflicts.update([(areachair, paper_note.number)])
            areachair_metadata.append({
                'user': areachair,
                'score': config['conflict_score'],
                'source': 'ConflictOfInterest'
            })


    metadata_by_forum[forum].content['minreviewers'] = config['minreviewers']
    metadata_by_forum[forum].content['maxreviewers'] = config['maxreviewers']
    metadata_by_forum[forum].content['minareachairs'] = config['minareachairs']
    metadata_by_forum[forum].content['maxareachairs'] = config['maxareachairs']
    metadata_by_forum[forum].content['reviewers'] = reviewer_metadata
    metadata_by_forum[forum].content['areachairs'] = areachair_metadata
    metadata_by_forum[forum].content['papers'] = paper_metadata
    metadata_by_forum[forum].content['title'] = paper_note.content['title']


print "%s conflicts detected. Writing %s/conflicts.csv" % (len(conflicts), outdir)
with open('%s/conflicts.csv' % outdir, 'w') as outfile:
    csvwriter = csv.writer(outfile)
    for conflict in conflicts:
        csvwriter.writerow([conflict[0].encode('utf-8'), conflict[1]])


print "Missing %s of %s areachair expertise areas. Writing %s/missing_areachair_expertise.csv" % (len(missing_areachair_expertise), len(areachairs_group.members), outdir)
with open('%s/missing_areachair_expertise.csv' % outdir, 'w') as outfile:
    csvwriter = csv.writer(outfile)
    for areachair in missing_areachair_expertise:
        csvwriter.writerow([areachair.encode('utf-8')])


print "Missing %s of %s reviewer expertise areas. Writing %s/missing_reviewer_expertise.csv" % (len(missing_reviewer_expertise), len(reviewers_group.members), outdir)
with open('%s/missing_reviewer_expertise.csv' % outdir, 'w') as outfile:
    csvwriter = csv.writer(outfile)
    for reviewer in missing_reviewer_expertise:
        csvwriter.writerow([reviewer.encode('utf-8')])

# .............................................................................
#
# Populate User Metadata
#
# .............................................................................


# Organize data
print "Generating reviewer metadata..."
for n in metadata_by_reviewer.values():
    n.content['maxpapers'] = config['max_reviewer_papers']
    n.content['minpapers'] = config['min_reviewer_papers']

    reviewer_similarities = []
    for reviewer in reviewers_group.members:

        try:
            primary_subjects_A = registered_expertise_by_reviewer[reviewer].get('primary area', [])
            secondary_subjects_A = registered_expertise_by_reviewer[reviewer].get('additional areas', [])

            primary_subjects_B = registered_expertise_by_reviewer[n.content['name']].get('primary area', [])
            secondary_subjects_B = registered_expertise_by_reviewer[n.content['name']].get('additional areas', [])

            primary_affinity = match_utils.subject_area_overlap(primary_subjects_A, primary_subjects_B)
            secondary_affinity = match_utils.subject_area_overlap(secondary_subjects_A, secondary_subjects_B)

            reviewer_affinity = (primary_affinity * config['reviewer_primary_weight']) + (secondary_affinity * (1-config['reviewer_primary_weight']))

            if reviewer_affinity > 0:
                reviewer_similarities.append({
                    'user': reviewer,
                    'score': reviewer_affinity,
                    'source': 'SubjectAreaOverlap'
                })

        except KeyError:
            pass

    n.content['reviewers'] = reviewer_similarities

    metadata_by_reviewer[n.content['name']] = n

print "Generating areachair metadata..."
for n in metadata_by_areachair.values():
    n.content['maxpapers'] = config['max_areachair_papers']
    n.content['minpapers'] = config['min_areachair_papers']

    areachair_similarities = []
    for areachair in areachairs_group.members:
        try:
            primary_subjects_A = registered_expertise_by_ac[areachair].get('primary area', [])
            secondary_subjects_A = registered_expertise_by_ac[areachair].get('additional areas', [])

            primary_subjects_B = registered_expertise_by_ac[n.content['name']].get('primary area', [])
            secondary_subjects_B = registered_expertise_by_ac[n.content['name']].get('additional areas', [])

            primary_affinity = match_utils.subject_area_overlap(primary_subjects_A, primary_subjects_B)
            secondary_affinity = match_utils.subject_area_overlap(secondary_subjects_A, secondary_subjects_B)

            areachair_affinity = (primary_affinity * config['reviewer_primary_weight']) + (secondary_affinity * (1-config['reviewer_primary_weight']))

            if areachair_affinity > 0:
                areachair_similarities.append({
                    'user': areachair,
                    'score': areachair_affinity,
                    'source': 'SubjectAreaOverlap'
                })

        except KeyError as e:
            pass

    n.content['areachairs'] = areachair_similarities
    metadata_by_areachair[n.content['name']] = n


# .............................................................................
#
# Match Reviewers or Areachairs
#
# .............................................................................

if mode == 'reviewers':
    user_group = reviewers_group
    metadata_group_name = 'reviewers'
    user_metadata_notes = metadata_by_reviewer.values()

if mode == 'areachairs':
    user_group = areachairs_group
    metadata_group_name = 'areachairs'
    user_metadata_notes = metadata_by_areachair.values()

filtered_paper_metadata_notes = [n for n in metadata_by_forum.values() if n.forum in papers_by_forum]
matcher = openreview_matcher.Matcher(user_group, papers_by_forum.values(), user_metadata_notes, filtered_paper_metadata_notes, metadata_group_name)


assignments = matcher.solve()

print 'Writing %s/uai_%s_match.csv' % (outdir, mode)
with open('%s/uai_%s_match.csv' % (outdir, mode), 'w') as outfile:
    csvwriter = csv.writer(outfile)
    for a in assignments:
        csvwriter.writerow([a[0].encode('utf-8'),a[1]])

outdata = {
    'reviewers_group': reviewers_group,
    'areachairs_group': areachairs_group,
    'papers_by_forum': papers_by_forum,
    'originals_by_forum': originals_by_forum,
    'originalforum_by_paperforum': originalforum_by_paperforum,
    'metadata_by_forum': metadata_by_forum,
    'metadata_by_reviewer': metadata_by_reviewer,
    'metadata_by_areachair': metadata_by_areachair,
    'domains_by_user': domains_by_user,
    'domains_by_email': domains_by_email,
    'bids_by_forum': bids_by_forum,
    'recs_by_forum': recs_by_forum,
    'registered_expertise_by_reviewer': registered_expertise_by_reviewer,
    'registered_expertise_by_ac': registered_expertise_by_ac
}

print "Saving local metadata to %s.pkl" % datapath
match_utils.save_obj(outdata, datapath)

print "Done"
