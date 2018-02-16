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

# get the already-posted configuration note

reviewer_configuration = {
    'minusers': 3,
    'maxusers': 3,
    'minpapers': 0,
    'maxpapers': 5,
    'weights': {
        'bid_score': 1
    }
}

papers = client.get_notes(invitation = 'auai.org/UAI/2018/-/Blind_Submission')
paper_metadata = client.get_notes(invitation = 'auai.org/UAI/2018/-/Paper_Metadata')
match_group = client.get_group('auai.org/UAI/2018/Program_Committee')

new_assignments_by_forum = openreview_matcher.match(reviewer_configuration,
    papers = papers, metadata = paper_metadata, group = match_group)

def create_assignment_note(forum, label):
    return openreview.Note(**{
        'forum': forum,
        'invitation': 'auai.org/UAI/2018/-/Paper_Assignment',
        'readers': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Senior_Program_Committee'
        ],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'content': {
            'label': label
        }
    })

existing_assignments = client.get_notes(invitation='auai.org/UAI/2018/-/Paper_Assignment')
existing_reviewer_assignments = {n.forum: n for n in existing_assignments if n.content['label'] == 'reviewers'}

for forum, assignment in new_assignments_by_forum.iteritems():
    assignment_note = existing_reviewer_assignments.get(forum, create_assignment_note(forum, 'reviewers'))
    assignment_note.content['assignment'] = assignment
    assignment_note = client.post_note(assignment_note)
    print('Paper{0: <6}'.format(assignment_note.number), ', '.join(assignment))


