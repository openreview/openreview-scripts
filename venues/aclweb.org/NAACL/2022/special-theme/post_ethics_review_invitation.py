import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
import flagged_papers

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
program_chairs_id = 'aclweb.org/NAACL/2022/Conference/Program_Chairs'


ethics_review_super = openreview.Invitation(
    id = "aclweb.org/NAACL/2022/Conference/-/Special_Theme_Ethics_Review",
    readers = ["everyone"],
    writers = ["aclweb.org/NAACL/2022/Conference"],
    signatures = ["aclweb.org/NAACL/2022/Conference"],
    reply = {
        "writers":{
            "values-copied":[
                "aclweb.org/NAACL/2022/Conference",
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
submissions_forum_list = flagged_papers.flagged_papers

blind_submission_by_number = { s.number: s for s in openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/-/Blind_Special_Theme_Submission')}
submission_by_number = { s.number: s for s in openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/-/Special_Theme_Submission')}
# For Each submission, create reviewer group, add reviewer group and AC group to readers
for submission_number in tqdm(submissions_forum_list):
    acl_blind_submission = blind_submission_by_number[submission_number]
    track_sac_id = f'aclweb.org/NAACL/2022/Conference/Senior_Area_Chairs'
    ethics_reviewer_id = f'aclweb.org/NAACL/2022/Conference/Paper{acl_blind_submission.number}/Special_Theme_Ethics_Reviewers'
    ethics_ac_id = f'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Chairs'
    ethics_review = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/NAACL/2022/Conference/Paper{acl_blind_submission.number}/-/Special_Theme_Ethics_Review",
        super = "aclweb.org/NAACL/2022/Conference/-/Special_Theme_Ethics_Review",
        invitees = [ethics_reviewer_id, program_chairs_id, ethics_ac_id],
        signatures = ["aclweb.org/NAACL/2022/Conference"],
        multiReply= False,
        process = './ethics_review_process.py',
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "signatures": {
                "values-regex": f'aclweb.org/NAACL/2022/Conference/Paper{acl_blind_submission.number}/Special_Theme_Ethics_Reviewer_.*|aclweb.org/NAACL/2022/Conference/Program_Chairs|aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Chairs',
                "description": "How your identity will be displayed."
            },
            "readers": {
                "values-copied": [program_chairs_id, ethics_ac_id, ethics_reviewer_id, track_sac_id]
            },
            "writers": {
                "values": [program_chairs_id, ethics_reviewer_id, ethics_ac_id]
            }
        }
    )
)