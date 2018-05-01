import openreview
import random
import argparse
import requests
from collections import defaultdict
import csv
import os
import json
import pickle
import openreview_matcher

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

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
group = client.get_group('cv-foundation.org/ECCV/2018/Conference/Area_Chairs')
all_users = group.members
profiles_by_id = {profile.id: profile for profile in client.get_profiles(all_users)}

#Load author profiles
print "loading author profiles from file..."
author_profiles_by_email = {}
with open('../data/author-profiles.pkl', 'rb') as f:
    author_profiles_by_email = pickle.load(f)

print "getting conference objects...",
metadata_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Conference/Area_Chairs/-/Paper_Metadata')
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
reviewers = client.get_group('cv-foundation.org/ECCV/2018/Conference/Area_Chairs')

print "loading score maps..."
with open('../data/score-maps-ac2.pkl', 'rb') as f:
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
