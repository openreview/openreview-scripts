'''
Bidding Stage (Oct 2 - Oct 5)

- Bidding Task / interface enabled and added to the Reviewer Console
- Reviewers bid on papers.
- Area chairs bid on papers.

'''

import openreview
import akbc19 as conference_config
import notes
import groups
import invitations
import argparse
import random
import csv

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('tfidf_score_file')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    # read in tfidf scores

    def read_scores(scores_file):
        scores_by_number = {}
        with open(args.tfidf_score_file) as f:
            for row in csv.reader(f):
                paper_number = int(row[0])
                profile_id = row[1]
                score = row[2]
                if paper_number not in scores_by_number:
                    scores_by_number[paper_number] = {}
                scores_by_number[paper_number][profile_id] = score

        return scores_by_number

    tfidf_scores_by_number = read_scores(args.tfidf_score_file)

    with open('../webfield/reviewerWebfieldBiddingEnabled.js','r') as f:
        reviewers = client.get_group(conference_config.REVIEWERS_ID)
        reviewers.web = f.read()
        reviewers = client.post_group(reviewers)

    with open('../webfield/areachairWebfieldBiddingEnabled.js','r') as f:
        area_chairs = client.get_group(conference_config.AREA_CHAIRS_ID)
        area_chairs.web = f.read()
        area_chairs = client.post_group(area_chairs)

    conference_config.add_bid.invitees = [conference_config.REVIEWERS_ID, conference_config.AREA_CHAIRS_ID]
    client.post_invitation(conference_config.add_bid)

    # set up User Score notes

    if not all(['~' in member for member in reviewers.members]):
        print('WARNING: not all reviewers have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_reviewer_ids = [r for r in reviewers.members if '~' in r]

    if not all(['~' in member for member in area_chairs.members]):
        print('WARNING: not all area chairs have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_ac_ids = [r for r in area_chairs.members if '~' in r]

    client.post_invitation(conference_config.scores_inv)
    user_score_notes = {}
    for paper in openreview.tools.iterget_notes(client, invitation=conference_config.BLIND_SUBMISSION_ID):
        for user_id in valid_reviewer_ids + valid_ac_ids:
            if user_id not in user_score_notes:
                user_score_notes[user_id] = openreview.Note.from_json({
                    'invitation': conference_config.SCORES_INV_ID,
                    'readers': [user_id],
                    'writers': [conference_config.CONFERENCE_ID],
                    'content': {
                        'user': user_id,
                        'scores': []
                    },
                    'signatures': [conference_config.CONFERENCE_ID],
                    'forum': None,
                    'multiReply': False
                })
            score_note = user_score_notes[user_id]

            score_entry = {
                'forum': paper.forum,
                'tfidfScore': float(tfidf_scores_by_number[paper.number].get(user_id,0.0)),
                # 'conflict': 'cs.umass.edu'
            }

            score_note.content['scores'].append(score_entry)

    for user_id, score_note in user_score_notes.items():
        print('posting score note for user {}'.format(user_id))
        client.post_note(score_note)
