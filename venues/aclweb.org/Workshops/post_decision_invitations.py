import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
import decision_process

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
# Posts decision invitations to all commitment submission invitations 
args = parser.parse_args()
confid = args.confid
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
program_chairs_id = "{confid}/Program_Chairs"

with open('decision_process.py') as d:
    content = d.read()
    process = content.replace("CONFERENCE_ID = ''", f"CONFERENCE_ID = '{confid}'")
    process = process.replace("CONFERENCE_SHORT_NAME = ''", f"CONFERENCE_SHORT_NAME = '{confid.split('/')[-1]}'")
    decision_super = openreview.Invitation(
        id = f"{confid}/-/Commitment_Decision",
        readers = ["everyone"],
        writers = [f"{confid}"],
        signatures = [f"{confid}"],
        invitees = [f"{confid}/Program_Chairs"],
        reply = {
            "readers":{
                "values": [
                    f"{confid}",
                    f"{confid}/Program_Chairs"
                    "{signatures}"
                ]
            },
            "writers":{
                "values-copied":[
                    f"{confid}",
                    "{signatures}"
                ]
            },
            "signatures":{
                "values-regex":program_chairs_id
            },
            "content": {
                "decision": {
                    "order": 1,
                    "value-radio": [
                        "Accept",
                        "Reject"
                    ],
                    "description": "Please select your decision",
                    "required": True
                    },
                    "comment": {
                    "order": 2,
                    "value-regex": "[\\S\\s]{1,200000}",
                    "description": "Provide an optional comment about your decision",
                    "required": False
                    }
            }
            
        }
    )
    client.post_invitation(decision_super)

    acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/Blind_Commitment_Submission'))
    program_chairs_id = f'{confid}/Program_Chairs'

    for acl_blind_submission in tqdm(acl_blind_submissions):
        author_id = f'{confid}/Commitment{acl_blind_submission.number}/Authors'
        conflict_id = f'{confid}/Commitment{acl_blind_submission.number}/Conflicts'
        decision = client.post_invitation(openreview.Invitation(
            id = f"{confid}/Commitment{acl_blind_submission.number}/-/Decision",
            super = f"{confid}/-/Commitment_Decision",
            signatures = [confid],
            multiReply= False,
            process_string = process,
            reply = {
                "forum": acl_blind_submission.forum,
                "replyto": acl_blind_submission.forum,
                "signatures": {
                    "values-regex": program_chairs_id,
                    "description": "How your identity will be displayed."
                },
                "readers": {
                    "values": [program_chairs_id, author_id]
                },
                "writers": {
                    "values": [program_chairs_id]
                }
            }
        )
    )