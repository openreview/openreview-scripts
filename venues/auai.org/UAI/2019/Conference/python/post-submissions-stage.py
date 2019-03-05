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

    conference.create_blind_submissions()
    conference.set_authors()

    conference.open_revise_submissions(name = 'Revision', start_date = datetime.datetime(2019, 2, 5, 11, 59), due_date = datetime.datetime(2019, 3, 9, 11, 59), additional_fields = {
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'required': True,
            'value-regex': 'upload',
            'order': 99
        }
    }, remove_fields = ['title', 'pdf'])

    conference.set_authorpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 Authors. It will be regularly updated as the conference progresses, \
            so please check back frequently for news and other updates.</p>',
        'schedule': '<h4>Submission Period</h4>\
            <p>\
                <em><strong>Abstract Submission deadline: March 4th, 2019, 11:59 pm SST (Samoa Standard Time)</strong></em>:\
                <ul>\
                    <li>Abtract submissions are closed now.</li>\
                </ul>\
            </p>\
            <br>\
            <p>\
                <em><strong>Paper Submission deadline: March 8th, 2019, 11:59 pm SST (Samoa Standard Time)</strong></em>:\
                <ul>\
                    <li>Authors can make paper submissions by creating revisions of their papers as many times as needed up to the full paper submission deadline.</li>\
                    <li>Please ensure that the email addresses of the corresponding authors are up-to-date in their profiles.</li>\
                </ul>\
            </p>'
    })

    
