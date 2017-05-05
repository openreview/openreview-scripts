
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
metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Paper/Metadata')

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


features = [
    uai_features.SubjectAreaOverlap(name='subject_area_overlap', data=subject_area_overlap_data),
    uai_features.BidScore(name='bid_score', data=bid_score_data),
    uai_features.ACRecommendation(name='ac_recommendation', data=ac_recommendation_data)
]

user_groups = {
    PC: client.get_group(PC),
    SPC: client.get_group(SPC)
}

print "building metadata..."
metadata = openreview_matcher.metadata.get_metadata(papers=papers, groups=user_groups, features=features)

posted_metadata = []
for m in metadata:
    print "posting ", m.forum
    posted_metadata.append(client.post_note(m))

print "Saving OpenReview metadata to %s.pkl" % download
match_utils.save_obj(
    {
        'user_groups': user_groups,
        'papers': papers,
        'metadata': posted_metadata
    },
    download)
