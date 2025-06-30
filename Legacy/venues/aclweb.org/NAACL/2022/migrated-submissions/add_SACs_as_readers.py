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

program_chairs_id = 'aclweb.org/NAACL/2022/Conference/Program_Chairs'

# Creating SAC groups from Track Name
sac_name_dictionary = tracks.sac_name_dictionary

acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/Blind_Submission'))
acl_meta_reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/ARR_Meta_Review'))
acl_reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/NAACL/2022/Conference/-/ARR_Official_Review'))
reviews_by_forum = {}
for metareview in acl_meta_reviews:
    if metareview.forum in reviews_by_forum:
        reviews_by_forum[metareview.forum].append(metareview)
    else:
        reviews_by_forum[metareview.forum] = [metareview]
for review in acl_reviews:
    if review.forum in reviews_by_forum:
        reviews_by_forum[review.forum].append(review)
    else:
        reviews_by_forum[review.forum] = [review]

# For each blind submission, set the readers to the SAC track group
for acl_blind_submission in tqdm(acl_blind_submissions):
    paper_track = sac_name_dictionary[acl_blind_submission.content["track"]]
    track_sac_id = f'aclweb.org/NAACL/2022/Conference/{paper_track}/Senior_Area_Chairs'
    conflict_id = f'aclweb.org/NAACL/2022/Conference/Commitment{acl_blind_submission.number}/Conflicts'

    acl_blind_submission.readers = [
        'aclweb.org/NAACL/2022/Conference',
        program_chairs_id,
        track_sac_id
    ]
    acl_blind_submission.nonreaders = [
        conflict_id
    ]
    acl_blind_submission.content = {
        'authors': ['Anonymous'],
        'authorids': [f'aclweb.org/NAACL/2022/Conference/Commitment{acl_blind_submission.number}/Authors']
    }
    client.post_note(acl_blind_submission)
    reviews = reviews_by_forum[acl_blind_submission.forum]
    for review in reviews:
        review.readers = [
            program_chairs_id,
            track_sac_id
        ]
        review.nonreaders = [
            conflict_id
        ]
        client.post_note(review)
