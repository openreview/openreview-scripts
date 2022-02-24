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

desk_rejected_invitation = client.post_invitation(openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/-/Withdrawn_Submission",
    writers = ['aclweb.org/ACL/2022/Conference'],
    readers = ['aclweb.org/ACL/2022/Conference'],
    signatures = ['aclweb.org/ACL/2022/Conference'],
    reply = {
        "readers": {
            "values-regex": ".*"
        },
        "writers": {
            "values": [
                'aclweb.org/ACL/2022/Conference'
            ]
        },
        "signatures": {
            "values": [
                'aclweb.org/ACL/2022/Conference'
            ]
        },
        "content": {
            "authorids": {
                "values-regex": ".*"
                },
            "authors": {
                "values": [
                    "Anonymous"
                ]
            }
        }
    }
))



# Get all ACL 2022 Conference blind submissions
acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))
# For each blind submission, set the readers to the SAC track group
for acl_blind_submission in tqdm(acl_blind_submissions):
    author_group = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors'
    conflict_id = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Conflicts'
    paper_track = sac_name_dictionary[acl_blind_submission.content["track"]]
    track_sac_id = f'aclweb.org/ACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    desk_reject = client.post_invitation(openreview.Invitation(
        id = f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Withdraw",
        invitees = ["aclweb.org/ACL/2022/Conference/Program_Chairs","OpenReview.net/Support", author_group],
        readers = ["everyone"],
        writers = ["aclweb.org/ACL/2022/Conference"],
        signatures = ["~Super_User1"],
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "readers": {
                "values": [
                    "aclweb.org/ACL/2022/Conference/Program_Chairs",
                    track_sac_id,
                    author_group
                ]
                },
            "writers": {
                "values-copied": [
                    "aclweb.org/ACL/2022/Conference",
                    "{signatures}"
                ]
            },
            "nonreaders": {
                "values": [conflict_id]
            },
            "signatures": {
                "values": [
                    author_group
                ],
                "description": "How your identity will be displayed."
                },
            "content": {
                "title": {
                    "value": "Submission Withdrawn by Paper Authors",
                    "order": 1
                },
            "withdrawal confirmation": {
                "description": "Please confirm to withdraw.",
                "value-radio": [
                    "I have read and agree with the venue's withdrawal policy on behalf of myself and my co-authors."
                ],
                "order": 2,
                "required": True
                }
            }},
            process = './withdraw-ACL-process.py'
                ))
