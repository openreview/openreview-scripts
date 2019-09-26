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

    ## Anonymize current submissions
    conference.create_blind_submissions()

    ## Create withdraw invitations
    conference.create_withdraw_invitations()

    ## Stage: discussion
    conference.set_comment_stage(openreview.CommentStage(allow_public_comments = True, unsubmitted_reviewers = True, reader_selection = True, email_pcs = False))

    ## Stage: bids
    conference.set_bid_stage(openreview.BidStage(due_date = datetime.datetime(2019, 9, 25, 0, 0)))

    conference.setup_matching()

    conference.set_assignments('reviewers-1')

    ## Stage: reviews
    conference.set_review_stage(openreview.ReviewStage(due_date = datetime.datetime(2019, 9, 25, 0, 0)))

    ## Area chair decisions
    conference.set_meta_review_stage(openreview.MetaReviewStage(due_date = datetime.datetime(2019, 9, 25, 0, 0)))

    ## Program Chairs decisions
    conference.set_decision_stage(openreview.DecisionStage(due_date = datetime.datetime(2019, 9, 25, 0, 0)))

    ## Camera ready revisions
    conference.open_revise_submissions()