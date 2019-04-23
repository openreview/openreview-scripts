import argparse
import openreview
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    all_reviews = list(openreview.tools.iterget_notes(
        client,
        invitation = conference.get_id() + '/-/Paper.*/Official_Review'
    ))
    all_quality_invis = list(openreview.tools.iterget_invitations(
        client,
        regex = conference.get_id() + '/-/Paper[0-9]+/Review[0-9]+/Review_Quality$'
    ))

    map_paper_reviews = {}
    for review in all_reviews:
        paper_number = int(review.invitation.split('Paper')[1].split('/')[0])
        if paper_number not in map_paper_reviews:
            map_paper_reviews[paper_number] = {}
        map_paper_reviews[paper_number][review.id] = review

    map_paper_max_review_number = {}
    map_paper_review_quality_invi = {}

    for invitation in all_quality_invis:
        paper_number = int(invitation.id.split('Paper')[1].split('/')[0])
        invitation_serial = int(invitation.id.split('Review')[1].split('/')[0])
        if (map_paper_max_review_number.get(paper_number, 0) < invitation_serial):
            map_paper_max_review_number[paper_number] = invitation_serial

        if paper_number not in map_paper_review_quality_invi:
            map_paper_review_quality_invi[paper_number] = []
        map_paper_review_quality_invi[paper_number].append(invitation.reply['replyto'])

    new_reviews = {}

    for paper_number in map_paper_reviews:
        current_reviews = list(map_paper_reviews[paper_number].keys())
        reviews_with_invitations = map_paper_review_quality_invi.get(paper_number)
        if reviews_with_invitations:
            new_review_ids = list(set(current_reviews) - set(reviews_with_invitations))
        else:
            new_review_ids = current_reviews
        if new_review_ids:
            for review in new_review_ids:
                new_reviews[review] = map_paper_reviews[paper_number][review]

    for review in new_reviews:
        paper_number = str(new_reviews[review].invitation.split('Paper')[1].split('/')[0])

        next_review_number = str(map_paper_max_review_number.get(int(paper_number),0) + 1)

        # Post review quality invitation
        review_quality_invitation = openreview.Invitation(
            id = conference.get_id() + '/-/Paper' + paper_number + '/Review' + next_review_number + '/Review_Quality',
            invitees = [
                conference.get_id() + '/Paper' + paper_number + '/Area_Chairs'
            ],
            duedate = 1557788400000,
            signatures = [conference.get_id()],
            readers = [
                conference.get_id() + '/Program_Chairs',
                conference.get_id() + '/Paper' + paper_number + '/Area_Chairs'
            ],
            writers = [conference.get_id()],
            multiReply = False,
            reply = {
                'forum': new_reviews[review].forum,
                'replyto': new_reviews[review].id,
                'readers': {'values': [
                    conference.get_id() + '/Paper' + paper_number + '/Area_Chairs',
                    conference.get_id() + '/Program_Chairs'
                    ]
                },
                'writers': {
                    'values': [conference.get_id() + '/Paper' + paper_number + '/Area_Chairs']
                },
                'signatures': {
                    'values-regex': conference.get_id() + '/Paper' + paper_number + '/Area_Chair[0-9]+'
                },
                'content': {
                    'title': {
                        'order': 1,
                        'value': 'Review Quality Evaluation',
                        'description': 'Title',
                        'required': True
                    },
                    'review quality': {
                        'order': 2,
                        'value-dropdown': ['Good review', 'Adequate Review', 'Poor Review'],
                        'description': 'Select your best estimate of the review\'s quality',
                        'required': True
                    }
                    }
            }
        )
        map_paper_max_review_number[int(paper_number)] = int(next_review_number)
        posted_review_quality_invitation = client.post_invitation(review_quality_invitation)
        print ("Review quality invitation {} posted ".format(posted_review_quality_invitation.id))