import argparse
import openreview
from openreview import tools

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connected to "+client.baseurl)
CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
ACCEPTED_PAPER_ID = CONFERENCE_ID + '/-/Accepted_Papers'

# create invitation for notification frequency tags
notify_inv = openreview.Invitation(
    id='{}/-/Notification_Subscription'.format(CONFERENCE_ID),
    readers=['everyone'],
    invitees=['~'],
    writers=[CONFERENCE_ID],
    signatures=[CONFERENCE_ID],
    details={'writable': True},
    multiReply=False,
    reply={
        'invitation': ACCEPTED_PAPER_ID,
        'content': {
            "tag": {
                "required": True,
                "description": "Select Frequency",
                "value-dropdown": [
                    "Immediate",
                    "Daily",
                    "Weekly",
                    "Never"
                ]
            }
        },
        'signatures': {
            'description': 'Your authorized identity to be associated with the above content.',
            'values-regex': '~.*'
        },
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [CONFERENCE_ID, CONFERENCE_ID+'/Program_Chairs', '{signatures}']
        },
        'writers': {
            'values-copied': [CONFERENCE_ID, '{signatures}']
        }
    }
)
client.post_invitation(notify_inv)

# for each submission, create group (so sub invites can be published)
# create invite for comment
notes = tools.iterget_notes(client,invitation=conference_id+'/-/NeurIPS_Submission')

for note in notes:
    # need paper group to publish sub-groups
    paper_group = client.post_group(openreview.Group(
        id='{conference_id}/{number}'.format(conference_id=CONFERENCE_ID, number=note.number),
        signatures=[CONFERENCE_ID], signatories=[CONFERENCE_ID],
        readers=[CONFERENCE_ID], writers=[CONFERENCE_ID]))

    # add comment invite
    comment_inv = openreview.Invitation(
        id=paper_group.id+'/-/Comment',
        readers=['everyone'],
        invitees=['~'],
        writers=[CONFERENCE_ID],
        signatures=[CONFERENCE_ID],
        reply={
            'forum': note.forum,
            'replyto': None,
            'content': {
                'title': {
                    'value-regex': '.*',
                    'order': 0,
                    'required': True
                },
                'comment': {
                    'description': 'Your comment or reply (max 5000 characters).',
                    'order': 1,
                    'required': True,
                    'value-regex': '[\\S\\s]{1,5000}'
                }
            },
            'signatures': {
                'description': 'Your authorized identity to be associated with the above content.',
                'values-regex': '~.*'
            },
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values': ['everyone']
            },
            'writers': {
                'values-copied': [CONFERENCE_ID, '{signatures}']
            }
        },
        process='../process/commentProcess.py'
    )
    client.post_invitation(comment_inv)