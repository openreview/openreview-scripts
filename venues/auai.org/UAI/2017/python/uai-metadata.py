import argparse
from collections import defaultdict
import imp

import openreview

from uaidata import *
import uai_features

from openreview_matcher.metadata import generate_metadata
from openreview_matcher.models import tfidf
from openreview_matcher import utils

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--download', help = "the filename (without extension) of the .pkl file to save the downloaded data. Defaults to ./metadata")
parser.add_argument('--overwrite', action='store_true', help = "if present erases the old metadata")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

download = './metadata' if args.download == None else args.download

print "getting notes..."
papers = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
program_committee = client.get_group('auai.org/UAI/2017/Program_Committee')

if args.overwrite:
    print "erasing old metadata..."
    paper_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Paper/Metadata')
    reviewer_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Reviewer/Metadata')
    areachair_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Area_Chair/Metadata')

    for p in paper_metadata: client.delete_note(p)
    for r in reviewer_metadata: client.delete_note(r)
    for a in areachair_metadata: client.delete_note(a)

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

print "loading TFIDF model..."
tfidf_model = utils.load_obj('../data/tfidf.pkl')

tfidf_data = {'model': tfidf_model, 'papers': papers}

# Define features
paper_features = [
    uai_features.PrimarySubjectOverlap(name='primary_subject_overlap', data=subject_area_overlap_data),
    uai_features.SecondarySubjectOverlap(name='secondary_subject_overlap', data=subject_area_overlap_data),
    uai_features.BidScore(name='bid_score', data=bids),
    uai_features.ACRecommendation(name='ac_recommendation', data=recs),
    uai_features.TFIDF(name='tfidf', data=tfidf_data)
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
paper_metadata_contents = generate_metadata(forum_ids=[n.forum for n in papers], groups=user_groups.values(), features=paper_features)

print "generating reviewer metadata..."
reviewer_metadata_contents = generate_metadata(forum_ids=user_groups[PC].members, groups=user_groups.values(), features=reviewer_features)

print "generating areachair metadata..."
areachair_metadata_contents = generate_metadata(forum_ids=user_groups[SPC].members, groups=user_groups.values(), features=reviewer_features)

new_paper_metadata = []
for forum in paper_metadata_contents:
    new_paper_metadata.append(openreview.Note(
        forum = forum,
        content = paper_metadata_contents[forum],
        invitation = 'auai.org/UAI/2017/-/Paper/Metadata',
        readers = ['auai.org/UAI/2017'],
        writers = ['auai.org/UAI/2017'],
        signatures = ['auai.org/UAI/2017']
    ))

new_reviewer_metadata = []
for forum in reviewer_metadata_contents:
    new_reviewer_metadata.append(openreview.Note(
        forum = forum,
        content = reviewer_metadata_contents[forum],
        invitation = 'auai.org/UAI/2017/-/Reviewer/Metadata',
        readers = ['auai.org/UAI/2017'],
        writers = ['auai.org/UAI/2017'],
        signatures = ['auai.org/UAI/2017']
    ))

new_areachair_metadata = []
for forum in areachair_metadata_contents:
    new_areachair_metadata.append(openreview.Note(
        forum = forum,
        content = areachair_metadata_contents[forum],
        invitation = 'auai.org/UAI/2017/-/Area_Chair/Metadata',
        readers = ['auai.org/UAI/2017'],
        writers = ['auai.org/UAI/2017'],
        signatures = ['auai.org/UAI/2017']
    ))

print "Saving OpenReview metadata to %s.pkl" % download
utils.save_obj(
    {
        'user_groups': user_groups,
        'papers': papers,
        'paper_metadata': new_paper_metadata,
        'reviewer_metadata': new_reviewer_metadata,
        'areachair_metadata': new_areachair_metadata
    },
    download)

post_notes = raw_input("Would you like to post the metadata notes? (y/[n]): ")

if post_notes.lower()=='y':
    print "posting paper metadata..."
    for p in new_paper_metadata: client.post_note(p)
    print "posting reviewer metadata..."
    for r in new_reviewer_metadata: client.post_note(r)
    print "posting area chair metadata..."
    for a in new_areachair_metadata: client.post_note(a)
