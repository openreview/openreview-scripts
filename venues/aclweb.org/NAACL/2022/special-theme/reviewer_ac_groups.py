import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
import flagged_papers

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
# Create Ethics AC group 
ethics_chairs = client.post_group(openreview.Group(
    id = 'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Chairs',
    signatures = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    signatories=[
        'aclweb.org/NAACL/2022/Conference',
        'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Chairs'
        ],
    readers = [
        'aclweb.org/NAACL/2022/Conference',
        'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Chairs'
    ],
    writers = [
            'aclweb.org/NAACL/2022/Conference'
            ],
    members = [

    ]
))
# Create Ethics Reviewers Group 
ethics_reviewers = client.post_group(openreview.Group(
        id = f'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Reviewers',
        signatures = [
            'aclweb.org/NAACL/2022/Conference'
            ],
        signatories=[
            'aclweb.org/NAACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Chairs',
            'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Reviewers',
            'aclweb.org/NAACL/2022/Conference'
            ],
        writers = [
            'aclweb.org/NAACL/2022/Conference'
             ]
        ))


# For submission in submissions, add paperx/Reviewers group and AC group as readers
# Currently assumes submissions_list is a list of Notes

submissions_forum_list = flagged_papers.flagged_papers

blind_submission_by_number = { s.number: s for s in openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/-/Blind_Special_Theme_Submission')}
submission_by_number = { s.number: s for s in openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/-/Special_Theme_Submission')}


# For Each submission, create reviewer group, add reviewer group and AC group to readers
for submission_number in tqdm(submissions_forum_list):
    submission = blind_submission_by_number[submission_number]
    original_submission = submission_by_number[submission_number]
    confid = "aclweb.org/NAACL/2022/Conference"
    # Create Ethics Reviewer group - using 'commitment' in case they want me to do the same thing for special theme 
    ethics_reviewers_paper = client.post_group(openreview.Group(
        id = f'aclweb.org/NAACL/2022/Conference/Paper{submission.number}/Special_Theme_Ethics_Reviewers',
        signatures = [
            'aclweb.org/NAACL/2022/Conference'
            ],
        signatories=[
            'aclweb.org/NAACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/NAACL/2022/Conference',
            'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Chairs',
            f'aclweb.org/NAACL/2022/Conference/Paper{submission.number}/Special_Theme_Ethics_Reviewers'
            ],
        writers = [
            'aclweb.org/NAACL/2022/Conference'
             ],
        nonreaders= submission.nonreaders,
        anonids=True
        ))
    readers_changed = False
    if ethics_reviewers_paper.id not in submission.readers:
        submission.readers.append(ethics_reviewers_paper.id)
        submission.content = {
        'authors': ['Anonymous'],
        'authorids': [f'aclweb.org/NAACL/2022/Conference/Paper{submission.number}/Authors']
        }
        readers_changed = True
    if ethics_chairs.id not in submission.readers:
        submission.readers.append(ethics_chairs.id)
        submission.content = {
        'authors': ['Anonymous'],
        'authorids': [f'aclweb.org/NAACL/2022/Conference/Paper{submission.number}/Authors']
        }
        readers_changed = True
    if readers_changed:
        client.post_note(submission)
    
    metareviews = openreview.tools.iterget_notes(client, invitation = f"aclweb.org/NAACL/2022/Conference/Paper{submission.number}/-/Meta_Review", forum = submission.forum)
    metareview_invitation = client.get_invitation(f"aclweb.org/NAACL/2022/Conference/Paper{submission.number}/-/Meta_Review")
    metareview_invitation.reply['readers'] = {"values-regex": ".*"}
    client.post_invitation(metareview_invitation)
    review_invitation = client.get_invitation(f"aclweb.org/NAACL/2022/Conference/Paper{submission.number}/-/Official_Review")
    review_invitation.reply['readers'] = {"values-regex": ".*"}
    client.post_invitation(review_invitation)
    for review in metareviews:
        meta_readers_changed = False
        if ethics_reviewers_paper.id not in review.readers:
            review.readers.append(ethics_reviewers_paper.id)
        if ethics_chairs.id not in review.readers:
            review.readers.append(ethics_chairs.id)
        if meta_readers_changed: 
            client.post_note(review)
    reviews = openreview.tools.iterget_notes(client, invitation = f"aclweb.org/NAACL/2022/Conference/Paper{submission.number}/-/Official_Review", forum = submission.forum)
    for review in reviews:
        review_readers_changed = False
        if ethics_reviewers_paper.id not in review.readers:
            review.readers.append(ethics_reviewers_paper.id)
            review_readers_changed = True
        if ethics_chairs.id not in review.readers:
            review.readers.append(ethics_chairs.id)
            review_readers_changed = True
        if review_readers_changed: 
            client.post_note(review)