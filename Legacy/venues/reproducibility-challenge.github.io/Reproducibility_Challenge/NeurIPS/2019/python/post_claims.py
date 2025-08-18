import openreview
from openreview import tools
from openreview import invitations
import datetime

client = openreview.Client()
print(client.baseurl)
conference_id = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'


#PAM TODO remember to expire Claim invites manually in November

# Claimant group - those that will be able to see the Report Submisson button
client.post_group(openreview.Group(
    id=conference_id+'/Claimants',
    readers=[conference_id+'Program_Chairs'],
    nonreaders=[],
    writers=[conference_id],
    signatories=[conference_id],
    signatures=['~Super_User1'],
    members=[],
    details={ 'writable': True })
)

claim_inv = client.post_invitation(openreview.Invitation(
    id='{}/-/Claim'.format(conference_id),
    readers=['everyone'],
    invitees=['~'],
    writers=[conference_id],
    signatures=[conference_id],
    reply={
        'content': {
            'title': {
                'value': 'Claim',
                'order': 0,
                'required': True
            },
            'plan': {'description': 'Your plan to reproduce results(max 5000 chars).',
                'order': 1,
                'required': True,
                'value-regex': '[\\S\\s]{1,5000}'
            },
            'institution': {
                'description': 'Your institution or organization(max 100 chars).',
                'order': 2,
                'required': True,
                'value-regex': '.{1,100}'
            }
        },
        'invitation': '{}/-/NeurIPS_Submission'.format(conference_id),
        'signatures': {
            'description': 'Your authorized identity to be associated with the above content.',
            'values-regex': '~.*'
        },
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [conference_id + '/Program_Chairs', '{signatures}']
        },
        'writers': {
            'values-copied': [conference_id,'{signatures}']
        }
    },
    process='../process/claimProcess.py'
))


claim_hold_inv = client.post_invitation(openreview.Invitation(
    id='{}/-/Claim_Hold'.format(conference_id),
    readers=[],
    invitees=['~'],
    writers=[conference_id],
    signatures=[conference_id],
    reply={
        'content': {
            'title': {
                'value-regex': '.{1,120}',
                'order': 0,
                'required': True
            }
        },
        'invitation': '{}/-/NeurIPS_Submission'.format(conference_id),
        'signatures': {'values': [conference_id]},
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'writers': {
            'values-copied': [conference_id]
        }
    }
))

