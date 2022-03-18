import argparse
from importlib.util import decode_source
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


invitations_by_forum = {}
original_acl_invitation = client.get_invitation('aclweb.org/NAACL/2022/Conference/-/Submission')
original_acl_invitation.reply['readers'] = {"values-regex": ".*"
  }
client.post_invitation(original_acl_invitation)


acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission'))

# For each submission, add the authors of the original ARR submission to the readers of the blind submission 
for acl_blind_submission in tqdm(acl_blind_submissions): 
    author_group = f'aclweb.org/NAACL/2022/Conference/Commitment{acl_blind_submission.number}/Authors'
    
    # Add authors as readers of blind submission
    if author_group not in acl_blind_submission.readers:
        print(acl_blind_submission.forum)
        acl_blind_submission.readers.append(author_group)
        acl_blind_submission.content = {
                    "authorids" : [author_group],
                    "authors":["Anonymous"]
                }
        client.post_note(acl_blind_submission)
   
   # Add authors as readers of original submission
    original_submission = client.get_note(acl_blind_submission.original)
    if author_group not in original_submission.readers:
        original_submission.readers.append(author_group)
        client.post_note(original_submission)
    
    # Make authors signatories and readers of the author group 
    group = client.get_group(author_group)
    group.signatories = ['aclweb.org/NAACL/2022/Conference', author_group]
    group.readers = ['aclweb.org/NAACL/2022/Conference', author_group]
    client.post_group(group)

    
        