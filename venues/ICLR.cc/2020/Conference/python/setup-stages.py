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
            'I have published in this field for several years.',
            'I have published one or two papers in this area.',
            'I have read many papers in this area.',
            'I do not know much about this area.'
        ],
        'description': 'Please make a selection that represents your experience correctly',
        'required': True
    },
    'review_assessment:_thoroughness_in_paper_reading': {
        'order': 5,
        'value-radio': [
            'I read the paper thoroughly.',
            'I read the paper at least twice and used my best judgement in assessing the paper.',
            'I made a quick assessment of this paper.',
            'N/A'
        ],
        'description': 'If this is not applicable, please select N/A',
        'required': True
    },
    'review_assessment:_checking_correctness_of_derivations_and_theory': {
        'order': 6,
        'value-radio': [
            'I carefully checked the derivations and theory.',
            'I assessed the sensibility of the derivations and theory.',
            'I did not assess the derivations or theory.',
            'N/A'
        ],
        'description': 'If no derivations or theory, please select N/A',
        'required': True
    },
    'review_assessment:_checking_correctness_of_experiments': {
        'order': 7,
        'value-radio': [
            'I carefully checked the experiments.',
            'I assessed the sensibility of the experiments.',
            'I did not assess the experiments.',
            'N/A'
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

    ## Update Instruction page for reviewers and ACs
    conference.set_reviewerpage_header(
        {
            "schedule": "<p><ul>\
            <li>Reviews due : 23 October 2019, 6PM East Africa Time</li>\
            <li>Discussion & rebuttal period starts : 5 November 2019, 6PM East Africa Time</li>\
            <li>Rebuttal period ends : 15 November 2019, 6PM East Africa Time</li>\
            <li>Meta-Reviews due : 6 December 2019, 6PM East Africa Time</li>\
            </ul></p>"
        }
    )

    conference.set_areachairpage_header(
        {
            "schedule": "<p><ul>\
            <li>Reviews due : 23 October 2019, 6PM East Africa Time</li>\
            <li>Discussion & rebuttal period starts : 5 November 2019, 6PM East Africa Time</li>\
            <li>Rebuttal period ends : 15 November 2019, 6PM East Africa Time</li>\
            <li>AC-Reviewer discussion ends : 22 November 2019, 6PM East Africa Time</li>\
            <li>Meta-Reviewing period starts : 25 December 2019, 6PM East Africa Time</li>\
            <li>Meta-Reviews due : 6 December 2019, 6PM East Africa Time</li>\
            </ul></p>"
        }
    )

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
        due_date = datetime.datetime(2019, 11, 2, 14, 59),
        additional_fields = additional_review_fields,
        remove_fields = remove_review_fields,
        public = True
    )
    conference.set_review_stage(review_stage)

    blind_notes = conference.get_submissions()
    official_reviews = openreview.tools.iterget_notes(
        client,
        invitation = conference.id + '/Paper[0-9]+/-/Official_Review$'
    )
    map_paper_to_review = {}
    for review in official_reviews:
        paper_number = review.invitation.split('Paper')[1].split('/')[0]
        if paper_number not in map_paper_to_review:
            map_paper_to_review[paper_number] = []
        map_paper_to_review[paper_number].append(review)

    ## Stage: reviews  - Reveal reviews and update tags for the desk-reject question
    tag_due_date = datetime.datetime(2019, 11, 30, 14, 59)
    for note in blind_notes:
        tag_invi = client.post_invitation(get_tag_invitation(conference, note, tag_due_date))
        for review in map_paper_to_review.get(str(note.number), []):
            review.readers = ['everyone']
            review.nonreaders = []
            try:
                client.post_note(review)
                print ('Posted correctly for paper: ', str(note.number))
            except:
                print ('Error posting review: ', review.id)

    ## Area chair decisions
    conference.set_meta_review_stage(openreview.MetaReviewStage(due_date = datetime.datetime(2019, 12, 6, 14, 59)))

    ## Program Chairs decisions
    conference.set_decision_stage(openreview.DecisionStage(due_date = datetime.datetime(2019, 12, 12, 14, 59)))

    # Camera ready revisions
    conference.open_revise_submissions()
