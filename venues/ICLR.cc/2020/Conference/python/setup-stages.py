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
    conference.set_review_stage(openreview.ReviewStage(due_date = datetime.datetime(2019, 10, 23, 14, 59)))

    ## Area chair decisions
    conference.set_meta_review_stage(openreview.MetaReviewStage(due_date = datetime.datetime(2019, 12, 6, 14, 59)))

    ## Program Chairs decisions
    conference.set_decision_stage(openreview.DecisionStage(due_date = datetime.datetime(2019, 12, 12, 14, 59)))

    ## Camera ready revisions
    conference.open_revise_submissions()
