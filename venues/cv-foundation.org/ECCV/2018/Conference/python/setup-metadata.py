import openreview
import random
import argparse
import requests
from collections import defaultdict
import csv
import os

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
papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
papers_by_forum = {}
forum_by_paperId = {}
for p in papers:
    papers_by_forum[p.forum] = p
    forum_by_paperId[p.content['paperId']] = p.forum

#Load users
groups = [client.get_group(g) for g in group_ids]
all_users = groups[0].members
profiles_by_id = {profile.id: profile for profile in client.get_profiles(all_users)}

#Load scores
tpms_scores = {}
all_emails = set()
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
        all_emails.add(email)

    #translate emails to ids
    profiles_by_email = client.get_profiles(list(all_emails))

    for k,v in scores_by_email.iteritems():

        if k in profiles_by_email:
            tpms_scores[profiles_by_email[k].id] = v

def conflict(forum, user_id):
    try:
        paper = papers_by_forum[forum]
        profile = profiles_by_id[user_id]
        paper_domain_conflicts, paper_relation_conflicts = openreview.tools.get_paper_conflicts(client, paper)
        profile_domain_conflicts, profile_relation_conflicts = openreview.tools.profile_conflicts(profile)
        if paper_domain_conflicts.intersection(profile_domain_conflicts):
            return '-inf'
        if paper_relation_conflicts.intersection(profile_relation_conflicts):
            return '-inf'
        else:
            return 0.0
    except KeyError as e:
        print "conflict error!"
        print 'forum: ', forum
        return 0.0

def tpms(forum, user_id):
    return tpms_scores.get(user_id, {}).get(forum, 0)


def metadata(forum, groups):
    metadata_params = {
        'forum': forum,
        'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Metadata',
        'readers': [
            'cv-foundation.org/ECCV/2018/Conference',
            'cv-foundation.org/ECCV/2018/Conference/Program_Chairs'
        ],
        'writers': ['cv-foundation.org/ECCV/2018/Conference'],
        'signatures': ['cv-foundation.org/ECCV/2018/Conference'],
        'content': {
                'groups': {}
            }
    }
    for g in groups:

        group_entry = []
        for user_id in g.members:
            if '~' in user_id:
                user_entry = {'userId': user_id, 'scores': {}}
                tpms_score = tpms(forum, user_id)
                conflict_score = conflict(forum, user_id)

                if conflict_score == '-inf':
                    user_entry['scores']['conflict_score'] = conflict_score
                if tpms_score > 0:
                    user_entry['scores']['tpms_score'] = tpms_score

                group_entry.append(user_entry)

        metadata_params['content']['groups'][g.id] = group_entry

    return metadata_params

existing_notes_by_forum = {n.forum: n for n in openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Paper_Metadata')}

print "posting paper metadata..."

for p in papers:
    if p.forum in existing_notes_by_forum:
        metadata_params = existing_notes_by_forum[p.forum].to_json()
    else:
        metadata_params = {}

    metadata_params.update(metadata(p.forum, groups))
    metadata_note = client.post_note(openreview.Note(**metadata_params))
    print metadata_note.id
