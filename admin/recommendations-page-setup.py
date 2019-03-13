'''
Sets up the supporting data for developing the "recommendation browser."

The scenario that this sets up is one where we're matching MIDL '19 reviewers
to MIDL '18 papers. We're doing this so that the MIDL '19 program chairs can
give us relevance judgments about
'''

from __future__ import print_function
import openreview

CONFERENCE_ID = 'MIDL.amsterdam/2018/Conference'
CONFIG_INV_ID = CONFERENCE_ID + '/-/Recommendation'
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
CONSTRAINTS_INV_ID = CONFIG_INV_ID + '/Value'
ASSIGNMENT_INV_ID = CONFERENCE_ID + '/-/Paper_Assignment'

## This is intentional! We're matching current MIDL reviewers with past papers.
REVIEWERS_ID = 'MIDL.io/2019/Conference/Reviewers'

def setup_recommendations():
    config_inv = openreview.Invitation(**{
        'id': CONFIG_INV_ID,
        'readers': [CONFERENCE_ID],
        'writers': [CONFERENCE_ID],
        'signatures': [CONFERENCE_ID],
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': None,
            'readers': {'values': [CONFERENCE_ID]},
            'writers': {'values': [CONFERENCE_ID]},
            'signatures': {'values': [CONFERENCE_ID]},
            'content': {
                'submission_invitation': {
                    'value': SUBMISSION_ID
                },
                'recommendation_invitation': {
                    'value': CONSTRAINTS_INV_ID
                },
                'assignment_invitation': {
                    'value': ASSIGNMENT_INV_ID
                },
                'group': {
                    'value': REVIEWERS_ID,
                }
            }
        }
    })

    config_note = openreview.Note(**{
        'invitation': CONFIG_INV_ID,
        'readers': [CONFERENCE_ID],
        'writers': [CONFERENCE_ID],
        'signatures': [CONFERENCE_ID],
        'content': {
            'submission_invitation': SUBMISSION_ID,
            'recommendation_invitation': CONSTRAINTS_INV_ID,
            'assignment_invitation': ASSIGNMENT_INV_ID,
            'group': REVIEWERS_ID
        }
    })

    recommendation_tag_inv = openreview.Invitation(**{
        'id': CONSTRAINTS_INV_ID,
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
                    'value-regex': '.*'
                }
            }
        }
    })

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

    client = openreview.Client()

    client.post_invitation(config_inv)
    note_response = client.post_note(config_note)
    client.post_invitation(recommendation_tag_inv)
    client.post_invitation(paper_assignment_inv)

    print('Recommendation config note ID: ' + note_response.id)

    midl18_submissions = client.get_notes(invitation=SUBMISSION_ID)
    reviewers_group = client.get_group(REVIEWERS_ID)
    assigned_groups = [
        {'conflicts': None, 'finalScore': 0.0, 'userId': userid, 'scores': {}}
        for userid in reviewers_group.members
    ]

    for paper in midl18_submissions:
        assignment_note = openreview.Note(**{
            'invitation': ASSIGNMENT_INV_ID,
            'forum': paper.forum,
            'replyto': paper.forum,
            'signatures': [CONFERENCE_ID],
            'writers': [CONFERENCE_ID],
            'readers': [CONFERENCE_ID],
            'content': {
                'title': config_note.content['title'],
                'assignedGroups': assigned_groups,
                'alternateGroups': []
            }
        })
        client.post_note(assignment_note)

    return true


if __name__ == '__main__':
    success = setup_recommendations()

    if success is True
        print('Setup complete')
