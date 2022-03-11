import argparse
import openreview
from tqdm import tqdm
import csv
from openreview import tools
import re
from collections import defaultdict

"""
OPTIONAL SCRIPT ARGUMENTS
    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password
"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--confid')

args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
confid = args.confid
super_invitation = openreview.Invitation(
    id=f'{confid}/-/Commitment_Camera_Ready_Revision',
    duedate=1647388799000, # March 15
    multiReply=True,
    readers=['everyone'],
    writers=[confid],
    signatures=[confid],
    reply={
        "content": {"pdf": {
          "description": "Upload a single PDF containing the paper, references and any appendices",
          "order": 1,
          "value-file": {
            "fileTypes": [
              "pdf"
            ],
            "size": 80
          },
          "required": True
        },
        "copyright_consent": {
            "description": "Check to submit",
            "value-checkbox": "I consent ACL Conference Copyright",
            "order": 2,
            "required": True
        },
        "dataset": {
            "description": "Dataset zip file. The maximum file size is 100MB.",
            "order": 3,
            "value-file": {
                "fileTypes": [
                    "zip"
                ],
                "size": 100
            },
            "required": False
        },
        "code": {
            "description": "Code zip file. The maximum file size is 100MB.",
            "order": 4,
            "value-file": {
                "fileTypes": [
                    "zip"
                ],
                "size": 100
            },
            "required": False
        }}
    }
    
)
client.post_invitation(super_invitation)
submissions=list(openreview.tools.iterget_notes(client, invitation=f'{confid}/-/Commitment_Submission'))
decision_by_forum={ d.forum: d for d in list(openreview.tools.iterget_notes(client, invitation=f'{confid}/Commitment.*/-/Decision'))}

for submission in tqdm(submissions):
    decision = decision_by_forum.get(submission.id)
    if decision:
        if 'Accept' in decision.content['decision']:
            r=client.post_invitation(openreview.Invitation(
                id=f'{confid}/Commitment{submission.number}/-/Camera_Ready_Revision',
                super=f'{confid}/-/Commitment_Camera_Ready_Revision',
                writers=[confid],
                signatures=[confid],
                readers=['everyone'],
                invitees=[confid, f'{confid}/Commitment{submission.number}/Authors'],
                reply={
                    'forum': submission.id,
                    'referent': submission.id,
                    'readers': {
                        'values': [
                            confid,
                            f'{confid}/Commitment{submission.number}/Authors'
                        ]
                    },
                    'writers': {
                        'values': [
                            confid,
                            f'{confid}/Commitment{submission.number}/Authors'
                        ]
                    },
                    'signatures': {
                        'values-regex': f'{confid}/Program_Chairs|{confid}/Commitment{submission.number}/Authors'
                    }                    
                }
            ))
            print(r)
    else:
        print('decision not found')