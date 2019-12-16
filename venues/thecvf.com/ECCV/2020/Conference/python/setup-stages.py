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

    conference = openreview.helpers.get_conference(client, 'Skx6tVahYB')

    ## Update Instruction page for reviewers and ACs
    conference.set_reviewerpage_header(
        {
            "schedule": "<p><ul>\
            <li>Paper Submission Deadline: March 5, 2020</li>\
            <li>Reviewer bidding period : March 6-15, 2020</li>\
            <li>Reviewing period : April 3 - May 10, 2020</li>\
            <li><strong>Reviews due : May 10, 2020</strong></li>\
            <li>Discussion period and final recommendations due : May 28 - June 7, 2020</li>\
            <li><strong>Final recommendation due : June 7, 2020</strong></li>\
            <li><strong>Decisions to authors : June 7, 2020</strong></li>\
            </ul></p>"
        }
    )

    conference.set_areachairpage_header(
        {
            "schedule": "<p><ul>\
            <li>Paper Submission Deadline: March 5, 2020</li>\
            <li>AC bidding period : March 6-15, 2020</li>\
            <li>Reviewing period : April 3 - May 10, 2020</li>\
            <li><strong>Reviews due : May 10, 2020</strong></li>\
            <li>Discussion period and final recommendations due : May 28 - June 7, 2020</li>\
            <li><strong>Final recommendation due : June 7, 2020</strong></li>\
            <li><strong>Decisions to authors : June 7, 2020</strong></li>\
            </ul></p>"
        }
    )

    conference.set_authorpage_header(
        {
            "schedule": "<p><ul>\
            <li>Paper Submission Deadline: March 5, 2020</li>\
            <li>Reviewing period : April 3 - May 10, 2020</li>\
            <li>Discussion period and final recommendations due : May 28 - June 7, 2020</li>\
            <li><strong>Decisions to authors : June 7, 2020</strong></li>\
            </ul></p>"
        }
    )

    ## Create reviewer and AC registration tasks
    reviewer_registration_tasks = {
        'profile_confirmed': {
            'description': 'In order to avoid conflicts of interest in reviewing, we ask that all reviewers take a moment to update their OpenReview profiles (link in instructions above) with their latest information regarding email addresses, dblp profile, google scholar profile, work history and professional relationships. Please confirm that your OpenReview profile is up-to-date by selecting "Yes".\n\n',
            'value-radio': ['Yes'],
            'required': True,
            'order': 1},
        'expertise_confirmed': {
            'description': 'We will be using OpenReview\'s Expertise System as one of the factors in calculating paper-reviewer affinity scores. Please take a moment to ensure that your latest papers are visible at the Expertise Selection (link in instructions above). Please confirm finishing this step by selecting "Yes".\n\n',
            'value-radio': ['Yes'],
            'required': True,
            'order': 2},
        'TPMS_registration_confirmed' : {
            'required': True,
            'description': 'Have you registered and/or updated your TPMS account (http://torontopapermatching.org/webapp/profileBrowser/login/), and updated your OpenReview profile to INCLUDE the email address you used for TPMS?',
            'value-radio': ['Yes'],
            'order': 3},
        'reviewer_compliance_-_review_count' : {
            'required': True,
            'description': 'Please confirm that you will provide the minimum number of reviews agreed upon by you when you accepted the invitation to review.',
            'value-radio': ['Yes'],
            'order': 4},
        'reviewer_compliance_-_instructions_for_reviewers' : {
            'required': True,
            'description': 'Please confirm that you will adhere to the reviewer instructions available at https://docs.google.com/document/d/1ifx0sIOnCQ2lCjBxy6IQun4xjZlSNyozTQexcMzcN9o/edit?usp=sharing.',
            'value-radio': ['Yes'],
            'order': 5},
        'emergency_review' : {
            'required': True,
            'description': 'Will you be able to serve as emergency reviewer? If yes, make sure that you are able to review papers within 72-96 hours in the time from May 15 to May 19.',
            'value-radio': [
                'Yes, I can provide 2 emergency reviews',
                'Yes, I can provide 1 emergency review',
                'No, I can not serve as an emergency reviewer'],
            'order': 6}
    }
    conference.open_registration(
        due_date = datetime.datetime(2020, 3, 5, 14, 59),
        additional_fields = reviewer_registration_tasks)

    ac_registration_tasks = {
        'profile_confirmed': {
            'description': 'In order to avoid conflicts of interest, we ask that all area chairs take a moment to update their OpenReview profiles (link in instructions above) with their latest information regarding email addresses, dblp profile, google scholar profile, work history and professional relationships. Please confirm that your OpenReview profile is up-to-date by selecting "Yes".\n\n',
            'value-radio': ['Yes'],
            'required': True,
            'order': 1},
        'TPMS_registration_confirmed' : {
            'required': True,
            'description': 'Have you registered and/or updated your TPMS account (http://torontopapermatching.org/webapp/profileBrowser/login/), and updated your OpenReview profile to INCLUDE the email address you used for TPMS?',
            'value-radio': ['Yes'],
            'order': 3}
    }
    conference.open_registration(
        due_date = datetime.datetime(2020, 3, 5, 14, 59),
        additional_fields = ac_registration_tasks,
        is_area_chair = True)

    ## Enable expertise selection interface
    expertise = conference.set_expertise_selection_stage(
        openreview.ExpertiseSelectionStage(
            due_date = datetime.datetime(2020, 3, 15, 14, 59)))

    ## Anonymize current submissions
    conference.create_blind_submissions()

    ## Create withdraw invitations
    conference.create_withdraw_invitations()

    ## Create desk reject invitations
    conference.create_desk_reject_invitations()

    ## Stage: discussion
    conference.set_comment_stage(openreview.CommentStage(allow_public_comments = False, unsubmitted_reviewers = False, reader_selection = True, email_pcs = False))

    ## Stage: bids
    conference.setup_matching(affinity_score_file='reviewer-path-to-scores.csv')
    conference.setup_matching(is_area_chair = True, affinity_score_file='ac-path-to-scores.csv')

    conference.set_bid_stage(openreview.BidStage(due_date = datetime.datetime(2020, 3, 15, 14, 59), use_affinity_score = True))

    ## Stage: paper matching
    conference.setup_matching(affinity_score_file='path-to-re-created-scores-reviewers.csv')
    conference.setup_matching(is_area_chair = True, affinity_score_file='path-to-re-created-scores-ac.csv')

    conference.set_assignments('reviewers-bids-elmo-final')
    conference.set_assignments('areachairs-bids-elmo', is_area_chair=True)

    ## Stage: reviews - Enable review invitations
    review_stage = openreview.ReviewStage(
        due_date = datetime.datetime(2020, 5, 10, 14, 59),
        additional_fields = additional_review_fields,
        remove_fields = remove_review_fields,
        public = True
    )
    conference.set_review_stage(review_stage)

    ## Stage: Enable meta-review invitations
    conference.set_meta_review_stage(
        openreview.MetaReviewStage(
            due_date = datetime.datetime(2020, 6, 7, 14, 59),
            additional_fields = meta_review_fields
        )
    )

    ## Stage: Program Chairs decisions
    conference.set_decision_stage(openreview.DecisionStage(due_date = datetime.datetime(2020, 6, 7, 14, 59)))

    ## Stage: Camera ready revisions
    conference.open_revise_submissions()
