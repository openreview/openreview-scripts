import openreview
import argparse
import datetime

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = openreview.helpers.get_conference(client, 'SkxpQPWdA4')

    ## Create reviewer registration tasks
    conference.invitation_builder.set_registration_invitation(conference, due_date = datetime.datetime(2019, 9, 25, 14, 59))

    ## Enable expertise selection interface
    expertise = conference.set_expertise_selection_stage(openreview.ExpertiseSelectionStage(due_date = datetime.datetime(2019, 9, 28, 14, 59)))


    ## Anonymize current submissions
    conference.create_blind_submissions()

    ## Create withdraw invitations
    conference.create_withdraw_invitations()

    ## Create desk reject invitations
    conference.create_desk_reject_invitations()

    ## Stage: discussion
    conference.set_comment_stage(openreview.CommentStage(allow_public_comments = True, unsubmitted_reviewers = True, reader_selection = True, email_pcs = False))

    ## Stage: bids
    conference.setup_matching(affinity_score_file='reviewer-path-to-scores.csv')
    conference.setup_matching(is_area_chair = True, affinity_score_file='ac-path-to-scores.csv')

    conference.set_bid_stage(openreview.BidStage(due_date = datetime.datetime(2019, 10, 2, 14, 59), use_affinity_score = True))

    ## Stage: paper matching
    conference.setup_matching(affinity_score_file='path-to-re-created-scores-reviewers.csv')
    conference.setup_matching(is_area_chair = True, affinity_score_file='path-to-re-created-scores-ac.csv')

    conference.set_assignments('reviewers-1')
    conference.set_assignments('acs-1')

    ## Stage: reviews
    remove_review_fields = ['review', 'confidence']
    additional_review_fields = {
        'title': {
            'order': 1,
            'value-regex': 'Official Blind Review #[0-9]+',
            'default': 'Official Blind Review #NUM',
            'description': 'Please replace NUM with your AnonReviewer number (it is the number following "AnonReviewer" in your signatures below)',
            'required': True
        },
        'rating': {
            'order': 2,
            'value-dropdown': [
                '1: Reject',
                '2: Weak Reject',
                '3: Weak Accept',
                '4: Accept'
            ],
            'required': True
        },
        'does the paper support its claims and contributions': {
            'order': 3,
            'value-radio': ['Yes', 'No'],
            'required': True
        },
        'experience assessment': {
            'order': 4,
            'value-radio': [
                'I have published in this field for several years.',
                'I have published one or two papers in this area.',
                'I have read many papers in this area.',
                'I do not know much about this area.'
            ],
            'description': 'Please make a selection that represents your experience correctly',
            'required': True
        },
        'review assessment: thoroughness in paper reading': {
            'order': 5,
            'values-checkbox': [
                'I read the paper thoroughly.',
                'I read the paper at least twice and used my best judgement in assessing the paper.',
                'I made a quick assessment of this paper.',
                'N/A'
            ],
            'description': 'Check a box or select N/A if it\'s not applicable',
            'required': True
        },
        'review assessment: checking correctness of derivations and theory': {
            'order': 6,
            'values-checkbox': [
                'I carefully checked the derivations and theory.',
                'I assessed the sensibility of the derivations and theory.',
                'I did not assess the derivations or theory.',
                'N/A'
            ],
            'description': 'Check a box or select N/A if no derivations or theory',
            'required': True
        },
        'review assessment: checking correctness of experiments': {
            'order': 7,
            'values-checkbox': [
                'I carefully checked the experiments.',
                'I assessed the sensibility of the experiments.',
                'I did not assess the experiments.',
                'N/A'
            ],
            'description': 'Check a box or select N/A if no experiments',
            'required': True
        }
    }

    review_stage = openreview.ReviewStage(
        due_date = datetime.datetime(2019, 10, 23, 14, 59),
        additional_fields = additional_review_fields,
        remove_fields = remove_review_fields
    )
    conference.set_review_stage(review_stage)

    ## Area chair decisions
    conference.set_meta_review_stage(openreview.MetaReviewStage(due_date = datetime.datetime(2019, 12, 6, 14, 59)))

    ## Program Chairs decisions
    conference.set_decision_stage(openreview.DecisionStage(due_date = datetime.datetime(2019, 12, 12, 14, 59)))

    ## Camera ready revisions
    conference.open_revise_submissions()
