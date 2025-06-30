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

comment_super = openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Comment",
    readers = ["everyone"],
    writers = ["aclweb.org/ACL/2022/Conference"],
    signatures = ["aclweb.org/ACL/2022/Conference"],
    reply = {
    "replyto": None,
    "content": {
        "title": {
            "order": 0,
            "value-regex": ".{1,500}",
            "description": "Brief summary of your comment.",
            "required": True
        },
        "comment": {
            "order": 1,
            "value-regex": "[\\S\\s]{1,5000}",
            "description": "Your comment or reply (max 5000 characters). Add formatting using Markdown and formulas using LaTeX. For more information see https://openreview.net/faq",
            "required": True,
            "markdown": True
        }
    }
}

)
client.post_invitation(comment_super)
program_chairs_id = 'aclweb.org/ACL/2022/Conference/Program_Chairs'

acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))
# For each blind submission, post the comment invitation
for acl_blind_submission in tqdm(acl_blind_submissions):
    paper_track = sac_name_dictionary[acl_blind_submission.content["track"]]
    track_sac_id = f'aclweb.org/ACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    conflict_id = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Conflicts'
    comment = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Comment",
        super = "aclweb.org/ACL/2022/Conference/-/Comment",
        invitees = [track_sac_id, 'aclweb.org/ACL/2022/Conference/Program_Chairs', 'aclweb.org/ACL/2022/Conference/Ethics_Chairs'],
        signatures = ["aclweb.org/ACL/2022/Conference"],
        process = "./commentProcess.js",
        reply = {
            "forum": acl_blind_submission.forum,
            "signatures": {
                "values-regex": f'{program_chairs_id}|{track_sac_id}|aclweb.org/ACL/2022/Conference/Ethics_Chairs',
                "description": "How your identity will be displayed."
            },
            "readers": {
                "values": [program_chairs_id, track_sac_id, 'aclweb.org/ACL/2022/Conference/Ethics_Chairs']
            },
            "writers": {
                "values": [program_chairs_id, track_sac_id, 'aclweb.org/ACL/2022/Conference/Ethics_Chairs']
            },
            "nonreaders": {
                "values": [conflict_id]
            }
        }
    ))