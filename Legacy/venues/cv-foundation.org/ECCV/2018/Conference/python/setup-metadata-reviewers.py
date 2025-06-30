import openreview
import openreview_matcher
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
