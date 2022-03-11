import argparse
from re import sub
from sys import set_asyncgen_hooks
import openreview
from tqdm import tqdm
import csv
import tracks
import countries

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
blind_submission_invitation = client.get_invitation('aclweb.org/NAACL/2022/Conference/-/Blind_Submission')
submission_invitation = client.get_invitation('aclweb.org/NAACL/2022/Conference/-/Submission')
blind_submission_content = {}
for key in submission_invitation.reply['content'].keys(): 
    blind_submission_content[key] = {
                "value-regex": ".*" 
                }
blind_submission_content['authors'] = {
                "values-regex": ".*" 
                }
blind_submission_content['authorids'] = { 
                "values-regex": ".*" 
                }
blind_submission_invitation.reply['content'] = blind_submission_content
client.post_invitation(blind_submission_invitation)

blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission'))

for blind_submission in tqdm(blind_submissions):
    original = client.get_note(blind_submission.original)
    if original.content['naacl_preprint'] == 'yes':
        content = {}
        keep_keys = ['title', 'pdf', 'abstract','paper_link','country_of_affiliation_of_corresponding_author', 'track','paper_type']
        for key in blind_submission.content: 
            if key not in keep_keys:
                content[key] = ''
        
        content['authorids'] = [f"aclweb.org/NAACL/2022/Conference/Commitment{blind_submission.number}/Authors"]
        content['authors'] = ["Anonymous"]
        blind_submission.content = content
        blind_submission.readers = ['everyone']
        client.post_note(blind_submission)
        