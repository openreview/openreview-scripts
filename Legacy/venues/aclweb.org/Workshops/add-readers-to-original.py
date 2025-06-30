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
# Need to first replace members by ID for PC group 
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
PC_group = [PC.id for PC in openreview.tools.get_profiles(client, client.get_group(f'{confid}/Program_Chairs').members)]
commitment_notes = list(openreview.tools.iterget_notes(client, invitation = f'{confid}/-/Commitment_Submission'))
original_arr_subs = {}
author_groups = {}
print("loading commitment data")
for commitment_note in tqdm(commitment_notes): 
    arr_submission_forum = ((commitment_note.content['paper_link'].split('=')[1]).split('&')[0]).strip()
    #try:
    original_arr_sub = client.get_note(arr_submission_forum)
    arr_conf_id = original_arr_sub.invitation.rsplit('/', 2)[0]
    if(original_arr_sub.original):
        original_arr_sub_id = original_arr_sub.original
    else:
        original_arr_sub_id = original_arr_sub.id
    original_arr_sub = client.get_note(original_arr_sub_id)
    original_arr_subs[commitment_note.forum] = original_arr_sub
    author_group = client.get_group(f'{arr_conf_id}/Paper{original_arr_sub.number}/Authors')
    author_groups[original_arr_sub.id] = [author.id for author in openreview.tools.get_profiles(client, author_group.members)]
    #except:
    #    print(f"Note {arr_submission_forum} does not exist")
print("adding PCs as readers")    
for commitment_note in tqdm(commitment_notes): 
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
    
    original_arr_sub = original_arr_subs.get(commitment_note.forum)
    if original_arr_sub: 
        arr_conf_id = original_arr_sub.invitation.rsplit('/', 2)[0]
        arr_reviewers = client.get_group(f'{arr_conf_id}/Paper{original_arr_sub.number}/Reviewers')
        #arr_reviewers_submitted = client.get_group(f'{arr_conf_id}/Paper{original_arr_sub.number}/Reviewers_Submitted')
        print(arr_reviewers.id)
        group_with_PCs = client.add_members_to_group(arr_reviewers, f'{confid}/Program_Chairs')
        # Check if PC is author of submission, and if so, add them as nonreaders of group 
        for PC in PC_group: 
            if PC in author_groups[original_arr_sub.id]: # Author groups dictionary of original arr sub: author group.members 
                group_with_PCs.nonreaders.append(PC)
        client.post_group(group_with_PCs)
        if client.get_group(f'{arr_conf_id}/Paper{original_arr_sub.number}/Reviewers/Submitted'):
            group_with_PCs = client.add_members_to_group(f'{arr_conf_id}/Paper{original_arr_sub.number}/Reviewers/Submitted', f'{confid}/Program_Chairs')
            # Check if PC is author of submission, and if so, add them as nonreaders of group 
            for PC in PC_group: 
                if PC in author_groups[original_arr_sub.id]: # Author groups dictionary of original arr sub: author group.members 
                    group_with_PCs.nonreaders.append(PC)
            client.post_group(group_with_PCs)
        

