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

constraint_maps = {}
score_maps = {}

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

#Network calls
print "getting all submissions..."
metadata_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Conference/Area_Chairs/-/Paper_Metadata')
areachairs = client.get_group('cv-foundation.org/ECCV/2018/Conference/Area_Chairs')
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
papers_by_forum = {}
forum_by_paperid = {}
for p in papers:
    papers_by_forum[p.forum] = p
    forum_by_paperid[int(p.content['paperId'])] = p.forum



#Load saved profiles:
print "loading author profiles from file..."
author_profiles_by_email = {}
with open('../data/author-profiles.pkl', 'rb') as f:
    author_profiles_by_email = pickle.load(f)

print "loading areachair profiles from file..."
areachair_profiles_by_email = {}
with open('../data/areachair-profiles.pkl', 'rb') as f:
    areachair_profiles_by_email = pickle.load(f)

areachair_profiles_by_id = {profile.id: profile for profile in areachair_profiles_by_email.values()}

'''
# get existing assignments
'''
print "getting existing assignments..."
assigned_papers_by_ac = defaultdict(list)

with open('../data/ac1-assignments-from-cmt-2018-04-25.pkl') as f:
    assigned_paperids_by_ac = pickle.load(f)
    for ac_id, assigned_paperids in assigned_paperids_by_ac.iteritems():
        for paperid in assigned_paperids:
            forum = forum_by_paperid.get(paperid)
            if forum in papers_by_forum:
                assigned_papers_by_ac[ac_id].append(forum)

#Load TPMS scores
print "loading tpms scores from file..."
scores_by_forum = {}
with open('../data/areachairs_scores.csv') as f:
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

            profile = areachair_profiles_by_email.get(email)

            if profile:
                scores_by_forum[forum][profile.id] = float(score)
            else:
                print "profile not found: ", email

'''
flatten TPMS scores for 2nd round AC match.

Explanation: the PCs want to assign a second set of ACs to existing AC assignments,
resulting in two ACs per paper. But they also want to minimize the number of unique
AC-AC pairs (e.g. ideally, every AC would get exactly one "buddy" AC).

The solution implemented here is to group the papers by assigned AC, and among these
groups, average the TPMS scores of all other ACs. This should have the desired effect.

'''
flattened_tpms_score_map = {}
for ac, forum_list in assigned_papers_by_ac.iteritems():

    summed_scores = reduce(
        lambda x, y: {userid: x.get(userid, 0.0) + y.get(userid, 0.0) for userid in x},
        [scores_by_forum.get(forum, {}) for forum in forum_list]
    )

    average_scores = {userid: val/float(len(forum_list)) for userid, val in summed_scores.iteritems()}

    for forum in forum_list:
        flattened_tpms_score_map[forum] = average_scores

score_maps['tpmsScore'] = flattened_tpms_score_map

# compute existing AC constraint map
ac_constraint_map = {}
for ac, forum_list in assigned_papers_by_ac.iteritems():
    for forum in forum_list:
        if forum not in ac_constraint_map:
            ac_constraint_map[forum] = {}
        ac_constraint_map[forum][ac] = '-inf'

constraint_maps['acConstraint'] = ac_constraint_map


#Load CMT conflicts
print "loading CMT conflicts...",
cmt_conflicts = {}
with open('../data/areachair-conflicts.csv') as f:
    reader = csv.reader(f)
    for line in reader:
        email = line[2].strip().lower()
        paperid = line[3].strip().lower()

        if paperid in forum_by_paperid:
            conflicted_forum = forum_by_paperid[paperid]

            areachair_profile = areachair_profiles_by_email.get(email)

            if areachair_profile:
                cmt_conflicts[conflicted_forum] = cmt_conflicts.get(conflicted_forum, {})
                cmt_conflicts[conflicted_forum][areachair_profile.id] = '-inf'
            else:
                print "profile not found: ", email

constraint_maps['cmtConflict'] = cmt_conflicts


# load openreview conflicts
print "loading openreview conflicts...",
openreview_conflicts = {}
for forum, paper in papers_by_forum.iteritems():
    forum_conflicts = {}
    for user_id in areachairs.members:
        areachair_profile = areachair_profiles_by_id[user_id]
        author_profiles = {}
        for authorid in paper.content['authorids']:
            author_profiles[authorid] = author_profiles_by_email.get(authorid, None)

        conflicts = openreview.matching.get_conflicts(author_profiles, areachair_profile)
        if conflicts:
            forum_conflicts[areachair_profile.id] = '-inf'

    openreview_conflicts[forum] = forum_conflicts

constraint_maps['openreviewConflict'] = openreview_conflicts

print "dumping...",
with open('../data/score-maps-ac2.pkl', 'wb') as f:
    pickle.dump({
        'score_maps': score_maps,
        'constraint_maps': constraint_maps
    }, f)

print "done"
