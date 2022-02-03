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

print('running')
decision_super = openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Decision",
    readers = ["everyone"],
    writers = ["aclweb.org/ACL/2022/Conference"],
    signatures = ["aclweb.org/ACL/2022/Conference"],
    invitees = ["aclweb.org/ACL/2022/Conference/Program_Chairs"],
    reply = {
        "readers":{
            "values": [
                 "aclweb.org/ACL/2022/Conference",
                "aclweb.org/ACL/2022/Conference/Program_Chairs",
                "aclweb.org/ACL/2022/Conference/Senior_Area_Chairs"
             ]
                "aclweb.org/ACL/2022/Conference",
                "aclweb.org/ACL/2022/Conference/Senior_Area_Chairs"
                "{signatures}"
            ]
        },
        "writers":{
            "values-copied":[
                "aclweb.org/ACL/2022/Conference",
                "{signatures}"
            ]
        },
        "signatures":{
            "values-regex":"~.*"
        },
        "content": {
            "decision": {
                "order": 1,
                "value-radio": [
                    "1 - Accept to main conference",
                    "2 - Accept to findings",
                    "3 - Reject"
                ],
                "description": "Please select your decision",
                "required": True
                }
        }
    }
)
client.post_invitation(decision_super)

acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))
program_chairs_id = 'aclweb.org/ACL/2022/Conference/Program_Chairs'

for acl_blind_submission in tqdm(acl_blind_submissions):
    paper_track = sac_name_dictionary[acl_blind_submission.content["track"]]
    track_sac_id = f'aclweb.org/ACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    conflict_id = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Conflicts'
    decision = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Decision",
        super = "aclweb.org/ACL/2022/Conference/-/Decision",
        signatures = ["aclweb.org/ACL/2022/Conference"],
        multiReply= False,
        process = './decision_process.py',
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "signatures": {
                "values-regex": program_chairs_id,
                "description": "How your identity will be displayed."
            },
            "readers": {
                "values": [program_chairs_id, track_sac_id]
            },
            "writers": {
                "values": [program_chairs_id, track_sac_id]
            },
            "nonreaders": {
                "values": [conflict_id]
            }
        }
    )
)