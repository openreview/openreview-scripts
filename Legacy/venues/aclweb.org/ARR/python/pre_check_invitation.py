import argparse
from operator import sub
from os import confstr_names
import openreview
from tqdm import tqdm
import csv
from openreview import tools
import re
from collections import defaultdict

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

pre_check_inv = client.post_invitation(openreview.Invitation(
    id = 'aclweb.org/ACL/ARR/2022/January/Reviewers/-/Pre-Check',
    readers = [
        "aclweb.org/ACL/ARR/2022/January",
        "aclweb.org/ACL/ARR/2022/January/Senior_Area_Chairs",
        "aclweb.org/ACL/ARR/2022/January/Area_Chairs"
    ],
    writers = ['aclweb.org/ACL/ARR/2022/January'],
    signatures=['aclweb.org/ACL/ARR/2022/January'],
    invitees = [
        "aclweb.org/ACL/ARR/2022/January",
        "OpenReview.net/Support",
        "aclweb.org/ACL/ARR/2022/January/Senior_Area_Chairs",
        "aclweb.org/ACL/ARR/2022/January/Area_Chairs"
    ],
    reply = {
        "readers": {
            "values-copied": [
            "aclweb.org/ACL/ARR/2022/January",
            "aclweb.org/ACL/ARR/2022/January/Paper{head.number}/Senior_Area_Chairs",
            "aclweb.org/ACL/ARR/2022/January/Paper{head.number}/Area_Chairs",
            "{tail}"
            ]
        },
        "nonreaders": {
            "values": [
            "aclweb.org/ACL/ARR/2022/January/Paper{head.number}/Authors"
            ]
        },
        "writers": {
            "values": [
            "aclweb.org/ACL/ARR/2022/January",
            "aclweb.org/ACL/ARR/2022/January/Paper{head.number}/Senior_Area_Chairs",
            "aclweb.org/ACL/ARR/2022/January/Paper{head.number}/Area_Chairs"
            ]
        },
        "signatures": {
            "values-regex": "aclweb.org/ACL/ARR/2022/January$|aclweb.org/ACL/ARR/2022/January/Program_Chairs|aclweb.org/ACL/ARR/2022/January/Paper{head.number}/Senior_Area_Chairs|aclweb.org/ACL/ARR/2022/January/Paper{head.number}/Area_Chair_.*",
            "default": "aclweb.org/ACL/ARR/2022/January/Program_Chairs"
        },
        'content':{
            "head": {
                "type": "Note",
                "query": {
                    "invitation": "aclweb.org/ACL/ARR/2022/January/-/Blind_Submission"
                }
            },
            "tail": {
                "type": "Profile",
                "query": {
                    "group": "aclweb.org/ACL/ARR/2022/January/Reviewers"
                }
            },
            "weight": {
                "value-regex": "[-+]?[0-9]*\\.?[0-9]*"
            },
            "label": {
                "value-regex": ".*"
                }
            }
        },
    multiReply = False
))
