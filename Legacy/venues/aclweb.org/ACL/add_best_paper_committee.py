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
flagged_papers = flagged_papers.flagged_papers
best_paper_committee = client.post_group(openreview.Group(
    id = 'aclweb.org/ACL/2022/Conference/Best_Paper_Committee',
    signatures = [
        'aclweb.org/ACL/2022/Conference'
        ],
    signatories=[
        'aclweb.org/ACL/2022/Conference',
        'aclweb.org/ACL/2022/Conference/Best_Paper_Committee'
        ],
    readers = [
        'aclweb.org/ACL/2022/Conference',
        'aclweb.org/ACL/2022/Conference/Best_Paper_Committee'
    ],
    writers = [
            'aclweb.org/ACL/2022/Conference'
            ],
    members = [
        
    ]
))
submissions_by_number = {s.number: s for s in list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))}
acl_meta_reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Meta_Review'))
acl_reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Official_Review'))
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

for paper_number in flagged_papers: 
    submission = submissions_by_number[paper_number]
    if best_paper_committee.id not in submission.readers: 
        submission.readers.append(best_paper_committee.id)
        submission.content = {
            'authors': ['Anonymous'],
            'authorids': [f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Authors'],
            "copyright_consent": "",
            "copyright_consent_signature_(type_name_or_NA_if_not_transferrable)": "",
            "copyright_consent_job_title": "",
            "copyright_consent_name_and_address": ""
        }
        client.post_note(submission)
    reviews = reviews_by_forum[submission.forum]
    for review in reviews: 
        if best_paper_committee.id not in review.readers: 
            review.readers.append(best_paper_committee.id)
            client.post_note(review)
