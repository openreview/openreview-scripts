'''
Bidding Stage (Oct 2 - Oct 5)

- Bidding Task / interface enabled and added to the Reviewer Console
- Reviewers bid on papers.
- Area chairs bid on papers.

'''

import openreview
from openreview import invitations
import config
import argparse
import random
import csv
import os

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('tfidf_score_file')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = config.get_conference(client)
    # read in tfidf scores

    def read_scores(scores_file):
        scores_by_id = {}
        with open(args.tfidf_score_file) as f:
            for row in csv.reader(f):
                paper_id = row[0]
                profile_id = row[1]
                score = row[2]
                if paper_id not in scores_by_id:
                    scores_by_id[paper_id] = {}
                scores_by_id[paper_id][profile_id] = score

        return scores_by_id

    tfidf_score_by_id = read_scores(args.tfidf_score_file)
    print(tfidf_score_by_id)

    with open('../webfield/reviewerWebfieldBiddingEnabled.js','r') as f:
        reviewers = client.get_group(conference.get_reviewers_id())
        reviewers.web = f.read()
        reviewers = client.post_group(reviewers)

    area_chairs = client.get_group(conference.get_area_chairs_id())

    bid_invitation = openreview.invitations.AddBid(
        conference_id = conference.get_id(),
        duedate = 1545411600000,
        completion_count = 50,
        inv_params = {
            'readers': [
                conference.get_id(),
                conference.get_program_chairs_id(),
                conference.get_area_chairs_id(),
                conference.get_reviewers_id()
            ],
            'invitees': [
                conference.get_area_chairs_id(),
                conference.get_reviewers_id()
            ],
            'web': os.path.abspath('../webfield/bidWebfield.js')
        },
        reply_params = {
            'invitation': conference.get_submission_id()
        }
    )
    bid_invitation = client.post_invitation(bid_invitation)

    # set up User Score notes

    if not all(['~' in member for member in reviewers.members]):
        print('WARNING: not all reviewers have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_reviewer_ids = [r for r in reviewers.members if '~' in r]

    if not all(['~' in member for member in area_chairs.members]):
        print('WARNING: not all area chairs have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_area_chairs_ids = [r for r in area_chairs.members if '~' in r]


    scores_inv = openreview.Invitation(
        id = conference.get_id() + '/-/User_Scores',
        invitees = [conference.get_id()],
        readers = ['everyone'],
        writers = [conference.get_id()],
        signatures = [conference.get_id()],
        reply = {
            'content': {},
            'forum': None,
            'replyto': None,
            'invitation': conference.get_submission_id(),
            'readers': {'values-regex':'~.*'},
            'writers': {'values': [conference.get_id()]}
        }
    )

    scores_inv = client.post_invitation(scores_inv)
    user_score_notes = {}
    for paper in openreview.tools.iterget_notes(client, invitation=conference.get_submission_id()):
        for user_id in valid_reviewer_ids:
            if user_id not in user_score_notes:
                user_score_notes[user_id] = openreview.Note.from_json({
                    'invitation': scores_inv.id,
                    'readers': [user_id],
                    'writers': [conference.get_id()],
                    'content': {
                        'user': user_id,
                        'scores': []
                    },
                    'signatures': [conference.get_id()],
                    'forum': None,
                    'multiReply': False
                })
            score_note = user_score_notes[user_id]

            score_entry = {
                'forum': paper.forum,
                'tfidfScore': float(tfidf_score_by_id[paper.id].get(user_id,0.0))
            }

            score_note.content['scores'].append(score_entry)

    for user_id, score_note in user_score_notes.items():
        print('posting score note for user {}'.format(user_id))
        client.post_note(score_note)
