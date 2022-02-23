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

# Get all Ethics Review invitations 
acl_ethics_review_invitations = list(openreview.tools.iterget_invitations(client, regex= 'aclweb.org/ACL/2022/Conference/Paper.*/-/Ethics_Review'))

invitations_by_forum = {}
original_acl_invitation = client.get_invitation('aclweb.org/ACL/2022/Conference/-/Submission')
original_acl_invitation.reply['readers'] = {"values-regex": ".*"
  }
client.post_invitation(original_acl_invitation)
for acl_ethics_review_invitation in acl_ethics_review_invitations: 
    invitations_by_forum[acl_ethics_review_invitation.reply['forum']] = acl_ethics_review_invitation


acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))

# For each submission, add the authors of the original ARR submission to the readers of the blind submission 
for acl_blind_submission in tqdm(acl_blind_submissions): 
    author_group = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors'
    # Need to add authors to ethics review invitation as readers
    if(acl_blind_submission.forum in invitations_by_forum):
        invitation = invitations_by_forum[acl_blind_submission.forum]
        if author_group not in invitation.reply['readers']['values-copied']:
            invitation.reply['readers'] = {
                "values-copied": [
                "aclweb.org/ACL/2022/Conference/Program_Chairs",
                "aclweb.org/ACL/2022/Conference/Ethics_Chairs",
                f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Ethics_Reviewers",
                author_group
                ]
            }
        client.post_invitation(invitation)
    
    if author_group not in acl_blind_submission.readers:
        acl_blind_submission.readers.append(author_group)
        acl_blind_submission.content = {
                    "authorids" : [f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors"],
                    "authors":["Anonymous"]
                }
        client.post_note(acl_blind_submission)
    
    ethics_review = client.get_notes(forum = acl_blind_submission.forum, invitation = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Ethics_Review')
    if ethics_review:
        if author_group not in ethics_review[0].readers:
            ethics_review[0].readers.append(author_group)
            client.post_note(ethics_review[0])
    
    original_submission = client.get_note(acl_blind_submission.original)
    if author_group not in original_submission.readers:
        original_submission.readers.append(author_group)
        client.post_note(original_submission)
    
    group = client.get_group(author_group)
    group.signatories = ['aclweb.org/ACL/2022/Conference', author_group]
    group.readers = ['aclweb.org/ACL/2022/Conference', author_group]
    client.post_group(group)
  
    
        