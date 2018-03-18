#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""
from __future__ import print_function
import argparse
import openreview
import openreview_matcher

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

label = 'areachairs'

config_by_label = {n.content['label']: n.to_json() for n in client.get_notes(invitation='auai.org/UAI/2018/-/Assignment_Configuration')}

configuration_note_params = config_by_label.get(label, {})

user_constraints = configuration_note_params.get('content', {}).get('constraints', {})

# post the configuration note. in the future, this note will be posted through the UI.

configuration_note_params.update({
    'invitation': 'auai.org/UAI/2018/-/Assignment_Configuration',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs'
    ],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'content': {
        'label': label,
        'configuration': {
            'minusers': 1,
            'maxusers': 1,
            'minpapers': 1,
            'maxpapers': 10,
            'weights': {
                'tpms_score': 1,
                'conflict_score': 1,
                'bid_score': 1
            }
        },
        'constraints': {},
        'paper_invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'metadata_invitation': 'auai.org/UAI/2018/-/Paper_Metadata',
        'assignment_invitation': 'auai.org/UAI/2018/-/Paper_Assignment',
        'match_group': 'auai.org/UAI/2018/Senior_Program_Committee',
        'status': 'queued' # 'queued', 'processing', 'complete' or 'error'
    }
})

configuration_note_params['content']['constraints'] = user_constraints

# ultimately, we'll set up a process function that executes the following code
# automatically when the configuration note is posted. for now, we will do this
# manually.

# get the already-posted configuration note

papers = openreview.tools.get_all_notes(client, configuration_note_params['content']['paper_invitation'])
paper_metadata = openreview.tools.get_all_notes(client, configuration_note_params['content']['metadata_invitation'])
match_group = client.get_group(id = configuration_note_params['content']['match_group'])
reviewer_configuration = configuration_note_params['content']['configuration']

new_assignments_by_forum = openreview_matcher.match(reviewer_configuration,
    papers = papers, metadata = paper_metadata, group = match_group, constraints = user_constraints)

def create_assignment_note(forum, label):
    return openreview.Note(**{
        'forum': forum,
        'invitation': configuration_note_params['content']['assignment_invitation'],
        'readers': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Program_Committee',
            'auai.org/UAI/2018/Senior_Program_Committee'
        ],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'content': {
            'label': label
        }
    })

def get_paper_scores(forum_id):
    papers = [p for p in paper_metadata if p.forum == forum_id]

    if papers:
        return papers[0].content['groups'][configuration_note_params['content']['match_group']]
    else:
        return []

def weight_scores(group_scores, weights):
    group_weighted_scores = []

    for g in group_scores:
        weighted_scores = {}
        final_score = 0
        count = 0
        for name, value in g['scores'].iteritems():
            if value != '-inf' and value != '+inf':
                weighted_score = value * weights.get(name, 0)
                weighted_scores[name] = weighted_score

                final_score += weighted_score
                count += 1
            else:
                print(value)

        group_weighted_scores.append({
            'userId': g['userId'],
            'finalScore': final_score / count if count > 0 else 0,
            'scores': weighted_scores
        })

    return group_weighted_scores

def get_assigned_groups(scores, weights, assignment):
    group_scores = [s for s in scores if s['userId'] in assignment]
    return weight_scores(group_scores, weights)


def get_alternate_groups(scores, weights, assignment, alternate_count):

    def getKey(item):
        return item.get('finalScore', 0)

    alternates = [s for s in scores if s['userId'] not in assignment and s['scores'].get('conflict_score', 0) != '-inf']
    sorted_alternates = sorted(weight_scores(alternates, weights), key=getKey, reverse=True)
    return sorted_alternates[:alternate_count]

existing_assignments = openreview.tools.get_all_notes(client, 'auai.org/UAI/2018/-/Paper_Assignment')
existing_reviewer_assignments = {n.forum: n for n in existing_assignments if n.content['label'] == label}

for forum, assignment in new_assignments_by_forum.iteritems():
    assignment_note = existing_reviewer_assignments.get(forum, create_assignment_note(forum, label))
    new_content = {}
    new_content['label'] = label
    new_content['assignment'] = assignment

    scores = get_paper_scores(forum)
    weights = configuration_note_params['content']['configuration']['weights']
    new_content['assignedGroups'] = get_assigned_groups(scores, weights, assignment)
    new_content['alternateGroups'] = get_alternate_groups(scores, weights, assignment, 5) # 5 could be in the configuration

    assignment_note.content = new_content
    assignment_note = client.post_note(assignment_note)
    print('Paper{0: <6}'.format(assignment_note.number), ', '.join(assignment))

configuration_note_params['content']['status'] = 'complete'
config_note = client.post_note(openreview.Note(**configuration_note_params))
print('{}/reviewers?assignmentId={}'.format(client.baseurl, config_note.id))

