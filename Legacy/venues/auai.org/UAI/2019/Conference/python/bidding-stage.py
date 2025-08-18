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


    conference.open_bids(due_date = datetime.datetime(2019, 3, 19, 10, 59), request_count = 30, with_area_chairs = True)
    conference.set_reviewerpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 reviewers. It will be regularly updated as the conference progresses, \
            so please check the "Reviewer Schedule" and "Review Tasks" section frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
        <p>\
            <em><strong>Please do the following by 23:59 PM Samoa Time, Friday, March 18 2019</strong></em>:\
            <ul>\
                <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
                <li>Complete the UAI 2019 registration form (found in your "Reviewer Tasks").</li>\
                <li>Register subject areas indicating your expertise (through UAI 2019 registration form).</li>\
            </ul>\
        </p><br>\
        <h4>Bidding Phase</h4>\
        <p>\
            <em><strong>Please note that bidding has begun. You are requested to do the\
            following by 23:59 PM Samoa Time, March 18th 2019</strong></em>:\
            <ul>\
                <li>Provide your reviewing preferences by bidding on papers using the Bidding \
                Interface.</li>\
                <li><strong><a href="/invitation?id=auai.org/UAI/2019/Conference/-/Bid">Go to \
                Bidding Interface</a></strong></li>\
            </ul>\
            </p>\
        <br>'
    })
    conference.set_areachairpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 area chairs. It will be regularly updated as the conference progresses, \
            so please check the "Area Chair Schedule" and "Area Chair Tasks" sections frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
            <p>\
            <em><strong>Please do the following by 23:59 PM Samoa Time, Friday, March 18 2019</strong></em>:\
            <ul>\
                <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
                <li>Complete the UAI 2019 registration form (found in your "Area Chair Tasks").</li>\
                <li>Register subject areas indicating your expertise (through UAI 2019 registration form).</li>\
            </ul>\
            </p>\
        <br>\
        <h4>Bidding Phase</h4>\
            <p>\
            <em><strong>Please note that bidding has begun. You are requested to do the\
            following by 23:59 PM Samoa Time, March 18th 2019</strong></em>:\
            <ul>\
                <li>Provide your reviewing preferences by bidding on papers using the Bidding \
                Interface.</li>\
                <li><strong><a href="/invitation?id=auai.org/UAI/2019/Conference/-/Bid">Go to \
                Bidding Interface</a></strong></li>\
            </ul>\
            </p>\
        <br>'
    })
