import openreview
import argparse
import datetime

remove_review_fields = ['confidence']
additional_review_fields = {
    'title': {
        'order': 1,
        'value-regex': 'Official Blind Review #[0-9]+',
        'default': 'Official Blind Review #NUM',
        'description': 'Please replace NUM with your AnonReviewer number (it is the number following "AnonReviewer" in your signatures below)',
        'required': True
    },
    'review': {
        'order': 2,
        'value-regex': '[\\S\\s]{500,200000}',
        'description': 'Provide your complete review here (500 - 200000 characters). For guidance in writing a good review, see this brief reviewer guide (https://iclr.cc/Conferences/2020/ReviewerGuide) with three key bullet points.',
        'required': True
    },
    'rating': {
        'order': 3,
        'value-dropdown': [
            '1: Reject',
            '3: Weak Reject',
            '6: Weak Accept',
            '8: Accept'
        ],
        'required': True
    },
    'experience_assessment': {
        'order': 4,
        'value-radio': [
            '5: I have published in this field for several years.',
            '4: I have published one or two papers in this area.',
            '3: I have read many papers in this area.',
            '1: I do not know much about this area.'
        ],
        'description': 'Please make a selection that represents your experience correctly',
        'required': True
    },
    'review_assessment:_thoroughness_in_paper_reading': {
        'order': 5,
        'value-radio': [
            '5: I read the paper thoroughly.',
            '3: I read the paper at least twice and used my best judgement in assessing the paper.',
            '1: I made a quick assessment of this paper.',
            '0: N/A'
        ],
        'description': 'If this is not applicable, please select N/A',
        'required': True
    },
    'review_assessment:_checking_correctness_of_derivations_and_theory': {
        'order': 6,
        'value-radio': [
            '5: I carefully checked the derivations and theory.',
            '3: I assessed the sensibility of the derivations and theory.',
            '0: I did not assess the derivations or theory.',
            '0: N/A'
        ],
        'description': 'If no derivations or theory, please select N/A',
        'required': True
    },
    'review_assessment:_checking_correctness_of_experiments': {
        'order': 7,
        'value-radio': [
            '5: I carefully checked the experiments.',
            '3: I assessed the sensibility of the experiments.',
            '0: I did not assess the experiments.',
            '0: N/A'
        ],
        'description': 'If no experiments, please select N/A',
        'required': True
    }
}

def get_tag_invitation(conference, note, due_date):
    return openreview.Invitation(
        readers = [conference.get_reviewers_id(note.number), conference.get_program_chairs_id()],
        invitees = [conference.get_reviewers_id(note.number)],
        id = conference.get_invitation_id(name = 'Support_Desk_Rejection', number = note.number),
        signatures = [conference.get_id()],
        writers = [conference.get_id()],
        duedate = openreview.tools.datetime_millis(due_date),
        expdate = openreview.tools.datetime_millis(due_date),
        multiReply = False,
        reply = {
            'forum' : note.forum,
            'replyto' : note.forum,
            "invitation" : conference.get_blind_submission_id(),
            "readers" : {
                "description": "The users who will be allowed to read the above content.",
                "values-copied": [
                    conference.get_program_chairs_id(),
                    '{signatures}'
                ]
            },
            "signatures" : {
                "description": "How your identity will be displayed with the above content.",
                "values-regex": "~.*"
            },
            "writers": {
                "values-regex": "~.*"
            },
            "content": {
                "tag": {
                    "description": "Should this paper have been desk rejected? (Note, this information will remain private, and is not visible to the authors)",
                    "order": 1,
                    "value-dropdown": [
                        "No",
                        "Yes"
                    ],
                    "required": True
                }
            }
        }
    )


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

    conference.set_assignments('reviewers-bids-elmo-final')
    conference.set_assignments('areachairs-bids-elmo', is_area_chair=True)

    ## Stage: reviews - Enable review invitations
    review_stage = openreview.ReviewStage(
        due_date = datetime.datetime(2019, 10, 23, 14, 59),
        additional_fields = additional_review_fields,
        remove_fields = remove_review_fields
    )
    conference.set_review_stage(review_stage)

    ## Stage: reviews  - Enable reviewers to post tags for the desk-reject question
    blind_notes = conference.get_submissions()
    tag_due_date = datetime.datetime(2019, 10, 23, 14, 59)
    for note in blind_notes:
        tag_invi = client.post_invitation(get_tag_invitation(conference, note, tag_due_date))

    ## Area chair decisions
    conference.set_meta_review_stage(openreview.MetaReviewStage(due_date = datetime.datetime(2019, 12, 6, 14, 59)))

    ## Program Chairs decisions
    conference.set_decision_stage(openreview.DecisionStage(due_date = datetime.datetime(2019, 12, 12, 14, 59)))

    ## Camera ready revisions
    conference.open_revise_submissions()
