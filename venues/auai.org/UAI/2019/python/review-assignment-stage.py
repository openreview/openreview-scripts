import argparse
import openreview
from openreview import invitations
import datetime
import os
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

    conference.close_bids()
    conference.set_reviewerpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 reviewers. It will be regularly updated as the conference progresses, \
            so please check back frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
            <p>\
            Update your profile to include your most up-to-date information, including emails,  \
                work history and relations, to ensure proper conflict-of-interest detection \
                during the paper matching process.\
            </p>\
        <br>\
        <h4>Bidding Phase</h4>\
        <p>\
        <em>Please note that the bidding phase is over now.</em>\
        </p>\
        <br>'
    })
    conference.set_areachairpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 area chairs. It will be regularly updated as the conference progresses, \
            so please check back frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
            <p>\
            Update your profile to include your most up-to-date information, including emails,  \
                work history and relations, to ensure proper conflict-of-interest detection \
                during the paper matching process.\
            </p>\
        <br>\
        <h4>Bidding Phase</h4>\
        <p>\
        <em>Please note that the bidding phase is over now.</em>\
        </p>\
        <br>'
    })
    conference.setup_matching(affinity_score_file = '../data/affinity_scores.csv')
