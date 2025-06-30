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


def send_email(email, user, role):

    subject = 'MIDL 2019: [Optional] Please Bid on Submissions'
    message = '''
Dear {user},

Thank you again for agreeing to serve as {role} for the International Conference on Medical Imaging with Deep Learning (MIDL).

In an effort to ensure satisfactory paper assignments, we have decided this year to experiment with an optional bidding stage. You will have from the submission deadline on Monday, December 17th, until Thursday, December 20th to submit your reviewing preferences on any of the submitted papers.

Bidding is completely optional. That being said, it is in your interest to bid on as many papers as you can, because both positive and negative bids will be considered during the paper matching process.

To submit your bids, please visit https://openreview.net/invitation?id=MIDL.io/2019/Conference/-/Bid

If you have any other questions, please contact the program chairs at program-chairs@midl.io or the OpenReview support team at info@openreview.net.

Cheers!

Ipek Oguz, Gozde Unal and Ender Konukoglu
Program Chairs for Medical Imaging with Deep Learning 2019
    '''.format(user = user, role = role)

    return client.send_mail(subject, [email], message)

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

    with open('../webfield/reviewerWebfieldBiddingEnabled.js','r') as f:
        reviewers = client.get_group(conference.get_reviewers_id())
        reviewers.web = f.read()
        reviewers = client.post_group(reviewers)

    with open('../webfield/areachairWebfieldBiddingEnabled.js','r') as f:
        area_chairs = client.get_group(conference.get_area_chairs_id())
        area_chairs.web = f.read()
        area_chairs = client.post_group(area_chairs)



    bid_invitation = openreview.invitations.AddBid(
        conference_id = conference.get_id(),
        duedate = 1545325200000,
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
                'tfidfScore': float(tfidf_score_by_id.get(paper.id, {}).get(user_id,0.0))
            }

            score_note.content['scores'].append(score_entry)

    for user_id, score_note in user_score_notes.items():
        print('posting score note for user {}'.format(user_id))
        client.post_note(score_note)

    # Send emails
    for member in reviewers.members:
        send_email(member, 'Reviewer', 'a reviewer')

    for member in area_chairs.members:
        send_email(member, 'Area Chair', 'an area chair')
