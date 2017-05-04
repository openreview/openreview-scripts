#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse

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


def subject_area_overlap(signature, forum, data):
    """
    @signature - tilde ID of user
    @forum - forum of paper
    @data - dict which has the following:
        {
            'subjectarea_by_signature': ...,
            'papers_by_forum': ...
        }

    """

    subjectareas_by_signature = data['subjectareas_by_signature']
    papers_by_forum = data['papers_by_forum']

    try:
        user_subject_list = subjectareas_by_signature[signature]
        paper_subject_list = papers_by_forum[forum].content['subject areas']

        user_subjects = set(user_subject_list)
        forum_subjects = set(paper_subject_list)
        intersection = int(len(user_subjects & forum_subjects))
        max_denominator = max([int(len(s)) for s in [user_subjects, forum_subjects]])

        if max_denominator > 0:
            return intersection / max_denominator
        else:
            return 0.0
    except:
        return 0.0

def bid_score(signature, forum, data):
    """
    @signature - tilde ID of user
    @forum - forum of paper
    @data - dict which has the following:
        {
            'bids_by_signature': ...
            'bid_score_map': ...
        }

    """
    bids_by_signature = data['bids_by_signature']
    bid_score_map = data['bid_score_map']
    try:
        bid = bids_by_signature[signature]
        score = bid_score_map[bid.tag]

        return score
    except:
        return 0.0

def recommended_by_ac(signature, forum, data):
    """
    @signature - tilde ID of user
    @forum - forum of paper
    @data - dict which has the following:
        {
            'recs_by_forum': ...
        }

    """
    recs_by_forum = data['recs_by_forum']
    recs = recs_by_forum[forum]
    recommended_users = [rec.tag for rec in recs]

    if signature in recommended_users:
        return 1.0
    else:
        return 0.0

def get_feature_vector(signature, forum, functions_by_feature, data_by_feature):
    """
    Arguments:
    @functions_by_feature: a dictionary of functions indexed by feature name
    @params_by_feature: a dictionary of data objects indexed by feature name

    Returns:
    A feature vector (list) of feature values

    """

    feature_names = data_by_feature.keys()
    feature_vector = [0]*len(data_by_feature)

    for feat_idx, feature in enumerate(feature_names):
        f = functions_by_feature[feature]

        feature_vector[feat_idx] = f(signature, forum, data_by_feature[feature])

    return feature_vector


## Main processing

papers_by_forum = data['papers_by_forum']
metadata_by_forum = data['metadata_by_forum']

user_groups = data['user_groups']

subjectareas_by_signature = data['subjectareas_by_signature']

bids_by_signature = data['bids_by_signature']
bid_score_map = data['bid_score_map']

recs_by_forum = data['recs_by_forum']


missing_reviewer_expertise = set()
missing_areachair_expertise = set()
conflicts = set()


# reset the metadata
empty_paper_note_content = {
    'groups': {group.id: {} for group in user_groups},
    'assignments': []
}

print "Resetting Paper Metadata"
for n in papers_by_forum.values():
    if n.forum not in metadata_by_forum:
        metadata_by_forum[n.forum] = openreview.Note(
          invitation = CONFERENCE + "/-/Paper/Metadata",
          readers = [CONFERENCE],
          forum = n.forum,
          writers = [CONFERENCE],
          content = empty_paper_note_content,
          signatures = [CONFERENCE]
        )
    else:
        metadata_by_forum[n.forum].content = empty_paper_note_content.copy()

functions_by_feature = {
    'subject_area_overlap': subject_area_overlap,
    'bid_score': bid_score,
    'recommended_by_ac': recommended_by_ac
}

data_by_feature = {
    'subject_area_overlap': {
        'subjectareas_by_signature': subjectareas_by_signature,
        'papers_by_forum': papers_by_forum
    },
    'bid_score': {
        'bids_by_signature': bids_by_signature,
        'bid_score_map': bid_score_map
    },
    'recommended_by_ac': {
        'recs_by_forum': recs_by_forum
    }
}

for forum in papers_by_forum:
    metadata = metadata_by_forum[forum]
    for group in user_groups:
        for signature in group.members:
            metadata.content['groups'][group.id][signature] = get_feature_vector(signature, forum, functions_by_feature, data_by_feature)

filtered_paper_metadata_notes = [n for n in metadata_by_forum.values() if n.forum in papers_by_forum]


usergroup_to_match = user_groups[0] # Program Committee
papers_to_match = papers_by_forum.values()
matching_configuration = {
    "minusers": 0,
    "maxusers": 100,
    "minpapers": 0,
    "maxpapers": 100,
    "weights": [.1, .1, .1]
}
paper_metadata = filtered_paper_metadata_notes

matcher = openreview_matcher.Matcher(usergroup_to_match, papers_to_match, matching_configuration, paper_metadata)
assignments = matcher.solve()
print assignments

print "Saving local metadata to metadata.pkl"
match_utils.save_obj(data, './metadata')


