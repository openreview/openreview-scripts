'''
Sets up the supporting data for developing the "recommendation browser."

The scenario that this sets up is one where we're matching MIDL '19 reviewers
to MIDL '18 papers. We're doing this so that the MIDL '19 program chairs can
give us relevance judgments about
'''

from __future__ import print_function
from random import uniform
from random import sample
import sys
import openreview

CONFERENCE_ID = 'MIDL.amsterdam/2018/Conference'
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
GROUP_ID = 'MIDL.io/2019/Conference/Reviewers'
TAG_INVITATION_ID = CONFERENCE_ID + '/-/Recommendation'
ASSIGNMENT_INV_ID = CONFERENCE_ID + '/-/Paper_Assignment'

def setup_recommendations(create_assignments=False):
    client = openreview.Client()

    recommendation_tag_inv = openreview.Invitation(**{
        'id': TAG_INVITATION_ID,
        'readers': ['everyone'],
        'writers': [CONFERENCE_ID],
        'signatures': [CONFERENCE_ID],
        'invitees': ['~'],
        'multiReply': True,
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': SUBMISSION_ID,
            'readers': {
                'values': [CONFERENCE_ID]
            },
            'signatures': {
                'values-regex': '~.*'
            },
            'content': {
                'tag': {
                    'description': 'Recommendation',
                    'value-regex': '.*'
                }
            }
        }
    })
    client.post_invitation(recommendation_tag_inv)

    if create_assignments is True:
        paper_assignment_inv = openreview.Invitation(**{
            'id': ASSIGNMENT_INV_ID,
            'readers': ['everyone'],
            'writers': [CONFERENCE_ID],
            'signatures': [CONFERENCE_ID],
            'invitees': [CONFERENCE_ID],
            'reply': {
                'forum': None,
                'replyto': None,
                'invitation': SUBMISSION_ID,
                'readers': {
                    'values': [CONFERENCE_ID]
                },
                'signatures': {
                    'values': [CONFERENCE_ID]
                },
                'content': {}
            }
        })
        client.post_invitation(paper_assignment_inv)

        paper_submissions = client.get_notes(invitation=SUBMISSION_ID)
        reviewers_group = client.get_group(GROUP_ID)
        num_reviewers_to_assign = 5
        for paper in paper_submissions:
            assigned_groups = [
                {'conflicts': None, 'finalScore': uniform(0, 10), 'userId': userid, 'scores': {}}
                for userid in sample(reviewers_group.members, num_reviewers_to_assign)
            ]
            assignment_note = openreview.Note(**{
                'invitation': ASSIGNMENT_INV_ID,
                'forum': paper.forum,
                'replyto': paper.forum,
                'signatures': [CONFERENCE_ID],
                'writers': [CONFERENCE_ID],
                'readers': [CONFERENCE_ID],
                'content': {
                    'title': 'Recommendation Test',
                    'assignedGroups': assigned_groups,
                    'alternateGroups': []
                }
            })
            client.post_note(assignment_note)

    return True


if __name__ == '__main__':
    create_assignments = '--with-assignments' in sys.argv
    success = setup_recommendations(create_assignments=create_assignments)

    if success is True:
        print('Setup complete')
