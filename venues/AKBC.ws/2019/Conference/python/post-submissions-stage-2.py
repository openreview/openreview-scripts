'''
Post-submission Stage 2 (Nov 17 - )

- Anonymous, publicly visible submissions are made available to the public.
- Commentary is enabled. Comment rules:
- - Reviewers, authors, and area chairs are forced to comment anonymously.
- - Members of the public may comment with their public ID (e.g. ~Michael_Spector1)
- - Readership of comments can be set to a subset of the following groups: [ Everyone, Paper Reviewers, Paper Authors, Paper ACs, Program Chairs ]

- Papers, reviewer IDs, areachair IDs sent to Laurent Charlin for TPMS processing.
- Receive TPMS scores from Laurent.


'''

import openreview
import akbc19 as conferenceConfig
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

    client.post_invitation(conferenceConfig.blind_submission_inv)

    original_notes = openreview.tools.iterget_notes(client, invitation=conferenceConfig.submission_inv.id)

    for original in original_notes:
        print('processing {}'.format(original.id))
        blind_note = notes.post_blind_note(client, original)

        groups.create_and_post(client, blind_note, 'Paper')
        author_group = groups.create_and_post(client, blind_note, 'Paper/Authors', members=original.content['authorids'])

        original.readers = [
            conferenceConfig.CONFERENCE_ID,
            author_group.id
        ]
        notes.freeze_and_post(client, original)

        invitations.enable_and_post(client, blind_note, 'Public_Comment')
        invitations.enable_and_post(client, blind_note, 'Official_Comment')
        invitations.enable_and_post(client, blind_note, 'Withdraw_Submission')

    reviewers_group = client.get_group(conferenceConfig.REVIEWERS_ID)
    areachairs_group = client.get_group(conferenceConfig.AREA_CHAIRS_ID)
    all_emails = reviewers_group.members + areachairs_group.members
    print('replacing members with IDs')
    openreview.tools.replace_members_with_ids(client, reviewers_group)
    openreview.tools.replace_members_with_ids(client, areachairs_group)
    groups.update_homepage(client, '../webfield/homepagePostSubmission.js')

    # User registration.

    '''
    This is a workaround to resolve the issue where not all reviewers/ACs
    see the AKBC venue in their "your active venues" list.

    Notice that we're falsifying the tauthor. This is so that the query
    in home.js (copied below) will pick up the note as a reply,
    but the note won't show up in the user's activity.

    home.js, Line 67:
    controller.get('invitations', { invitee: true, duedate: true, details: 'replytoNote,repliedNotes' })
    '''
    register_user_inv = client.post_invitation(conferenceConfig.register_user_inv)
    for email in all_emails:
        print('posting registration note for {}'.format(email))
        register_note = client.post_note(openreview.Note.from_json({
            'invitation': register_user_inv.id,
            'forum': None,
            'replyto': None,
            'readers': register_user_inv.reply['readers']['values'],
            'writers': register_user_inv.reply['writers']['values'],
            'signatures': register_user_inv.reply['signatures']['values'],
            'content': {'registered': 'yes'},
            'tauthor': email
        }))
