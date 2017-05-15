
import argparse
from collections import defaultdict

import openreview
import match_utils

from uaidata import *
import uai_features

import openreview_matcher

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--download', help = "the filename (without extension) of the .pkl file to save the downloaded data. Defaults to ./metadata")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

download = './metadata' if args.download == None else args.download

print "getting notes..."
papers = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
paper_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Paper/Metadata')
reviewer_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Reviewer/Metadata')
areachair_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Area_Chair/Metadata')

print "getting expertise..."
reviewer_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer_Expertise')
areachair_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/SPC_Expertise')

print "getting recommendations..."
recs = []
for p in papers:
    recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % p.number)

bids = client.get_tags(invitation = CONFERENCE + '/-/Add/Bid')


subject_area_overlap_data = {
    'subject_areas': reviewer_expertise_notes + areachair_expertise_notes,
    'papers': papers
}

bid_score_data = {
    'bids': bids,
    'bid_score_map': {
        "I want to review": 1.0,
        "I can review": 0.75,
        "I can probably review but am not an expert": 0.5,
        "I cannot review": 0.25,
        "No bid": 0.0
    }
}

ac_recommendation_data = {
    'recs': recs
}

# Define
paper_features = [
    uai_features.PrimarySubjectOverlap(name='primary_subject_overlap', data=subject_area_overlap_data),
    uai_features.SecondarySubjectOverlap(name='secondary_subject_overlap', data=subject_area_overlap_data),
    uai_features.BidScore(name='bid_score', data=bid_score_data),
    uai_features.ACRecommendation(name='ac_recommendation', data=ac_recommendation_data)
]

reviewer_features = [
    uai_features.PrimaryUserAffinity(name='primary_user_affinity', data=subject_area_overlap_data),
    uai_features.SecondaryUserAffinity(name='secondary_user_affinity', data=subject_area_overlap_data)
]

user_groups = {
    PC: client.get_group(PC),
    SPC: client.get_group(SPC)
}

print "generating paper metadata..."
new_paper_metadata = openreview_matcher.metadata.generate_metadata(forum_ids=[n.forum for n in papers], groups=user_groups, features=paper_features, invitation='auai.org/UAI/2017/-/Paper/Metadata', metadata=paper_metadata)
for m in new_paper_metadata:
    client.post_note(m)

print "generating reviewer metadata..."
new_reviewer_metadata = openreview_matcher.metadata.generate_metadata(forum_ids=user_groups[PC].members, groups=user_groups, features=reviewer_features, invitation='auai.org/UAI/2017/-/Reviewer/Metadata', metadata=reviewer_metadata)
for m in new_reviewer_metadata:
    client.post_note(m)

print "generating areachair metadata..."
new_areachair_metadata = openreview_matcher.metadata.generate_metadata(forum_ids=user_groups[SPC].members, groups=user_groups, features=reviewer_features, invitation='auai.org/UAI/2017/-/Area_Chair/Metadata', metadata=areachair_metadata)
for m in new_areachair_metadata:
    client.post_note(m)

print "Saving OpenReview metadata to %s.pkl" % download
match_utils.save_obj(
    {
        'user_groups': user_groups,
        'papers': papers,
        'paper_metadata': new_paper_metadata,
        'reviewer_metadata': new_reviewer_metadata,
        'areachair_metadata': new_areachair_metadata
    },
    download)
