'''
Post-submission Stage (Sept. 27 - Oct 1)

- Anonymous, publicly visible submissions are made available to the public.
- Author permission to edit papers is revoked.
- ICLR 2019 homepage is updated to show anonymous submissions.
- Commentary is enabled. Comment rules:
- - Reviewers, authors, and area chairs are forced to comment anonymously.
- - Members of the public may comment with their public ID (e.g. ~Michael_Spector1)
- - Readership of comments can be set to a subset of the following groups: [ Everyone, Paper Reviewers, Paper Authors, Paper ACs, Program Chairs ]

- Papers, reviewer IDs, areachair IDs sent to Laurent Charlin for TPMS processing.
- Receive TPMS scores from Laurent.


'''

import openreview
import iclr19
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

    client.post_invitation(iclr19.blind_submission_inv)

    original_notes = list(openreview.tools.iterget_notes(client, invitation=iclr19.submission_inv.id))
    blind_notes = notes.post_blind_notes(client, original_notes)

    groups.create_and_post(client, blind_notes, 'Paper')
    groups.create_and_post(client, blind_notes, 'Paper/Authors')
    groups.update_homepage(client, '../webfield/homepagePostSubmission.js')

    notes.freeze_and_post(client, original_notes)

    invitations.enable_and_post(client, blind_notes, 'Public_Comment')
    invitations.enable_and_post(client, blind_notes, 'Official_Comment')
