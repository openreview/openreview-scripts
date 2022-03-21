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

acl_blind_submission_invitation = client.get_invitation("aclweb.org/ACL/2022/Conference/-/Blind_Submission")
acl_blind_submission_invitation.reply['content']["copyright_consent_name_and_address"] = {
    "value-regex": ".*",
      "required": False
    }
acl_blind_submission_invitation.reply['content']["copyright_consent_signature_(type_name_or_NA_if_not_transferrable)"] = {
    "value-regex": ".*",
      "required": False
    }
acl_blind_submission_invitation.reply['content']["copyright_consent"] = {
    "value-regex": ".*",
      "required": False
    }
acl_blind_submission_invitation.reply['content']["copyright_consent_job_title"] = {
    "value-regex": ".*",
      "required": False
    }

client.post_invitation(acl_blind_submission_invitation)
acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation="aclweb.org/ACL/2022/Conference/-/Blind_Submission"))
for acl_blind_submission in tqdm(acl_blind_submissions):
    acl_blind_submission.content = {
                        "authorids" : [f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors"],
                        "authors":["Anonymous"],
                        "copyright_consent_signature_(type_name_or_NA_if_not_transferrable)": "", 
                        "copyright_consent_name_and_address": "",
                        "copyright_consent": "",
                        "copyright_consent_job_title": ""
                    }
    client.post_note(acl_blind_submission)