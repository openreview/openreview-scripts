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

for acl_ethics_review_invitation in acl_ethics_review_invitations: 
    invitations_by_forum[acl_ethics_review_invitation.reply['forum']] = acl_ethics_review_invitation


acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))

# For each submission, add the authors of the original ARR submission to the readers of the blind submission 
for acl_blind_submission in tqdm(acl_blind_submissions): 
    # Need to add authors to ethics review invitation as readers 
    invitation = invitations_by_forum[acl_blind_submission.forum]
    if author_group not in invitation.reply['readers']:
        invitation.reply['readers'].append(author_group)
        client.post_invitation(invitation)

    author_group = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors'
    if author_group not in acl_blind_submission.readers:
        acl_blind_submission.readers.append(author_group)
        acl_blind_submission.content = {
                    "authorids" : [f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors"],
                    "authors":["Anonymous"]
                }
        client.post_note(acl_blind_submission)
    
    ethics_review = client.get_notes(forum = acl_blind_submission.forum, invitation = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/-/Ethics_Review')
    if author_group not in ethics_review.readers:
        ethics_review.readers.append(author_group)
        client.post_note(ethics_review)
  
    
        