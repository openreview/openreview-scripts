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

label = 'reviewers'

config_by_label = {n.content['label']: n.to_json() for n in client.get_notes(invitation='auai.org/UAI/2018/-/Assignment_Configuration')}

configuration_note_params = config_by_label.get(label, {})

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
            'minusers': 3,
            'maxusers': 3,
            'minpapers': 0,
            'maxpapers': 5,
            'weights': {
                'bid_score': 1,
                'affinity_score': 1,
                'conflict_score': 1,
                'recommendation_score': 1
            }
        },
        'paper_invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'metadata_invitation': 'auai.org/UAI/2018/-/Paper_Metadata',
        'assignment_invitation': 'auai.org/UAI/2018/-/Paper_Assignment',
        'constraints_invitation': 'auai.org/UAI/2018/-/Paper_Constraints',
        'match_group': 'auai.org/UAI/2018/Program_Committee',
        'status': 'queued' # 'queued', 'processing', 'complete' or 'error'
    }
})

# add some user constraints. in the future, this will be added by the user through the GUI.
configuration_note_params['content']['constraints'] = {
    '~Benjamin_Guedj1': {
        'SkWNNgtvUz': '-inf'
    },
    '~David_Jensen1': {
        'Bkv4lKPLf': '+inf'
    }
}


# ultimately, we'll set up a process function that executes the following code
# automatically when the configuration note is posted. for now, we will do this
# manually.

# get the already-posted configuration note

papers = client.get_notes(invitation = configuration_note_params['content']['paper_invitation'])
paper_metadata = client.get_notes(invitation = configuration_note_params['content']['metadata_invitation'])
match_group = client.get_group(id = configuration_note_params['content']['match_group'])
reviewer_configuration = configuration_note_params['content']['configuration']
user_constraints = configuration_note_params['content']['constraints']

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

existing_assignments = client.get_notes(invitation='auai.org/UAI/2018/-/Paper_Assignment')
existing_reviewer_assignments = {n.forum: n for n in existing_assignments if n.content['label'] == label}

for forum, assignment in new_assignments_by_forum.iteritems():
    assignment_note = existing_reviewer_assignments.get(forum, create_assignment_note(forum, label))
    assignment_note.content['assignment'] = assignment
    assignment_note = client.post_note(assignment_note)
    print('Paper{0: <6}'.format(assignment_note.number), ', '.join(assignment))

configuration_note_params['content']['status'] = 'complete'
client.post_note(openreview.Note(**configuration_note_params))

