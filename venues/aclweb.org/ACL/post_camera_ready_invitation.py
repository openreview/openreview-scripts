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
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

super_invitation = openreview.Invitation(
    id='aclweb.org/ACL/2022/Conference/-/Camera_Ready_Revision',
    duedate=1647388799000, # March 15
    multiReply=True,
    readers=['everyone'],
    writers=['aclweb.org/ACL/2022/Conference'],
    signatures=['aclweb.org/ACL/2022/Conference'],
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
submissions=list(openreview.tools.iterget_notes(client, invitation='aclweb.org/ACL/2022/Conference/-/Blind_Submission', details='original'))
decision_by_forum={ d.forum: d for d in list(openreview.tools.iterget_notes(client, invitation='aclweb.org/ACL/2022/Conference/Paper.*/-/Decision'))}

for submission in tqdm(submissions):
    decision = decision_by_forum.get(submission.id)
    if decision:
        if 'Accept' in decision.content['decision']:
            r=client.post_invitation(openreview.Invitation(
                id=f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/-/Camera_Ready_Revision',
                super='aclweb.org/ACL/2022/Conference/-/Camera_Ready_Revision',
                writers=['aclweb.org/ACL/2022/Conference'],
                signatures=['aclweb.org/ACL/2022/Conference'],
                readers=['everyone'],
                invitees=['aclweb.org/ACL/2022/Conference', f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Authors'],
                reply={
                    'forum': submission.original,
                    'referent': submission.original,
                    'readers': {
                        'values': [
                            'aclweb.org/ACL/2022/Conference',
                            f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Authors'
                        ]
                    },
                    'writers': {
                        'values': [
                            'aclweb.org/ACL/2022/Conference',
                            f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Authors'
                        ]
                    },
                    'signatures': {
                        'values-regex': f'aclweb.org/ACL/2022/Conference/Program_Chairs|aclweb.org/ACL/2022/Conference/Paper{submission.number}/Authors'
                    }                    
                }
            ))
    else:
        print('decision not found')