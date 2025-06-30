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
    id='aclweb.org/NAACL/2022/Conference/-/Commitment_Camera_Ready_Revision',
    duedate=1650041991000, # March 15
    multiReply=True,
    readers=['everyone'],
    writers=['aclweb.org/NAACL/2022/Conference'],
    signatures=['aclweb.org/NAACL/2022/Conference'],
    reply={
        "content": {
            "title": {
                "description": "Enter the title of the ARR submission that you want to commit to NAACL 2022",
                "value-regex": ".{1,250}",
                "required": True,
                "order": 1
                },
                "authors": {
                    "description": "Comma separated list of author names.",
                    "order": 2,
                    "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                    "required": False,
                    "hidden": True
                    },
                "authorids": {
                    "description": "Search author profile by first, middle and last name or email address. If the profile is not found, you can add the author by completing first, middle, and last names as well as author email address.",
                    "order": 3,
                    "values-regex": "~.*|([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,},){0,}([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,})",
                    "required": True
                    },
            "pdf": {
                "description": "Upload a single PDF containing the paper, references and any appendices",
                "order": 5,
                "value-file": {
                    "fileTypes": [
                    "pdf"
                    ],
                    "size": 80
                },
                "required": True
                },
            "abstract": {
                "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 4,
                "value-regex": "[\\S\\s]{1,5000}",
                "required": True
                },  
            "dataset": {
                    "description": "Dataset zip file. The maximum file size is 100MB.",
                    "order": 6,
                    "value-file": {
                        "fileTypes": [
                            "zip"
                        ],
                        "size": 100
                    },
                    "required": False
                },
            "software": {
                "description": "Each ARR submission can be accompanied by one .tgz or .zip archive containing software (max. 200MB).",
                "order": 21,
                "value-file": {
                    "fileTypes": [
                    "tgz",
                    "zip"
                    ],
                    "size": 200
                },
                "required": False
                },
               "Response_to_Ethics_Reviews_(for_Conditionally_Accepted_Papers_Only)": {
                "description": "Optional Response to Ethics Reviews",
                "order": 21,
                "value-regex": "[\\S\\s]{1,5000}",
                "required": False
                },
                "Application_for_Reproducibility_Badges": {
                    "description": "The Reproducibility Track at NAACL 2022 allows authors to earn up to three reproducibility badges: 1. Open-Source Code Badge, 2. Trained Model Badge, 3. Reproducible Results Badge. Fill in this form https://forms.office.com/r/BmTTJ5fKfH to apply.",
                        "values-checkbox": [
                        ],
                        "required": False,
                        "order": 50
                        }
            }
    }
)
client.post_invitation(super_invitation)
submissions=list(openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/-/Blind_Submission', details='original'))
decision_by_forum={ d.forum: d for d in list(openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/Commitment.*/-/Decision'))}

for submission in tqdm(submissions):
    decision = decision_by_forum.get(submission.id)
    if decision:
        if 'Accept' in decision.content['decision']:
            r=client.post_invitation(openreview.Invitation(
                id=f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/-/Camera_Ready_Revision',
                super='aclweb.org/NAACL/2022/Conference/-/Commitment_Camera_Ready_Revision',
                writers=['aclweb.org/NAACL/2022/Conference'],
                signatures=['aclweb.org/NAACL/2022/Conference'],
                readers=['everyone'],
                invitees=['aclweb.org/NAACL/2022/Conference', f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Authors'],
                reply={
                    'forum': submission.original,
                    'referent': submission.original,
                    'readers': {
                        'values': [
                            'aclweb.org/NAACL/2022/Conference',
                            f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Authors'
                        ]
                    },
                    'writers': {
                        'values': [
                            'aclweb.org/NAACL/2022/Conference',
                            f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Authors'
                        ]
                    },
                    'signatures': {
                        'values-regex': f'aclweb.org/NAACL/2022/Conference/Program_Chairs|aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Authors'
                    }                    
                }
            ))
    else:
        print('decision not found')