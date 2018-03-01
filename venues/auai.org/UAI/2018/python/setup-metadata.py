import openreview
import openreview_matcher
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

submissions = client.get_notes(invitation='auai.org/UAI/2018/-/Submission')

group_ids = [
    'auai.org/UAI/2018/Program_Committee',
    'auai.org/UAI/2018/Senior_Program_Committee'
]

papers = client.get_notes(invitation = 'auai.org/UAI/2018/-/Blind_Submission')
groups = [client.get_group(g) for g in group_ids]
all_users = reduce(lambda acc, g: acc.members + g.members, groups)

'''
The functions below are "dummy" feature functions for building up a test dataset.
'''

def affinity(forum, user_id):
    return random.random()*10

def conflict(forum, user_id):
    if random.random() > 0.9:
        return '-inf'
    else:
        return None



tpms_scores = {}
for n in papers:
    tpms_scores[n.forum] = {}
    for user_id in all_users:
        tpms_scores[n.forum][user_id] = random.random()*10

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

        group_entry = {}
        for user_id in g.members:
            user_entry = {}
            affinity_score = affinity(forum, user_id)
            tpms_score = tpms(forum, user_id)
            conflict_score = conflict(forum, user_id)

            if affinity_score > 0:
                user_entry['affinity_score'] = affinity_score
            if conflict_score == '-inf':
                user_entry['conflict_score'] = conflict_score
            if tpms_score > 0:
                user_entry['tpms_score'] = tpms_score
            group_entry[user_id] = user_entry

        metadata_params['content']['groups'][g.id] = group_entry

    return metadata_params

existing_notes_by_forum = {n.forum: n for n in client.get_notes(invitation = 'auai.org/UAI/2018/-/Paper_Metadata')}

print "posting paper metadata..."
for p in papers:
    if p.forum in existing_notes_by_forum:
        metadata_params = existing_notes_by_forum[p.forum].to_json()
    else:
        metadata_params = {}

    metadata_params.update(metadata(p.forum, groups))
    metadata_note = client.post_note(openreview.Note(**metadata_params))
    print metadata_note.id
