import openreview
import config
import json
from collections import defaultdict

client = openreview.Client()
conference = config.get_conference(client)

all_reviews = list(openreview.tools.iterget_notes(
    client,
    invitation = conference.get_id() + '/-/Paper.*/Official_Review'
))

map_paper_max_review_number = defaultdict(lambda: 0)

for review in all_reviews:
    paper_number = str(review.invitation.split('Paper')[1].split('/')[0])
    review_invi = client.get_invitation(review.invitation)
    review_invi.reply['readers']['values'] = [
        conference.get_id() + '/Program_Chairs',
        conference.get_id() + '/Paper' + paper_number + '/Program_Committee',
        conference.get_id() + '/Paper' + paper_number + '/Authors'
        ]
    review.readers = [
        conference.get_id() + '/Program_Chairs',
        conference.get_id() + '/Paper' + paper_number + '/Program_Committee',
        conference.get_id() + '/Paper' + paper_number + '/Authors'
        ]
    client.post_invitation(review_invi)
    client.post_note(review)

    next_review_number = str(map_paper_max_review_number.get(paper_number, 0) + 1)

    # Post author rebuttal invitation
    rebuttal_invitation = openreview.Invitation(
        id = conference.get_id() + '/-/Paper' + paper_number + '/Review' + next_review_number + '/Rebuttal',
        invitees = [
            conference.get_id() + '/Paper' + paper_number + '/Authors'
        ],
        duedate = 1553742000000,
        signatures = [conference.get_id()],
        readers = [
            conference.get_id() + '/Program_Chairs',
            conference.get_id() + '/Paper' + paper_number + '/Program_Committee',
            conference.get_id() + '/Paper' + paper_number + '/Authors'
        ],
        writers = [conference.get_id()],
        multiReply = False,
        reply = {
            'forum': review.forum,
            'replyto': review.id,
            'readers': {'values': [
                conference.get_id() + '/Paper' + paper_number + '/Authors',
                conference.get_id() + '/Paper' + paper_number + '/Program_Committee',
                conference.get_id() + '/Program_Chairs'
                ]
            },
            'writers': {
                'values': [conference.get_id() + '/Paper' + paper_number + '/Authors']
            },
            'signatures': {
                'values-regex': conference.get_id() + '/Paper' + paper_number + '/Authors'
            },
            'content': {
                'title': {
                    'order': 1,
                    'value-regex': '.{0,500}',
                    'description': 'Title of the rebuttal.',
                    'required': True
                },
                'rebuttal': {
                    'order': 2,
                    'value-regex': '[\\S\\s]{1,200000}',
                    'description': 'Maximum 200000 characters.',
                    'required': True
                }
            }
        }
    )
    map_paper_max_review_number[paper_number] = int(next_review_number)
    posted_rebuttal_invitation = client.post_invitation(rebuttal_invitation)
    print ("Rebuttal invitation posted with id: ", posted_rebuttal_invitation.id )