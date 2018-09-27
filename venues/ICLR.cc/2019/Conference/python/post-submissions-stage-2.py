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

    original_notes = openreview.tools.iterget_notes(client, invitation=iclr19.submission_inv.id)

    for original in original_notes:
        blind_note = notes.post_blind_note(client, original)

        groups.create_and_post(client, blind_note, 'Paper')
        author_group = groups.create_and_post(client, blind_note, 'Paper/Authors', members=original.content['authorids'])

        original.readers = [
            iclr19.CONFERENCE_ID,
            author_group.id
        ]
        notes.freeze_and_post(client, original)

        invitations.enable_and_post(client, blind_note, 'Public_Comment')
        invitations.enable_and_post(client, blind_note, 'Official_Comment')
        invitations.enable_and_post(client, blind_note, 'Withdraw_Submission')

    reviewers_group = client.get_group(iclr19.REVIEWERS_ID)
    areachairs_group = client.get_group(iclr19.AREA_CHAIRS_ID)
    openreview.tools.replace_members_with_ids(client, reviewers_group)
    openreview.tools.replace_members_with_ids(client, areachairs_group)
    groups.update_homepage(client, '../webfield/homepagePostSubmission.js')
