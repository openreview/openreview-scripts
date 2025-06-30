import openreview
import config
import json
from collections import defaultdict

client = openreview.Client()

all_reviews = list(openreview.tools.iterget_notes(
    client,
    invitation = 'learningtheory.org/COLT/2019/Conference/-/Paper.*/Official_Review'
))

all_rebuttal_invis = list(openreview.tools.iterget_invitations(
    client,
    regex = 'learningtheory.org/COLT/2019/Conference/-/Paper[0-9]+/Review[0-9]+/Rebuttal'
))

map_paper_reviews = {}
for review in all_reviews:
    paper_number = int(review.invitation.split('Paper')[1].split('/')[0])
    if paper_number not in map_paper_reviews:
        map_paper_reviews[paper_number] = {}
    map_paper_reviews[paper_number][review.id] = review

map_paper_max_review_number = defaultdict(lambda: 0)
map_paper_rebuttal_invi = {}

for invitation in all_rebuttal_invis:
    paper_number = int(invitation.id.split('Paper')[1].split('/')[0])
    invitation_serial = int(invitation.id.split('Review')[1].split('/')[0])
    if (map_paper_max_review_number.get(paper_number, 0) < invitation_serial):
        map_paper_max_review_number[paper_number] = invitation_serial

    if paper_number not in map_paper_rebuttal_invi:
        map_paper_rebuttal_invi[paper_number] = []
    map_paper_rebuttal_invi[paper_number].append(invitation.reply['replyto'])

new_reviews = {}

for paper_number in map_paper_reviews:
    current_reviews = list(map_paper_reviews[paper_number].keys())
    reviews_with_invitations = map_paper_rebuttal_invi[paper_number]
    new_review_ids = list(set(current_reviews) - set(reviews_with_invitations))
    if new_review_ids:
        for review in new_review_ids:
            new_reviews[review] = map_paper_reviews[paper_number][review]

for review in new_reviews:
    paper_number = str(new_reviews[review].invitation.split('Paper')[1].split('/')[0])

    next_review_number = str(map_paper_max_review_number[int(paper_number)] + 1)

    # Post author rebuttal invitation
    rebuttal_invitation = openreview.Invitation(
        id = 'learningtheory.org/COLT/2019/Conference/-/Paper' + paper_number + '/Review' + next_review_number + '/Rebuttal',
        invitees = [
            'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors'
        ],
        duedate = 1553742000000,
        signatures = ['learningtheory.org/COLT/2019/Conference'],
        readers = [
            'learningtheory.org/COLT/2019/Conference/Program_Chairs',
            'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Program_Committee',
            'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors'
        ],
        writers = ['learningtheory.org/COLT/2019/Conference'],
        multiReply = False,
        reply = {
            'forum': new_reviews[review].forum,
            'replyto': new_reviews[review].id,
            'readers': {'values': [
                'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors',
                'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Program_Committee',
                'learningtheory.org/COLT/2019/Conference/Program_Chairs',
                'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Reviewers/Discussion'
                ]
            },
            'writers': {
                'values': ['learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors']
            },
            'signatures': {
                'values-regex': 'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors'
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
                    'value-regex': '[\\S\\s]{1,4000}',
                    'description': 'Maximum 4000 characters.',
                    'required': True
                }
                }
        }
    )
    map_paper_max_review_number[int(paper_number)] = int(next_review_number)
    posted_rebuttal_invitation = client.post_invitation(rebuttal_invitation)
    print ("Rebuttal invitation {} posted ".format(posted_rebuttal_invitation.id))
