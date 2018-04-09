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

metadata_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Conference/Reviewers/-/Paper_Metadata')

#Load Papers
print "getting all submissions...",
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
papers_by_forum = {}
forum_by_paperId = {}
for p in papers:
    papers_by_forum[p.forum] = p
    forum_by_paperId[p.content['paperId']] = p.forum
print "done."

#Load group profiles
print "getting groups...",
reviewers = client.get_group('cv-foundation.org/ECCV/2018/Conference/Reviewers')
profiles_by_id = {profile.id: profile for profile in client.get_profiles(reviewers.members)}
print "done."

#Load TPMS scores
print "loading tpms scores from file...",
scores_by_forum = {}
ids_by_email = {}
with open('../data/reviewers_scores.csv') as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        paperId = line[0].strip()
        email = line[1].strip().lower()
        score = line[2].strip()

        forum = forum_by_paperId.get(paperId, '')

        if forum not in scores_by_forum:
            scores_by_forum[forum] = {}

        if email not in ids_by_email:
            profiles = client.get_profiles([email])
            if profiles:
                userid = profiles[email].id
            else:
                userid = None
            ids_by_email[email] = userid
        else:
            userid = ids_by_email[email]

        if userid:
            scores_by_forum[forum][userid] = float(score)
print "done."

#Load author profiles
print "loading author profiles from file...",
author_profiles_by_email = {}
with open('../data/profiles.pkl', 'rb') as f:
    author_profiles_by_email = pickle.load(f)
print "done."

#Load CMT conflicts
print "loading CMT conflicts..."
cmt_conflicts = {}
profiles_by_email = {}
with open('../data/reviewer-conflicts.csv') as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        email = line[2].strip().lower()
        print email
        paperid = line[3].strip().lower()
        if paperid in forum_by_paperId:
            conflicted_forum = forum_by_paperId[paperid]
            if not email in profiles_by_email:
                new_profiles = client.get_profiles([email])
                if not new_profiles:
                    profiles_by_email.update({email: None})
                else:
                    profiles_by_email.update(new_profiles)

            userid = None
            if email in profiles_by_email and profiles_by_email[email]:
                userid = profiles_by_email[email].id

            if userid:
                cmt_conflicts[conflicted_forum] = cmt_conflicts.get(conflicted_forum, {})
                cmt_conflicts[conflicted_forum][userid] = '-inf'
print "done."

# load openreview conflicts
print "loading openreview conflicts..."
openreview_conflicts = {}
for forum, paper in papers_by_forum.iteritems():
    print forum
    forum_conflicts = {}
    for user_id in reviewers.members:
        profile = profiles_by_id[user_id]
        author_profiles = {}
        for authorid in paper.content['authorids']:
            author_profiles[authorid] = author_profiles_by_email.get(authorid, None)
        conflicts = openreview.matching.get_conflicts(author_profiles, profile)
        if conflicts:
            forum_conflicts[user_id] = '-inf'

    openreview_conflicts[forum] = forum_conflicts
print "done."

new_metadata_notes = openreview_matcher.metadata.generate_metadata_notes(client,
    papers = papers,
    metadata_invitation = metadata_invitation,
    match_group = reviewers,
    score_maps = {
        'tpmsScore': scores_by_forum,
    },
    constraint_maps = {
        'cmtConflict': cmt_conflicts,
        'openreviewConflict': openreview_conflicts
    }
)

for m in new_metadata_notes:
    new_m = client.post_note(m)
    print new_m.id




