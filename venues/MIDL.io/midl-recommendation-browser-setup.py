'''
Sets up the supporting data for developing the "recommendation browser."

The scenario that this sets up is one where we're matching MIDL '19 reviewers
to MIDL '18 papers. We're doing this so that the MIDL '19 program chairs can
give us relevance judgments about
'''

import openreview

CONFERENCE_ID = 'MIDL.amsterdam/2018/Conference'
CONFIG_INV_ID = CONFERENCE_ID + '/-/Assignment_Configuration'
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
CONSTRAINTS_INV_ID = CONFIG_INV_ID + '/Lock'
ASSIGNMENT_INV_ID = CONFERENCE_ID + '/-/Paper_Assignment'

# YES, this is intentional! We're matching current MIDL reviewers with past papers.
REVIEWERS_ID = 'MIDL.io/2019/Conference/Reviewers'

config_inv = openreview.Invitation.from_json({
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
            "title": {
                "value-regex": ".{1,250}",
                "required": True,
                "description": "Title of the configuration.",
                "order": 1
            },
            'paper_invitation': {
                "value": SUBMISSION_ID
            },
            'constraints_invitation': {
                "value": CONSTRAINTS_INV_ID
            },
            'assignment_invitation': {
                "value": ASSIGNMENT_INV_ID
            },
            'match_group': {
                "value": REVIEWERS_ID,
            },
            "scores_names": {
                "values": ['affinity', 'bid']
            },
            "status": {
                "value": 'Complete'
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
        'title': 'recommendations',
        'paper_invitation': SUBMISSION_ID,
        'constraints_invitation': CONSTRAINTS_INV_ID,
        'assignment_invitation': ASSIGNMENT_INV_ID,
        'match_group': REVIEWERS_ID,
        'scores_names': ['affinity','bid'],
        'status': 'Complete'
    }
})

lock_tag_inv = openreview.Invitation(**{
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
            'values': [
                CONFERENCE_ID
            ]
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': {
            'tag': {
                'value-regex': '.*'
            }
        }
    }})

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
            'values': [
                CONFERENCE_ID
            ]
        },
        'signatures': {
            'values': [
                CONFERENCE_ID
            ]
        },
        'content': {}
    }
})


if __name__ == '__main__':
    client = openreview.Client()
    client.post_invitation(config_inv)
    client.post_note(config_note)
    client.post_invitation(lock_tag_inv)
    client.post_invitation(paper_assignment_inv)

    midl18_submissions = client.get_notes(invitation=SUBMISSION_ID)
    reviewers_group = client.get_group(REVIEWERS_ID)

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
                'assignedGroups': [],
                'alternateGroups': [{'conflicts': None, 'finalScore': 0.0, 'userId': userid, 'scores': {} } for userid in reviewers_group.members]
            }
        })
        client.post_note(assignment_note)
