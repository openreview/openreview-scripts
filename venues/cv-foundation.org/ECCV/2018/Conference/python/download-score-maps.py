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

#Network calls
print "getting all submissions...",
metadata_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Conference/Reviewers/-/Paper_Metadata')
reviewers = client.get_group('cv-foundation.org/ECCV/2018/Conference/Reviewers')
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
papers_by_forum = {}
forum_by_paperid = {}
for p in papers:
    papers_by_forum[p.forum] = p
    forum_by_paperid[p.content['paperId']] = p.forum

#Load saved profiles:
print "loading author profiles from file..."
author_profiles_by_email = {}
with open('../data/author-profiles.pkl', 'rb') as f:
    author_profiles_by_email = pickle.load(f)

print "loading reviewer profiles from file..."
reviewer_profiles_by_email = {}
with open('../data/reviewer-profiles.pkl', 'rb') as f:
    reviewer_profiles_by_email = pickle.load(f)

reviewer_profiles_by_id = {profile.id: profile for profile in reviewer_profiles_by_email.values()}

#Load TPMS scores
print "loading tpms scores from file..."
scores_by_forum = {}
with open('../data/reviewers_scores.csv') as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        paperId = line[0].strip()
        email = line[1].strip().lower()
        score = line[2].strip()

        forum = forum_by_paperid.get(paperId)

        if forum:
            if forum not in scores_by_forum:
                scores_by_forum[forum] = {}

            profile = reviewer_profiles_by_email.get(email)

            if profile:
                scores_by_forum[forum][profile.id] = float(score)
            else:
                print "profile not found: ", email

#Load AC ranks
print "loading ac ranks from file..."
ac_rank_by_forum = {}
max_rank = 0
with open('../data/ac-recommendations-2018-04-10.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        ac_email = row[0].lower().strip()
        paper_id = row[1]
        ac_rank = int(row[2])
        reviewer_email = row[3].lower().strip()

        reviewer_profile = reviewer_profiles_by_email.get(reviewer_email)
        paper_forum = forum_by_paperid.get(paper_id)

        if paper_forum not in ac_rank_by_forum:
            ac_rank_by_forum[paper_forum] = {}

        if reviewer_profile:
            ac_rank_by_forum[paper_forum][reviewer_profile.id] = ac_rank
        else:
            print "no reviewer found for email ", reviewer_email

        if ac_rank > max_rank:
            max_rank = ac_rank

print "converting to score...",
#rank_to_score converts the rank given by the AC for a reviewer into a score in the range (0.0, 1.0]
rank_to_score = [float(max_rank-i)/float(max_rank) for i in range(max_rank)]
ac_score_by_forum = {}
for forum, reviewer_ranks in ac_rank_by_forum.iteritems():
    if forum not in ac_score_by_forum:
        ac_score_by_forum[forum] = {}
    for reviewer, rank in ac_rank_by_forum[forum].iteritems():
        # rank-1 because AC ranks starts at index 1, and rank_to_score starts at index 0
        ac_score_by_forum[forum][reviewer] = rank_to_score[rank-1]

#Load CMT conflicts
print "loading CMT conflicts...",
cmt_conflicts = {}
with open('../data/reviewer-conflicts.csv') as f:
    reader = csv.reader(f)
    for line in reader:
        email = line[2].strip().lower()
        paperid = line[3].strip().lower()

        if paperid in forum_by_paperid:
            conflicted_forum = forum_by_paperid[paperid]

            reviewer_profile = reviewer_profiles_by_email.get(email)

            if reviewer_profile:
                cmt_conflicts[conflicted_forum] = cmt_conflicts.get(conflicted_forum, {})
                cmt_conflicts[conflicted_forum][reviewer_profile.id] = '-inf'
            else:
                print "profile not found: ", email

# load openreview conflicts
print "loading openreview conflicts...",
openreview_conflicts = {}
for forum, paper in papers_by_forum.iteritems():
    forum_conflicts = {}
    for user_id in reviewers.members:
        reviewer_profile = reviewer_profiles_by_id[user_id]
        author_profiles = {}
        for authorid in paper.content['authorids']:
            author_profiles[authorid] = author_profiles_by_email.get(authorid, None)

        conflicts = openreview.matching.get_conflicts(author_profiles, reviewer_profile)
        if conflicts:
            forum_conflicts[reviewer_profile.id] = '-inf'

    openreview_conflicts[forum] = forum_conflicts

print "dumping...",
with open('../data/score-maps.pkl', 'wb') as f:
    pickle.dump({
        'score_maps': {
            'tpmsScore': scores_by_forum,
            'acRecommendation': ac_score_by_forum
        },
        'constraint_maps': {
            'cmtConflict': cmt_conflicts,
            'openreviewConflict': openreview_conflicts
        }
    }, f)

print "done"
