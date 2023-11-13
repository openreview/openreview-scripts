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
    duedate=1651622834000, # March 15
    multiReply=True,
    readers=['everyone'],
    writers=[confid],
    signatures=[confid]  
)
client.post_invitation(super_invitation)
submissions=list(openreview.tools.iterget_notes(client, invitation=f'{confid}/-/Blind_Commitment_Submission', details = 'original'))
decision_by_forum={ d.forum: d for d in list(openreview.tools.iterget_notes(client, invitation=f'{confid}/Commitment.*/-/Decision'))}
short_phrase = confid.split('/')[-1]  
for submission in tqdm(submissions):
    print(submission.original)
    with open('camera_ready_process.py') as d:
      content = d.read()
      short_phrase = confid.split('/')[-1]
      process = content.replace("SHORT_PHRASE = ''", f"SHORT_PHRASE = '{short_phrase}'")
      process = process.replace("AUTHOR_ID = ''", f"AUTHOR_ID = '{confid}/Commitment{submission.number}/Authors'")
    original_submission = client.get_note(submission.original)
    
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
                process_string = process,
                reply={
                    'forum': original_submission.id,
                    'referent': original_submission.id,
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
                    },
                    'content':   {
                          'authors': {
                              'values': submission.details["original"]["content"]['authors'],
                              'required': True,
                              'hidden': True,
                              'order': 2
                          },
                          'authorids': {
                              'values': submission.details["original"]["content"]['authorids'],
                              'required': True,
                              'order': 3
                          },
                          "title": {
                            "description": "Enter the title of the ARR submission that you want to commit to MIA",
                            "order": 1,
                            "value-regex": ".{1,250}",
                            "required": False
                          },
                          "existing_preprints": {
                            "values-regex": ".{1,500}",
                            "description": "If there are any publicly available non-anonymous preprints of this paper, please list them here (provide the URLs please).",
                            "required": False,
                            "order": 7
                          },
                          "archival": {
                            "description": "Please indicate if you want your paper to be archival or non-archival.",
                            "value-radio": [
                            "Archival",
                            "Non-Archival"
                            ],
                            "order": 8,
                            "required": False
                        },
                        "abstract": {
                          "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$.",
                          "order": 4,
                          "value-regex": "[\\S\\s]{1,5000}",
                          "required": False
                        },
                        "pdf": {
                          "description": "Upload a single PDF containing the paper, references and any appendices. Please refer to the CFP (https://aclrollingreview.org/cfp) and author checklist (https://aclrollingreview.org/authorchecklist). Failure to follow the rules regarding format, anonymization, authorship, citation and comparison, and multiple submission will lead to desk rejection.",
                          "order": 5,
                          "value-file": {
                            "fileTypes": [
                              "pdf"
                            ],
                            "size": 80
                          },
                          "required": False
                        }
                    }                  
                }
            ))
            
    else:
        print('decision not found')