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

with open('suggested_decision_pre_process.py') as g:
    pre_content = g.read()
    suggested_decision_super = openreview.Invitation(
        id = "aclweb.org/NAACL/2022/Conference/-/Suggested_Decision",
        readers = ["everyone"],
        writers = ["aclweb.org/NAACL/2022/Conference"],
        signatures = ["aclweb.org/NAACL/2022/Conference"],
        reply = {
            "content": {
                "suggested_decision": {
                    "order": 1,
                    "value-radio": [
                        "1 - definite accept",
                        "2 - possible accept to main conference",
                        "3 - possible accept to findings",
                        "4 - reject"
                    ],
                    "description": "Please select your suggested decision",
                    "required": True
                    },
                "justification": {
                    "order": 3,
                    "value-regex": "[\\S\\s]{1,200000}",
                    "description": "Provide justification for your suggested decision. Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq.",
                    "required": True,
                    "markdown": True
                    },
                "ranking":{
                    "order":2,
                    "value-regex": "^(5|\d)(\.\d{1,2})?$",
                    "description": "If you selected options 2 or 3, provide a numerical score for the paper. It should be a number between 1 and 5 with up to 2 decimal places.",
                    "required": False
                },
                "best_paper":{
                    "order":4,
                    "value-checkbox": "This is an outstanding paper that should be considered for a best paper award.",
                    "description": "Do you consider this paper an outstanding paper?",
                    "required": False
                },
                "best_paper_justification": {
                    "order": 5,
                    "value-regex": "[\\S\\s]{1,200000}",
                    "description": "Provide justification for selecting this as an outstanding paper. Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq.",
                    "required": False,
                    "markdown": True
                    },
            }
        },
    preprocess=pre_content
    )
    client.post_invitation(suggested_decision_super)

acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission'))
program_chairs_id = 'aclweb.org/NAACL/2022/Conference/Program_Chairs'

for acl_blind_submission in tqdm(acl_blind_submissions):
    paper_track = sac_name_dictionary[acl_blind_submission.content["track"]]
    track_sac_id = f'aclweb.org/NAACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    conflict_id = f'aclweb.org/NAACL/2022/Conference/Commitment{acl_blind_submission.number}/Conflicts'
    suggested_decision = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/NAACL/2022/Conference/Commitment{acl_blind_submission.number}/-/Suggested_Decision",
        super = "aclweb.org/NAACL/2022/Conference/-/Suggested_Decision",
        invitees = [track_sac_id, program_chairs_id],
        signatures = ["aclweb.org/NAACL/2022/Conference"],
        multiReply= False,
        process = './suggested_decision_process.py',
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "signatures": {
                "values-regex": track_sac_id,
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