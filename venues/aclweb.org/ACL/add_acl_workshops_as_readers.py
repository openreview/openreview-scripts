import openreview
from tqdm import tqdm
import argparse
"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password
    confid - the venue id of the workshop being added as readers 

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--confid')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

confid = args.confid
workshop_submissions = list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/Blind_Submission'))
##TODO: add validation that authors are in fact authors of the arr submission, otherwise they should not be granted readership 
for workshop_submission in workshop_submissions:
    if workshop_submission.content.get('paper_link'):
        arr_forum = workshop_submission.content['paper_link'].split('=')[1].split('&')[0]
        arr_submission = client.get_note(arr_forum)
        arr_submission_reviewers_id = f'{confid}/Paper{arr_submission.number}/Reviewers'
        client.add_members_to_group(arr_submission_reviewers_id,workshop_submission.readers)
