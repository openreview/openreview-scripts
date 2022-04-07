import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
import tracks

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
sac_name_dictionary = tracks.sac_name_dictionary
program_chairs_id = "aclweb.org/NAACL/2022/Conference/Program_Chairs"

decision_super = openreview.Invitation(
    id = "aclweb.org/NAACL/2022/Conference/-/Commitment_Decision",
    readers = ["everyone"],
    writers = ["aclweb.org/NAACL/2022/Conference"],
    signatures = ["aclweb.org/NAACL/2022/Conference"],
    invitees = ["aclweb.org/NAACL/2022/Conference/Program_Chairs"],
    reply = {
        "readers":{
            "values": [
                "aclweb.org/NAACL/2022/Conference",
                "aclweb.org/NAACL/2022/Conference/Program_Chairs"
                "{signatures}"
            ]
        },
        "writers":{
            "values-copied":[
                "aclweb.org/NAACL/2022/Conference",
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
                    "Accept - Findings",
                    "Conditional Accept",
                    "Conditionat Accept - Findings",
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

acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission'))
program_chairs_id = 'aclweb.org/NAACL/2022/Conference/Program_Chairs'

for acl_blind_submission in tqdm(acl_blind_submissions):
    conflict_id = f'aclweb.org/NAACL/2022/Conference/Commitment{acl_blind_submission.number}/Conflicts'
    decision = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/NAACL/2022/Conference/Commitment{acl_blind_submission.number}/-/Decision",
        super = "aclweb.org/NAACL/2022/Conference/-/Commitment_Decision",
        signatures = ["aclweb.org/NAACL/2022/Conference"],
        multiReply= False,
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "signatures": {
                "values-regex": program_chairs_id,
                "description": "How your identity will be displayed."
            },
            "readers": {
                "values": [program_chairs_id]
            },
            "writers": {
                "values": [program_chairs_id]
            },
            "nonreaders": {
                "values": [conflict_id]
            }
        }
    )
)