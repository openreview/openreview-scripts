
import argparse
from collections import defaultdict

import openreview
import match_utils

from uaidata import *
import feature_functions

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--download', help = "the filename (without extension) of the .pkl file to save the downloaded data. Defaults to ./metadata")
parser.add_argument('--upload', help = "the .pkl file (with extension) to upload to OpenReview. If \"true\", defaults to ./metadata.pkl")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

download = './metadata' if args.download == None else args.download

data = {}

papers_by_forum = { n.forum: n for n in client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission') }
metadata_by_forum = { n.forum: n for n in client.get_notes(invitation='auai.org/UAI/2017/-/Paper/Metadata') }

data['user_groups'] = {id: client.get_group(id) for id in ['auai.org/UAI/2017/Program_Committee', 'auai.org/UAI/2017/Senior_Program_Committee'] }

reviewer_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer_Expertise')
areachair_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/SPC_Expertise')
subjectareas_by_signature = {n.signatures[0]: n.content for n in areachair_expertise_notes+reviewer_expertise_notes}

bids_by_signature = {bid.signatures[0]: bid for bid in client.get_tags(invitation = CONFERENCE + '/-/Add/Bid') if bid.forum in papers_by_forum}

bid_score_map = {
    "I want to review": 1.0,
    "I can review": 0.75,
    "I can probably review but am not an expert": 0.5,
    "I cannot review": 0.25,
    "No bid": 0.0
}

print "Getting areachair recommendations..."

recs_by_forum = defaultdict(list)
for forum in papers_by_forum:
    tags = client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % papers_by_forum[forum].number)
    recs_by_forum[forum] = tags

# reset the metadata
empty_paper_note_content = {
    'groups': {group.id: {} for group in data['user_groups'].values()},
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

features_by_name = {
    'subject_area_overlap': feature_functions.SubjectAreaOverlap(data_by_feature['subject_area_overlap']),
    'bid_score': feature_functions.BidScore(data_by_feature['bid_score']),
    'recommended_by_ac': feature_functions.ACRecommendation(data_by_feature['recommended_by_ac'])
}


for forum in papers_by_forum:
    metadata = metadata_by_forum[forum]
    for group in data['user_groups'].values():
        for signature in group.members:
            feature_vector = [features_by_name[name].score(signature, forum) for name in features_by_name]
            metadata.content['groups'][group.id][signature] = feature_vector


data['papers_to_match'] = [ client.post_note(papers_by_forum[forum]) for forum in papers_by_forum ]
data['paper_metadata'] = [ client.post_note(metadata_by_forum[forum]) for forum in papers_by_forum ]

###
print "Saving OpenReview metadata to %s.pkl" % download
match_utils.save_obj(data, download)
