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
program_chairs_id = 'aclweb.org/ACL/2022/Conference/Program_Chairs'

    
ethics_review_super = openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Ethics_Review",
    readers = ["everyone"],
    writers = ["aclweb.org/ACL/2022/Conference"],
    signatures = ["aclweb.org/ACL/2022/Conference"],
    reply = {
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
            "recommendation": {
                "order": 1,
                "value-radio": [
                    "1 - No serious ethical issues",
                    "2 - Serious ethical issues that need to be addressed in the final version",
                    "3 - Paper should be rejected due to ethical issues"
                ],
                "description": "Please select your ethical recommendation",
                "required": True
                },
            "ethics_review": {
                "order": 3,
                "value-regex": "[\\S\\s]{1,200000}",
                "description": "Provide justification for your suggested ethics issues. Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq.",
                "required": True,
                "markdown": True
                }
        }
    }
)
client.post_invitation(ethics_review_super)
submissions_forum_list = ['_SmerUlTll0']
# For Each submission, create reviewer group, add reviewer group and AC group to readers 
for submission_forum in tqdm(submissions_forum_list): 
    acl_blind_submission = client.get_note(submission_forum)
    paper_track = sac_name_dictionary[acl_blind_submission.content["track"]]
    track_sac_id = f'aclweb.org/ACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    conflict_id = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Conflicts'
    ethics_reviewer_id = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Ethics_Reviewers'
    ethics_ac_id = f'aclweb.org/ACL/2022/Conference/Ethics_Area_Chairs'
    
    ethics_review = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Ethics_Review",
        super = "aclweb.org/ACL/2022/Conference/-/Ethics_Review",
        invitees = [ethics_reviewer_id, program_chairs_id, ethics_ac_id], 
        signatures = ["aclweb.org/ACL/2022/Conference"],
        multiReply= False,
        process = './ethics_review_process.py',
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "signatures": {
                "values-regex": f'aclweb.org/ACL/2022/Conference/Paper404/Ethics_Reviewer_.*|aclweb.org/ACL/2022/Conference/Ethics_Area_Chairs|aclweb.org/ACL/2022/Conference/Program_Chairs', 
                "description": "How your identity will be displayed."
            },
            "readers": {
                "values": [program_chairs_id, ethics_ac_id, ethics_reviewer_id]
            },
            "writers": {
                "values": [program_chairs_id, ethics_ac_id, ethics_reviewer_id]
            },
            "nonreaders": {
                "values": [conflict_id]
            }
        }
    )
)