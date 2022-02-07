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



# For submission in submissions, add paperx/Reviewers group and AC group as readers 
# Currently assumes submissions_list is a list of Notes 

submissions_forum_list = flagged_papers.flagged_papers

# For Each submission, create reviewer group, add reviewer group and AC group to readers 
for submission_forum in tqdm(submissions_forum_list): 
    submission = client.get_note(submission_forum)
    paper_track = sac_name_dictionary[submission.content["track"]]
    track_sac_id = f'aclweb.org/ACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    conflict_id = f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Conflicts'
    # Create Ethics Reviewer group 
    ethics_reviewers_paper = client.post_group(openreview.Group(
        id = f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Ethics_Reviewers',
        signatures = [
            'aclweb.org/ACL/2022/Conference'
            ],
        signatories=[
            'aclweb.org/ACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/ACL/2022/Conference',
            'aclweb.org/ACL/2022/Conference/Ethics_Chairs',
            f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Ethics_Reviewers'
            ],
        writers = [
            'aclweb.org/ACL/2022/Conference'
             ],
        nonreaders= submission.nonreaders,
        anonids=True
        ))
    
    submission.readers = [
        "aclweb.org/ACL/2022/Conference",
        "aclweb.org/ACL/2022/Conference/Program_Chairs",
        track_sac_id,
        'aclweb.org/ACL/2022/Conference/Ethics_Chairs',
        ethics_reviewers_paper.id
    ]
    submission.nonreaders = [
        conflict_id
    ]
    submission.content = {
        'authors': ['Anonymous'],
        'authorids': [f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Authors']
    }
    client.post_note(submission)
    metareviews = openreview.tools.iterget_notes(client, invitation = "aclweb.org/ACL/2022/Conference/-/Meta_Review", forum = submission.forum)
    for review in metareviews: 
        review.readers = [
            "aclweb.org/ACL/2022/Conference/Program_Chairs",
            track_sac_id,
            'aclweb.org/ACL/2022/Conference/Ethics_Chairs',
            ethics_reviewers_paper.id
        ]
        review.nonreaders = [
            conflict_id
        ]
        client.post_note(review)
    reviews = openreview.tools.iterget_notes(client, invitation = "aclweb.org/ACL/2022/Conference/-/Official_Review", forum = submission.forum)
    for review in reviews: 
        review.readers = [
            "aclweb.org/ACL/2022/Conference/Program_Chairs",
            track_sac_id,
            'aclweb.org/ACL/2022/Conference/Ethics_Chairs',
            ethics_reviewers_paper.id
        ]
        review.nonreaders = [
            conflict_id
        ]
        client.post_note(review)