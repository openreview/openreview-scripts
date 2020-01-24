import openreview
import argparse
import datetime
from openreview import tools

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = openreview.helpers.get_conference(client, 'Syl0khB_iH')

    conference.create_blind_submissions(force=True)

    conference.set_authors()

    conference.open_revise_submissions(name = 'Revision', start_date = datetime.datetime(2020, 1, 25, 12), 
                                   due_date = datetime.datetime(2020, 1, 31, 14, 59), 
                                   additional_fields = {
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'required': True,
            'value-regex': 'upload',
            'order': 99
        }
    }, remove_fields = ['pdf'])

    for note in conference.get_submissions():
        note.ddate = tools.datetime_millis(datetime.datetime.now())
        note.content = {
            'authors': ['Anonymous'],
            'authorids': []
        }
        client.post_note(note)