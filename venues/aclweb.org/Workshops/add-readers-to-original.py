import argparse
from calendar import c
from re import sub
import openreview
from tqdm import tqdm
import csv


"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password
    confid - the user's conference 

"""
# For workshops using their original venue -- PCs only posting decisions and Camera Ready Revision Invitations to Papers 
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--confid')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

confid = args.confid
#committee = [f'{confid}/Program_Chairs']
#if openreview.tools.get_group(client, f'{confid}/Area_Chairs'):
 #   committee.append(f'{confid}/Area_Chairs')
# Retrieve all commitment submissions 
commitment_notes = list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/Commitment_Submission'))
for commitment_note in commitment_notes: 
    paper_group = openreview.Group(
        id = f'{confid}/Commitment{commitment_note.number}',
        signatures = [
            confid
            ],
        signatories = [
            confid
            ],
        readers = [
            confid
            ],
        writers = [
            confid
            ]
    )
    client.post_group(paper_group)

    # Create paperX/Authors
    authors = openreview.Group(
        id = f'{confid}/Commitment{commitment_note.number}/Authors',
        signatures = [
            confid
            ],
        signatories = [
            confid,
            f'{confid}/Commitment{commitment_note.number}/Authors'
            ],
        readers = [
            confid,
            f'{confid}/Commitment{commitment_note.number}/Authors'
            ],
        writers = [
            confid
            ],
        members = commitment_note.content['authorids']
    )

    authors_posted = client.post_group(authors)
    assert authors_posted, print('Failed to post author groups: ', commitment_note.id)
    
    arr_submission_forum = (commitment_note.content['paper_link'].split('=')[1]).split('&')[0]
    try:
        original_arr_sub = client.get_note(arr_submission_forum)
        if(original_arr_sub.original):
            original_arr_sub_id = original_arr_sub.original
        else:
            original_arr_sub_id = original_arr_sub.id
    except:
        print(f"Note {arr_submission_forum} does not exist")

    if original_arr_sub: 
        arr_conf_id = original_arr_sub.invitation.rsplit('/', 2)[0]
        original_arr_sub.invitation.split('/')
        arr_reviewers = client.get_group(f'{arr_conf_id}/Paper{original_arr_sub.number}/Reviewers')
        client.add_members_to_group(arr_reviewers, f'{confid}/Program_Chairs')

