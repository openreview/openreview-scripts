import openreview
import random
import argparse
import requests
from collections import defaultdict

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

papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
papers_by_forum = {n.forum: n for n in papers}
groups = [client.get_group(g) for g in group_ids]
all_users = groups[0].members
profiles_by_id = {profile.id: profile for profile in client.get_profiles(all_users)}


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

tpms_scores = {}
for n in papers:
    tpms_scores[n.forum] = {}
    for user_id in all_users:
        tpms_scores[n.forum][user_id] = 1.0 #random.random()*10

# with open(<tpms file>) as f:
#   read file
#   tpms_scores = ...

def tpms(forum, user_id):
    return tpms_scores[forum][user_id]


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
