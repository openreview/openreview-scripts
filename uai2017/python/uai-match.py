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
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--mode', help="choose either \"reviewers\" or \"areachairs\"")
parser.add_argument('-c', '--configfile', help="the JSON configuration file")
parser.add_argument('-o','--outdir', help="directory to write uai_assignments.csv")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client()

if args.configfile:
    with open(args.configfile) as f:
        config = json.load(f)
else:
    defaultconfig = {
        'reviewer_primary_weight': 0.7,
        'areachair_primary_weight': 0.7,
        'recommendation_score': '+inf',
        'minreviewers': 1,
        'maxreviewers': 3,
        'minareachairs': 1,
        'maxareachairs': 1,
        'minpapers': 1,
        'maxpapers': 15,
        'bid_score_map': {
             'I want to review': 1.0,
             'I can review': 0.75,
             'I can probably review but am not an expert': 0.5,
             'I cannot review': '-inf',
             'No bid': 0.0
        }
    }
    config = defaultconfig

overwrite = args.overwrite and args.overwrite.lower()=='true'
mode = args.mode.lower() if args.mode else 'reviewers'
outdir = args.outdir if args.outdir else '.'

params = {'minusers': None, 'maxusers': None}
params['minusers'] = config['minreviewers'] if mode == 'reviewers' else config['minareachairs']
params['maxusers'] = config['maxreviewers'] if mode == 'reviewers' else config['maxareachairs']
params['minpapers'] = config['minpapers']
params['maxpapers'] = config['maxpapers']

missing_reviewer_expertise = set()
missing_areachair_expertise = set()
conflicts = set()

# API calls
print "Getting paper notes..."
paper_notes = client.get_notes(invitation = CONFERENCE + "/-/blind-submission")
original_notes = client.get_notes(invitation = CONFERENCE + "/-/submission")
print "Getting submission metadata..."
paper_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Paper/Metadata')
print "Getting reviewer metadata..."
reviewer_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer/Metadata')
print "Getting areachair metadata..."
areachair_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Area_Chair/Metadata')
print "Getting reviewer expertise..."
reviewer_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer_Expertise')
print "Getting areachair expertise..."
areachair_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/SPC_Expertise')

reviewers_group = client.get_group(PC)
areachairs_group = client.get_group(SPC)

print "Getting bids..."
bids = client.get_tags(invitation = CONFERENCE + '/-/Add/Bid')

print "Getting areachair recommendations..."
recs = []
for n in paper_notes:
    recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % n.number)

# Indexes
metadata_by_forum = {n.forum: n for n in paper_metadata_notes}
metadata_by_reviewer = {u.content['name']: u for u in reviewer_metadata_notes}
metadata_by_areachair = {u.content['name']: u for u in areachair_metadata_notes}

papers_by_forum = {n.forum: n for n in paper_notes}
originals_by_forum = {n.forum: n for n in original_notes}
originalforum_by_paperforum = {n.forum: n.original for n in paper_notes}

registered_expertise_by_reviewer = {n.signatures[0]: n.content for n in reviewer_expertise_notes}
registered_expertise_by_ac = {n.signatures[0]: n.content for n in areachair_expertise_notes}

# Get conflict information
print "Getting conflict of interesting information... (this may take a while)"
domains_by_user = defaultdict(set)

for reviewer in reviewers_group.members:
    if reviewer not in domains_by_user.keys():
        try:
            reviewer_profile = client.get_profile(reviewer)
            domains_by_user[reviewer] = set([p.split('@')[1] for p in reviewer_profile.content['emails']])
        except openreview.OpenReviewException:
            print "Profile not found for reviewer %s" % reviewer
            pass

for areachair in areachairs_group.members:
    if areachair not in domains_by_user.keys():
        try:
            areachair_profile = client.get_profile(areachair)
            domains_by_user[areachair] = set([p.split('@')[1] for p in areachair_profile.content['emails']])
        except openreview.OpenReviewException:
            print "Profile not found for areachair %s" % areachair
            pass

domains_by_email = defaultdict(set)

for n in original_notes:
    author_emails = n.content['authorids']
    for author_email in author_emails:
        try:
            author_profile = client.get_profile(author_email)
            domains_by_email[author_email] = set([p.split('@')[1] for p in author_profile.content['emails']])
        except openreview.OpenReviewException:
            pass

# .............................................................................
#
# Initialize Metadata
#
# Initialize the metadata in OpenReview by creating notes
# .............................................................................

# Pre-populate all the paper metadata notes
print "Overwriting paper metadata..." if overwrite else "Generating Paper Metadata..."
for n in paper_notes:
    if n.forum not in metadata_by_forum:
        metadata = openreview.Note(
          invitation = CONFERENCE + "/-/Paper/Metadata",
          readers = [COCHAIRS, CONFERENCE],
          forum = n.forum,
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
print "Overwriting reviewer metadata..." if overwrite else "Generating reviewer metadata..."
for r in reviewers_group.members:
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
print "Overwriting areachair metadata..." if overwrite else "Generating areachair metadata..."
for a in areachairs_group.members:
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

paper_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Paper/Metadata')
reviewer_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer/Metadata')
areachair_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Area_Chair/Metadata')

metadata_by_forum = {n.forum: n for n in paper_metadata_notes}
metadata_by_reviewer = {u.content['name']: u for u in reviewer_metadata_notes}
metadata_by_areachair = {u.content['name']: u for u in areachair_metadata_notes}

# .............................................................................
#
# Populate Paper Metadata
#
# .............................................................................

## Bid-relevant data

print "Processing bids..."
bids_by_forum = defaultdict(list)
deleted_papers = set()
for b in bids:
    try:
        n = papers_by_forum[b.forum]
        bids_by_forum[n.forum].append(b)
    except KeyError as e:
        deleted_papers.update([b.forum])

print "Processing recommendations..."
recs_by_forum = defaultdict(list)
for r in recs:
    try:
        n = papers_by_forum[r.forum]
        recs_by_forum[n.forum].append(r)
    except KeyError as e:
        deleted_papers.update([r.forum])


# Populate Paper metadata notes
print "Populating paper metadata... (this may take a while)"

for n in paper_metadata_notes:
    forum = n.forum
    reviewer_metadata = []
    areachair_metadata = []
    paper_metadata = []
    paper_note = papers_by_forum[forum]
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
    for m in paper_metadata_notes:
        paper_subjects_A = paper_note.content['subject areas']
        paper_subjects_B = papers_by_forum[m.forum].content['subject areas']
        paper_paper_affinity = match_utils.subject_area_overlap(paper_subjects_A, paper_subjects_B)

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

            areachair_metadata.append({
                'user': areachair,
                'score': ac_affinity,
                'source': 'SubjectAreaOverlap'
            })
        else:
            missing_areachair_expertise.update([a])

    # Get conflicts of interest
    for reviewer in reviewers_group.members:
        author_emails = original_note.content['authorids']
        author_domain_set = set()
        for e in author_emails:
            author_domain_set.update(domains_by_email[e])

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

    metadata_by_forum[forum].content['minreviewers'] = config['minreviewers']
    metadata_by_forum[forum].content['maxreviewers'] = config['maxreviewers']
    metadata_by_forum[forum].content['minareachairs'] = config['minareachairs']
    metadata_by_forum[forum].content['maxareachairs'] = config['maxareachairs']
    metadata_by_forum[forum].content['reviewers'] = reviewer_metadata
    metadata_by_forum[forum].content['areachairs'] = areachair_metadata
    metadata_by_forum[forum].content['papers'] = paper_metadata
    metadata_by_forum[forum].content['title'] = paper_note.content['title']

    client.post_note(metadata_by_forum[forum])

paper_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Paper/Metadata')
metadata_by_forum = {n.forum: n for n in paper_metadata_notes}

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
for n in reviewer_metadata_notes:
    n.content['maxpapers'] = config['maxpapers']
    n.content['minpapers'] = config['minpapers']

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

            reviewer_similarities.append({
                'user': reviewer,
                'score': reviewer_affinity,
                'source': 'SubjectAreaOverlap'
            })
        except KeyError:
            pass

    n.content['reviewers'] = reviewer_similarities

    client.post_note(n)

reviewer_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer/Metadata')
metadata_by_reviewer = {u.content['name']: u for u in reviewer_metadata_notes}

print "Generating areachair metadata..."
for n in areachair_metadata_notes:
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

            areachair_similarities.append({
                'user': areachair,
                'score': areachair_affinity,
                'source': 'SubjectAreaOverlap'
            })

        except KeyError as e:
            pass

    n.content['areachairs'] = areachair_similarities
    client.post_note(n)

areachair_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Area_Chair/Metadata')
metadata_by_areachair = {u.content['name']: u for u in areachair_metadata_notes}

# .............................................................................
#
# Match Reviewers or Areachairs
#
# .............................................................................

if mode == 'reviewers':
    user_group = reviewers_group
    params['metadata_group'] = 'reviewers'
    user_metadata_notes = reviewer_metadata_notes

if mode == 'areachairs':
    user_group = areachairs_group
    params['metadata_group'] = 'areachairs'
    user_metadata_notes = areachair_metadata_notes

matcher = openreview_matcher.Matcher(user_group, paper_notes, user_metadata_notes, paper_metadata_notes, params)
assignments = matcher.solve()

outdir = args.outdir if args.outdir else '.'

print 'Writing %s/uai_%s_match.csv' % (outdir, mode)
with open('%s/uai_%s_match.csv' % (outdir, mode), 'w') as outfile:
    csvwriter = csv.writer(outfile)
    for a in assignments:
        csvwriter.writerow([a[0].encode('utf-8'),a[1]])
print "Done"
