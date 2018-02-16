#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

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
    'label': 'reviewers',
    'group': 'auai.org/UAI/2018/Program_Committee',
    'submission': 'auai.org/UAI/2018/-/Blind_Submission',
    'exclude': [],
    'metadata': 'auai.org/UAI/2018/-/Paper_Metadata',
    'assignment': 'auai.org/UAI/2018/-/Paper_Assignment',
    'minusers': 3,
    'maxusers': 3,
    'minpapers': 0,
    'maxpapers': 5,
    'weights': {
        'bid_score': 1
    }
}

matcher = openreview_matcher.Matcher(client=client)

# solving the matcher returns a configuration note object with the content.assignments field filled in.
assignment_notes = matcher.solve(reviewer_configuration)


existing_assignment_notes_by_forum = {n.forum: n for n in client.get_notes(invitation='auai.org/UAI/2018/-/Paper_Assignment')}
# Post a note with the configuration and assignments for later use
for assignment in assignment_notes:
	if assignment.forum in existing_assignment_notes_by_forum:
		assignment.content = existing_assignment_notes_by_forum[assignment.forum].content
	client.post_note(assignment)
	print "posted assignment note {0}".format(assignment.forum)

