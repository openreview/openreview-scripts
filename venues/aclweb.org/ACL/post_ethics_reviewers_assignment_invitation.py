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

assignment_invitation = openreview.Invitation(
    id = "aclweb.org/ACL/2022/Conference/Ethics_Reviewers/-/Assignment",
    readers = ["aclweb.org/ACL/2022/Conference", "aclweb.org/ACL/2022/Conference/Ethics_Chairs"],
    writers = ["aclweb.org/ACL/2022/Conference"],
    signatures = ["aclweb.org/ACL/2022/Conference"],
    reply = {
        "readers": {
            "values-copied": [
                "aclweb.org/ACL/2022/Conference"
                "aclweb.org/ACL/2022/Conference/Ethics_Chairs"
                "{tail}"
            ]
        },
        "nonreaders": {
            "values": [
                "aclweb.org/ACL/2022/Conference/Paper{head.number}/Authors"
            ]
        },
        "writers": {
            "values": [
                "aclweb.org/ACL/2022/Conference"
                "aclweb.org/ACL/2022/Conference/Ethics_Chairs"
            ]
        },
        "signatures": {
            "values-regex": "aclweb.org/ACL/2022/Conference/Ethics_Chairs|aclweb.org/ACL/2022/Conference/Program_Chairs",
            "default": "aclweb.org/ACL/2022/Conference/Program_Chairs"
        },
        "content": {
            "head": {
                "type": "Note",
                "query": {
                    "invitation": "aclweb.org/ACL/2022/Conference/-/Blind_Submission"
                }
            },
            "tail": {
                "type": "Profile",
                "query": {
                    "value-regex": "~.*|.+@.+"
                },
            },
            "weight": {
                "value-regex": "[-+]?[0-9]*\\.?[0-9]*"
            },
            "label": {
                "value-regex": ".*"
            }
        }
    },
    preprocess='./ethics_reviewer_assignment_preprocess.py',
    process='./ethics_reviewer_assignment_process.py'
)
client.post_invitation(assignment_invitation)
