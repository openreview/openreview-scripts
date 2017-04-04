#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
import csv
import sys
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
parser.add_argument('--minusers', help="the minimum number of users assigned per paper (default 1)")
parser.add_argument('--maxusers', help="the maximum number of users assigned per paper (default 3)")
parser.add_argument('--minpapers', help="the minimum number of papers assigned per user (default 0)")
parser.add_argument('--maxpapers', help="the maximum number of papers assigned per user (default 5)")
parser.add_argument('-o','--outdir', help="directory to write uai_assignments.csv")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client()


# .............................................................................
#
# Metadata init
#
# .............................................................................

print "Obtaining submission data..."
overwrite = args.overwrite and args.overwrite.lower()=='true'

submissions = client.get_notes(invitation = CONFERENCE+"/-/blind-submission")

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






# .............................................................................
#
# Populate Paper Metadata
#
# .............................................................................

bid_score_map = {
 'I want to review': 1.0,
 'I can review': 0.75,
 'I can probably review but am not an expert': 0.5,
 'I cannot review': '-inf',
 'No bid': 0.0
}

## Reviewer-relevant data
print "Obtaining reviewer-relevant data..."
reviewers = client.get_group(PC)
profile_expertise_by_reviewer = {}
registered_expertise_by_reviewer = {}

for r in [x for x in reviewers.members if '~' in x]:
    profile = client.get_profile(r)
    profile_expertise_by_reviewer[r] = profile.content['expertise']

reviewer_reg_responses = client.get_notes(invitation='auai.org/UAI/2017/-/Reviewer_Expertise')
for reg in reviewer_reg_responses:
    registered_expertise_by_reviewer[reg.signatures[0]] = reg.content

missing_reviewer_reg = set()

## Areachair-relevant data
print "Obtaining areachair-relevant data..."
areachairs = client.get_group(SPC)
profile_expertise_by_ac = {}
registered_expertise_by_ac = {}

for a in [x for x in areachairs.members if '~' in x]:
    profile = client.get_profile(a)
    profile_expertise_by_ac[a] = profile.content['expertise']

spc_reg_responses = client.get_notes(invitation='auai.org/UAI/2017/-/SPC_Expertise')
for reg in spc_reg_responses:
    registered_expertise_by_ac[reg.signatures[0]] = reg.content

missing_spc_reg = set()

## Bid-relevant data
bids = client.get_tags(invitation='auai.org/UAI/2017/-/Add/Bid')
metadata_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Paper/Metadata')
metadata_by_id = {n.forum:n for n in metadata_notes}


print "Processing submissions..."
submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
submissions_by_forum = {n.forum: n for n in submissions}
recs = []
for n in submissions:
    recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % n.number)

print "Processing bids... (this may take a while)"
bids_by_id = defaultdict(list)
for b in bids:
    try:
        n = submissions_by_forum[b.forum]
        bids_by_id[n.forum].append(b)
    except KeyError as e:
        print "Bid found on deleted paper: ", b.forum

print "Processing recommendations..."
recs_by_id = defaultdict(list)
for r in recs:
    try:
        n = submissions_by_forum[r.forum]
        recs_by_id[n.forum].append(r)
    except KeyError as e:
        print "Recommendation found on deleted paper: ", r.forum


print "Populating metadata notes..."

# Populate Metadata notes
# .............................................................................

for n in metadata_notes:
    forum = n.forum
    reviewer_metadata = []
    areachair_metadata = []
    paper_metadata = []
    paper_note = client.get_note(forum)

    for bid in bids_by_id[forum]:

        if bid.signatures[0] in reviewers.members:
            reviewer_metadata.append({
                'user': bid.signatures[0],
                'score': bid_score_map[bid.tag],
                'source': 'ReviewerBid'
            })
        if bid.signatures[0] in areachairs.members:
            areachair_metadata.append({
                'user': bid.signatures[0],
                'score': bid_score_map[bid.tag],
                'source': 'AreachairBid'
            })

    for bid in recs_by_id[forum]:
        reviewer_metadata.append({
            'user': bid.tag,
            'score': '+inf',
            'source': 'AreachairRec'
        })

    # The following for loop is needed until we have a real way of getting paper-paper scores
    for m in metadata_notes:
        paper_metadata.append({
            'submissionId': paper_note.number,
            'score': 1.0 if m.forum == n.forum else 0.0,
            'source': 'DummyModel'
        })

    # The following for loop is needed until we have a real way of getting reviewer-paper scores
    for reviewer in reviewers.members:
        if reviewer in registered_expertise_by_reviewer.keys():
            registered_reviewer = reviewer
            reviewer_affinity = match_utils.subject_area_affinity(
                paper_note.content['subject areas'],
                registered_expertise_by_reviewer[registered_reviewer]['primary area'],
                registered_expertise_by_reviewer[registered_reviewer]['additional areas'],
                primary_weight = 0.7
            )

            reviewer_metadata.append({
                'user': registered_reviewer,
                'score': reviewer_affinity,
                'source': 'SubjectAreaOverlap'
            })
        else:
            missing_reviewer_reg.update([reviewer])

    for a in areachairs.members:
        if a in registered_expertise_by_ac.keys():
            registered_ac = a
            ac_affinity = match_utils.subject_area_affinity(
                paper_note.content['subject areas'],
                registered_expertise_by_ac[registered_ac]['primary area'],
                registered_expertise_by_ac[registered_ac]['additional areas'],
                primary_weight = 0.7
            )

            areachair_metadata.append({
                'user': registered_ac,
                'score': ac_affinity,
                'source': 'SubjectAreaOverlap'
            })
        else:
            missing_spc_reg.update([a])

    metadata_by_id[forum].content['minreviewers'] = 1
    metadata_by_id[forum].content['maxreviewers'] = 3
    metadata_by_id[forum].content['minareachairs'] = 0
    metadata_by_id[forum].content['maxareachairs'] = 1
    metadata_by_id[forum].content['reviewers'] = reviewer_metadata
    metadata_by_id[forum].content['areachairs'] = areachair_metadata
    metadata_by_id[forum].content['papers'] = paper_metadata
    metadata_by_id[forum].content['title'] = paper_note.content['title']

    client.post_note(metadata_by_id[forum])

print "Done."
print ''
print "Missing %s of %s areachair expertise areas: " % (len(list(missing_spc_reg)), len(areachairs.members))
for spc in list(missing_spc_reg):
    print spc

print ''
print "Missing %s of %s reviewer expertise areas: " % (len(list(missing_reviewer_reg)), len(reviewers.members))
for reviewer in list(missing_reviewer_reg):
    print reviewer



# .............................................................................
#
# Populate User Metadata
#
# .............................................................................


# Organize data

reviewers = client.get_group(PC)
reviewer_metadata_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Reviewer/Metadata')
reviewer_metadata_by_id = {n.forum:n for n in reviewer_metadata_notes}

print "Generating reviewer metadata..."
for n in reviewer_metadata_notes:
    n.content['maxpapers'] = 3
    n.content['minpapers'] = 0

    reviewer_similarities = []
    for reviewer in reviewers.members:
        reviewer_similarities.append({
            'user': reviewer,
            'score': 1.0 if reviewer == n.content['name'] else 0,
            'source': 'DummyModel'
        })

    n.content['reviewers'] = reviewer_similarities

    client.post_note(n)

areachairs = client.get_group(SPC)
areachair_metadata_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Area_Chair/Metadata')
areachair_metadata_by_id = {n.forum:n for n in areachair_metadata_notes}

print "Generating areachair metadata..."
for n in areachair_metadata_notes:
    areachair_similarities = []
    for areachair in areachairs.members:
        areachair_similarities.append({
            'user': areachair,
            'score': 1.0 if areachair == n.content['name'] else 0,
            'source': 'DummyModel'
        })

    n.content['areachairs'] = areachair_similarities
    client.post_note(n)

# .............................................................................
#
# Match Reviewers or Areachairs
#
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
        csvwriter.writerow([a[0].encode('utf-8'),a[1]])
print "Done"
