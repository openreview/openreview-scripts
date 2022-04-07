import argparse
from re import sub
import openreview
from tqdm import tqdm
import csv
import tracks
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
sac_name_dictionary = tracks.sac_name_dictionary
'''
# Create Ethics AC group 
ethics = client.post_group(openreview.Group(
    id = 'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
    signatures = [
        'aclweb.org/NAACL/2022/Conference'
        ],
    signatories=[
        'aclweb.org/NAACL/2022/Conference',
        'aclweb.org/NAACL/2022/Conference/Ethics_Chairs'
        ],
    readers = [
        'aclweb.org/NAACL/2022/Conference',
        'aclweb.org/NAACL/2022/Conference/Ethics_Chairs'
    ],
    writers = [
            'aclweb.org/NAACL/2022/Conference'
            ],
    members = [

    ]
))
# Create Ethics Reviewers Group 
ethics_reviewers = client.post_group(openreview.Group(
        id = f'aclweb.org/NAACL/2022/Conference/Ethics_Reviewers',
        signatures = [
            'aclweb.org/NAACL/2022/Conference'
            ],
        signatories=[
            'aclweb.org/NAACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
            'aclweb.org/NAACL/2022/Conference/Ethics_Reviewers',
            'aclweb.org/NAACL/2022/Conference'
            ],
        writers = [
            'aclweb.org/NAACL/2022/Conference'
             ]
        ))
'''

# For submission in submissions, add paperx/Reviewers group and AC group as readers
# Currently assumes submissions_list is a list of Notes

submissions_forum_list = flagged_papers.flagged_papers

blind_submission_by_number = { s.number: s for s in openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/-/Blind_Submission')}
submission_by_number = { s.number: s for s in openreview.tools.iterget_notes(client, invitation='aclweb.org/NAACL/2022/Conference/-/Submission')}


# For Each submission, create reviewer group, add reviewer group and AC group to readers
for submission_number in tqdm(submissions_forum_list):
    submission = blind_submission_by_number[submission_number]
    original_submission = submission_by_number[submission_number]
    paper_track = sac_name_dictionary[original_submission.content["track"]]
    track_sac_id = f'aclweb.org/NAACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    conflict_id = f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Conflicts'
    # Create Ethics Reviewer group - using 'commitment' in case they want me to do the same thing for special theme 
    ethics_reviewers_paper = client.post_group(openreview.Group(
        id = f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Ethics_Reviewers',
        signatures = [
            'aclweb.org/NAACL/2022/Conference'
            ],
        signatories=[
            'aclweb.org/NAACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/NAACL/2022/Conference',
            'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
            f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Ethics_Reviewers'
            ],
        writers = [
            'aclweb.org/NAACL/2022/Conference'
             ],
        nonreaders= submission.nonreaders,
        anonids=True
        ))
    if len(submission.readers) >1:
        submission.readers = [
            "aclweb.org/NAACL/2022/Conference",
            "aclweb.org/NAACL/2022/Conference/Program_Chairs",
            track_sac_id,
            'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
            ethics_reviewers_paper.id
        ]
        submission.nonreaders = [
            conflict_id
        ]
        submission.content = {
            'authors': ['Anonymous'],
            'authorids': [f'aclweb.org/NAACL/2022/Conference/Commitment{submission.number}/Authors']
        }
        client.post_note(submission)
    metareviews = openreview.tools.iterget_notes(client, invitation = "aclweb.org/NAACL/2022/Conference/-/ARR_Meta_Review", forum = submission.forum)
    for review in metareviews:
        review.readers = [
            "aclweb.org/NAACL/2022/Conference/Program_Chairs",
            track_sac_id,
            'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
            ethics_reviewers_paper.id
        ]
        review.nonreaders = [
            conflict_id
        ]
        client.post_note(review)
    reviews = openreview.tools.iterget_notes(client, invitation = "aclweb.org/NAACL/2022/Conference/-/ARR_Official_Review", forum = submission.forum)
    for review in reviews:
        review.readers = [
            "aclweb.org/NAACL/2022/Conference/Program_Chairs",
            track_sac_id,
            'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
            ethics_reviewers_paper.id
        ]
        review.nonreaders = [
            conflict_id
        ]
        client.post_note(review)
    try:
        comment = (client.get_notes(invitation=f"aclweb.org/NAACL/2022/Conference/Commitment{submission_number}/-/Comment_by_Authors"))[0]
        comment_invitation = client.get_invitation(f"aclweb.org/NAACL/2022/Conference/Commitment{submission_number}/-/Comment_by_Authors")
        
        comment_invitation.reply['readers']['values'] = ["aclweb.org/NAACL/2022/Conference/Program_Chairs",
            track_sac_id,
            'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
            ethics_reviewers_paper.id
            ]
        client.post_invitation(comment_invitation)
        comment.readers = [ 
            "aclweb.org/NAACL/2022/Conference/Program_Chairs",
            track_sac_id,
            'aclweb.org/NAACL/2022/Conference/Ethics_Chairs',
            ethics_reviewers_paper.id
        ]
        client.post_note(comment)
    except: 
        print(f'no comment by authors found for {submission.number} forum {submission.forum}')
    