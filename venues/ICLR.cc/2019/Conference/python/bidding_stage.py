'''
Bidding Stage (Oct 2 - Oct 5)

- Bidding Task / interface enabled and added to the Reviewer Console
- Reviewers bid on papers.
- Area chairs bid on papers.

'''

import openreview
import iclr19
import notes
import groups
import invitations
import argparse
import random
import csv

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('scores_file')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    # read in TPMS scores
    paper_scores_by_number = {}
    with open(args.scores_file) as f:
        for row in csv.reader(f):
            paper_number = int(row[0])
            profile_id = row[1]
            score = row[2]
            if paper_number not in paper_scores_by_number:
                paper_scores_by_number[paper_number] = {}
            paper_scores_by_number[paper_number][profile_id] = score

    with open('../webfield/reviewerWebfieldBiddingEnabled.js','r') as f:
        reviewers = client.get_group(iclr19.REVIEWERS_ID)
        reviewers.web = f.read()
        reviewers = client.post_group(reviewers)

    with open('../webfield/areachairWebfieldBiddingEnabled.js','r') as f:
        area_chairs = client.get_group(iclr19.AREA_CHAIRS_ID)
        area_chairs.web = f.read()
        area_chairs = client.post_group(area_chairs)

    iclr19.add_bid.invitees = [iclr19.REVIEWERS_ID, iclr19.AREA_CHAIRS_ID]
    client.post_invitation(iclr19.add_bid)

    # set up User Score notes

    if not all(['~' in member for member in reviewers.members]):
        print('WARNING: not all reviewers have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_reviewer_ids = [r for r in reviewers.members if '~' in r]

    if not all(['~' in member for member in area_chairs.members]):
        print('WARNING: not all area chairs have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_ac_ids = [r for r in area_chairs.members if '~' in r]

    client.post_invitation(iclr19.scores_inv)
    user_score_notes = {}
    for paper in openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID):
        for user_id in valid_reviewer_ids + valid_ac_ids:
            if user_id not in user_score_notes:
                user_score_notes[user_id] = openreview.Note.from_json({
                    'invitation': iclr19.SCORES_INV_ID,
                    'readers': [user_id],
                    'writers': ['ICLR.cc/2019/Conference'],
                    'content': {
                        'user': user_id,
                        'scores': []
                    },
                    'signatures': ['ICLR.cc/2019/Conference'],
                    'forum': None,
                    'multiReply': False
                })
            score_note = user_score_notes[user_id]

            score_entry = {
                'forum': paper.forum,
                'tpmsScore': float(paper_scores_by_number[paper.number].get(user_id,0.0)),
                # 'conflict': 'cs.umass.edu'
            }

            score_note.content['scores'].append(score_entry)

    for user_id, score_note in user_score_notes.items():
        print('posting score note for user {}'.format(user_id))
        client.post_note(score_note)





