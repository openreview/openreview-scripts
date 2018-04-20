import openreview
import random
import argparse
import requests
from collections import defaultdict
import csv
import os
import json
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

group_ids = [
    'cv-foundation.org/ECCV/2018/Conference/Area_Chairs'
]

#Load Papers
print "getting all submissions..."
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
papers_by_forum = {}
forum_by_paperId = {}
for p in papers:
    papers_by_forum[p.forum] = p
    forum_by_paperId[p.content['paperId']] = p.forum

#Load group profiles
print "getting groups..."
groups = [client.get_group(g) for g in group_ids]
all_users = groups[0].members
profiles_by_id = {profile.id: profile for profile in client.get_profiles(all_users)}

#Load TPMS scores
print "loading tpms scores from file..."
tpms_scores = {}
with open(os.path.join(os.path.dirname(__file__),'../data/areachairs_scores.csv')) as f:
    reader = csv.reader(f)
    reader.next()
    scores_by_email = {}
    for line in reader:
        paperId = line[0].strip()
        email = line[1].strip().lower()
        score = line[2].strip()

        if email not in scores_by_email:
            scores_by_email[email] = {}

        forum = forum_by_paperId.get(paperId, 0)

        scores_by_email[email][forum] = float(score)

    #translate emails to ids
    for k,v in scores_by_email.iteritems():
        profiles = client.get_profiles([k])
        if profiles:
            tpms_scores[profiles[k].id] = v
        else:
            'Profile not found', k

#Load author profiles
print "loading author profiles from file..."
author_profiles_by_email = {}
with open('../data/profiles.pkl', 'rb') as f:
    author_profiles_by_email = pickle.load(f)

print "getting conference objects...",
metadata_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Conference/Reviewers/-/Paper_Metadata')
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
reviewers = client.get_group('cv-foundation.org/ECCV/2018/Conference/Reviewers')

print "loading score maps..."
with open('../data/score-maps.pkl', 'rb') as f:
    maps = pickle.load(f)
score_maps = maps['score_maps']
constraint_maps = maps['constraint_maps']

new_metadata_notes = openreview_matcher.metadata.generate_metadata_notes(client,
    papers = papers,
    metadata_invitation = metadata_invitation,
    match_group = reviewers,
    score_maps = score_maps,
    constraint_maps = constraint_maps
)

for m in new_metadata_notes:
    new_m = client.post_note(m)
    print new_m.id
