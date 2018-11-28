'''
Create review rating invitations for all reviewers. This will be an invitation to rate reviews from other reviewers on the same paper
'''

import argparse
import openreview
import iclr19

def get_paper_reviews(client, paper_number):
    reply_notes = client.get_notes(invitation = iclr19.CONFERENCE_ID + "/-/Paper{}/Official_Review".format(paper_number))
    map_anon_reviewer_to_replynote = {}
    for note in reply_notes:
        anon_rev = note.signatures[0].split("/")[-1]
        map_anon_reviewer_to_replynote[anon_rev] = note.id
    return map_anon_reviewer_to_replynote

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    review_rating_template = {
        'id': iclr19.CONFERENCE_ID + '/-/Paper{number}/AnonReviewer{AnonRevSerial}>/Review_Rating',
        'readers': ['everyone'],
        'writers': [iclr19.CONFERENCE_ID],
        'invitees': [],
        'noninvitees': [],
        'signatures': [iclr19.CONFERENCE_ID],
        'duedate': iclr19.REVIEW_RATING_DEADLINE,
        'process': None,
        'multiReply': None,
        'reply': {
            'forum': '<forum>',
            'replyto': None,
            'invitation': iclr19.OFFICIAL_REVIEW_TEMPLATE_STR,
            'readers': {
                'description': 'The users who will be allowed to read the reply content.',
                'values-copied': [iclr19.CONFERENCE_ID, iclr19.PROGRAM_CHAIRS_ID]
            },
            'nonreaders': {
                'values': [iclr19.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': iclr19.PAPER_ANONREVIEWERS_TEMPLATE_REGEX
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values-copied':  [
                    '{signatures}'
                ]
            },
            'content': openreview.invitations.content.review_rating
        }
    }

    papers_rate_reviews = [1155] #, 987, 1071, 60, 1550]

    # Get all reviews for these papers
    map_paper_to_anonrev_review_note = {}
    for paper in papers_rate_reviews:
        map_paper_to_anonrev_review_note[paper] = get_paper_reviews(client, paper)

    print (map_paper_to_anonrev_review_note)

    for paper in map_paper_to_anonrev_review_note:
        