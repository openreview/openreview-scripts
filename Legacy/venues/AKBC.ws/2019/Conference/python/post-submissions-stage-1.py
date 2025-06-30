'''
Post-submission Stage 1 (Midnight Nov 16)

- Author permission to edit papers is revoked.
- AKBC 2019 homepage is updated to show anonymous submissions.

'''

import openreview
import akbc19 as conference_config
import notes
import groups
import invitations
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    original_notes = openreview.tools.iterget_notes(client, invitation=conference_config.submission_inv.id)

    for original in original_notes:
        notes.freeze_and_post(client, original)
        print('freezing note {}'.format(original.id))

    groups.update_homepage(client, '../webfield/homepagePostSubmission.js')
