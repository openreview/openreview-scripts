
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
conference_id = 'NeurIPS.cc/2019/Reproducibility_Challenge'

# create invitation for notification frequency tags
notify_inv = openreview.Invitation(
    id='{}/-/Notification_Subscription'.format(conference_id),
    readers=['everyone'],
    invitees=['~'],
    writers=[conference_id],
    signatures=[conference_id],
    details={'writable': True},
    multiReply=False,
    reply={
        'invitation': conference_id+"/-/NeurIPS_Submission",
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
            'values': [conference_id, conference_id+'/Program_Chairs', '{signatures}']
        },
        'writers': {
            'values-copied': [conference_id, '{signatures}']
        }
    }
)
client.post_invitation(notify_inv)

# for each submission, create group (so sub invites can be published)
# create invite for comment
notes = tools.iterget_notes(client,invitation=conference_id+'/-/NeurIPS_Submission')
claims = tools.iterget_notes(client, invitation=conference_id+'/-/Claim')
claims_by_forum = {}
for claim in claims:
    if claim.forum not in claims_by_forum:
        claims_by_forum[claim.forum] = []
    claimants = set()
    claimants.add(claim.tauthor)
    if 'team_emails' in claim.content:
        for t in claim.content['team_emails']:
            claimants.add(t)
    claims_by_forum[claim.forum].append(claimants)

for note in notes:
    # need paper group to publish sub-groups
    paper_group = client.post_group(openreview.Group(
        id='{conference_id}/{number}'.format(conference_id=conference_id, number=note.number),
        signatures=[conference_id], signatories=[conference_id],
        readers=[conference_id], writers=[conference_id]))

    # paper claimants group
    claimants = claims_by_forum.get(note.forum, [])

    for index, claimant in enumerate(claimants):
        group_id = paper_group.id + '/Claimants' + str(index+1)
        claimants_paper_group = client.post_group(openreview.Group(
            id = group_id,
            members = list(claimant),
            readers = [conference_id, group_id],
            writers = [conference_id],
            signatures = [conference_id],
            signatories = [group_id]
        ))
        print(claimants_paper_group.id)

    # add comment invite
    comment_inv = openreview.Invitation(
        id=paper_group.id+'/-/Comment',
        readers=['everyone'],
        invitees=['~'],
        writers=[conference_id],
        signatures=[conference_id],
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
                'values-regex': '~.*|' + paper_group.id + '/Claimants.*'
            },
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values': ['everyone']
            },
            'writers': {
                'values-copied': [conference_id, '{signatures}']
            }
        },
        process='../process/commentProcess.py'
    )
    client.post_invitation(comment_inv)