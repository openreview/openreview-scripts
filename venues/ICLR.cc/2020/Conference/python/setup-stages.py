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

    conference = openreview.helpers.get_conference(client, 'Skli7GteaN')

    ## Anonymize current submissions
    conference.create_blind_submissions()

    ## Setup committee consoles
    conference.set_authors()
    conference.set_area_chairs([])
    conference.set_reviewers([])

    ## Stage: bids
    conference.open_bids(due_date = datetime.datetime(2019, 9, 25, 0, 0), with_area_chairs = True)

    ## Stage: reviews
    conference.open_reviews(due_date = datetime.datetime(2019, 9, 25, 0, 0))

    ## Stage: discussion
    conference.open_comments(name = 'Official_Comment', public = False, anonymous = True, reader_selection = True)
    conference.open_comments(name = 'Public_Comment', public = True, anonymous = False)

    ## Area chair decisions
    conference.open_meta_reviews(due_date = datetime.datetime(2019, 9, 25, 0, 0))

    ## Program Chairs decisions
    conference.open_decisions(due_date = datetime.datetime(2019, 9, 25, 0, 0))

    ## Camera ready revisions
    conference.open_revise_submissions()