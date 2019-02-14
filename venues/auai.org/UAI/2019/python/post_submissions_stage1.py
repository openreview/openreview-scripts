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

    conference.close_submissions()

    conference.open_revise_submissions(name = 'Revision', due_date = datetime.datetime(2019, 3, 9, 11, 59), public = False, additional_fields = {
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'required': True,
            'value-regex': 'upload',
            'order': 99
        }
    }, remove_fields = ['title', 'pdf'])

