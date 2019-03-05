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

    conference.set_program_chairs(emails = [])
    conference.set_reviewers(emails = [])
    conference.set_area_chairs(emails = [])

    conference.open_submissions(start_date = datetime.datetime(2019, 2, 15, 11, 59), due_date = datetime.datetime(2019, 3, 5, 11, 59), remove_fields = ['pdf'], additional_fields = {
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'required': False,
            'value-regex': 'upload'
        }
    })
