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
    'auai.org/UAI/2018/Program_Committee',
    'auai.org/UAI/2018/Senior_Program_Committee'
]

papers = openreview.tools.get_all_notes(client, 'auai.org/UAI/2018/-/Blind_Submission')
papers_by_forum = {n.forum: n for n in papers}
originals_by_forum = {n.forum: n for n in openreview.tools.get_all_notes(client, 'auai.org/UAI/2018/-/Submission')}
groups = [client.get_group(g) for g in group_ids]
all_users = [u for u in reduce(lambda acc, g: acc.members + g.members, groups) if '~' in u]
profiles_by_id = {uid: client.get_note(uid) for uid in all_users}

'''
The functions below are "dummy" feature functions for building up a test dataset.
'''

def affinity(forum, user_id):
    return 1.0

def conflict(forum, user_id):
    try:
        paper = papers_by_forum[forum]
        original = originals_by_forum[paper.original]
        profile = profiles_by_id[user_id]
        paper_domain_conflicts, paper_relation_conflicts = openreview.tools.get_paper_conflicts(client, original)
        profile_domain_conflicts, profile_relation_conflicts = openreview.tools.profile_conflicts(profile)
        if paper_domain_conflicts.intersection(profile_domain_conflicts):
            return '-inf'
        if paper_relation_conflicts.intersection(profile_relation_conflicts):
            return '-inf'
        else:
            return 0.0
    except KeyError as e:
        print "conflict error!"
        print 'original: ', paper.original
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

'''
The functions below are the "real" versions.

'''

# scores_by_user_by_forum = {n.forum: defaultdict(lambda:0) for n in papers}

# for g in groups:
#     for n in papers:
#         print 'processing ', n.id
#         response = requests.get(
#             client.baseurl+'/reviewers/scores?group={0}&forum={1}'.format(g.id, n.forum),
#             headers=client.headers)
#         scores_by_user_by_forum[n.forum].update({r['user']: r['score'] for r in response.json()['scores']})


# def affinity(forum, user_id):
#     return scores_by_user_by_forum[forum][user_id]

# def conflict(forum, user_id):
#     pass

def metadata(forum, groups):
    metadata_params = {
        'forum': forum,
        'invitation': 'auai.org/UAI/2018/-/Paper_Metadata',
        'readers': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Program_Committee',
            'auai.org/UAI/2018/Senior_Program_Committee'
        ],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'content': {
                'groups': {}
            }
    }
    for g in groups:

        group_entry = []
        for user_id in g.members:
            if '~' in user_id:
                user_entry = {'userId': user_id, 'scores': {}}
                affinity_score = affinity(forum, user_id)
                tpms_score = tpms(forum, user_id)
                conflict_score = conflict(forum, user_id)

                if affinity_score > 0:
                    user_entry['scores']['affinity_score'] = affinity_score
                if conflict_score == '-inf':
                    user_entry['scores']['conflict_score'] = conflict_score
                if tpms_score > 0:
                    user_entry['scores']['tpms_score'] = tpms_score

                group_entry.append(user_entry)

        metadata_params['content']['groups'][g.id] = group_entry

    return metadata_params

existing_notes_by_forum = {n.forum: n for n in openreview.tools.get_all_notes(client, 'auai.org/UAI/2018/-/Paper_Metadata')}

print "posting paper metadata..."

for p in papers:
    if p.forum in existing_notes_by_forum:
        metadata_params = existing_notes_by_forum[p.forum].to_json()
    else:
        metadata_params = {}

    metadata_params.update(metadata(p.forum, groups))
    metadata_note = client.post_note(openreview.Note(**metadata_params))
    print metadata_note.id
