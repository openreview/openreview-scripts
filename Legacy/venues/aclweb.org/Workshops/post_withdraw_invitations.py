import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv

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

desk_rejected_invitation = client.post_invitation(openreview.Invitation(
    id = f"{confid}/-/Withdrawn_Commitment_Submission",
    writers = [confid],
    readers = [confid],
    signatures = [confid],
    reply = {
        "readers": {
            "values-regex": ".*"
        },
        "writers": {
            "values": [
                confid
            ]
        },
        "signatures": {
            "values": [
                confid
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
            },
            "title": {
      "value-regex": ".*"
    },
    "abstract": {
      "value-regex": ".*"
    },
    "pdf": {
      "value-regex": ".*"
    },
    "software": {
      "value-regex": ".*"
    },
    "data": {
      "value-regex": ".*"
    },
    "paper_link": {
      "value-regex": ".*"
    },
    "paper_type": {
      "value-regex": ".*"
    },
    "track": {
      "value-regex": ".*"
    },
    "comment": {
      "value-regex": ".*"
    },
    "authorship": {
      "value-regex": ".*"
    },
    "paper_version": {
      "value-regex": ".*"
    },
    "anonymity_period": {
      "value-regex": ".*"
    },
    "commitment_note": {
      "value-regex": ".*"
    },
    "ACL_preprint": {
      "value-regex": ".*"
    },
    "preprint": {
      "value-regex": ".*"
    },
    "existing_preprints": {
      "value-regex": ".*"
    },
    "previous_URL": {
      "value-regex": ".*"
    },
    "TL;DR": {
      "value-regex": ".*"
    },
    "author_profiles": {
      "value-regex": ".*"
    },
    "country_of_affiliation_of_corresponding_author": {
      "value-regex": ".*"
    },
    "paper_link": {
      "value-regex": ".*"
    }
        }
    }
))



# Get all ACL 2022 Conference blind submissions
acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/Blind_Commitment_Submission'))

# For each blind submission, set the readers to the SAC track group
for acl_blind_submission in tqdm(acl_blind_submissions):
    with open('withdraw-ACL-process.py') as d:
      content = d.read()
      short_phrase = confid.split('/')[-1]
      process = content.replace("CONFERENCE_SHORT_NAME = ''", f"CONFERENCE_SHORT_NAME = '{short_phrase}'")
      process = process.replace("WITHDRAWN_SUBMISSION_ID = ''", f"WITHDRAWN_SUBMISSION_ID = '{confid}/-/Withdrawn_Commitment_Submission'")
      process = process.replace("PAPER_AUTHORS_ID = ''", f"PAPER_AUTHORS_ID = '{confid}/Commitment{acl_blind_submission.number}/Authors'")
    author_group = f'{confid}/Commitment{acl_blind_submission.number}/Authors'
    conflict_id = f'{confid}/Commitment{acl_blind_submission.number}/Conflicts'
    desk_reject = client.post_invitation(openreview.Invitation(
        id = f"{confid}/Commitment{acl_blind_submission.number}/-/Withdraw",
        invitees = [f"{confid}/Program_Chairs","OpenReview.net/Support", author_group],
        readers = ["everyone"],
        writers = [confid],
        signatures = ["~Super_User1"],
        reply = {
            "forum": acl_blind_submission.forum,
            "replyto": acl_blind_submission.forum,
            "readers": {
                "values": [
                    f"{confid}/Program_Chairs",
                    author_group
                ]
                },
            "writers": {
                "values-copied": [
                    confid,
                    "{signatures}"
                ]
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
            process_string = process
                ))
