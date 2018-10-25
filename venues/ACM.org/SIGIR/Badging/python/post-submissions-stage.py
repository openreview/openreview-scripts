'''
Post-submission Stage 2 (Nov 17 - )

- Public Commentary is enabled. Comment rules:
- - Members of the public may comment with their public ID (e.g. ~Michael_Spector1)
- - Readership of comments can be set to a subset of the following groups: [ Everyone, Paper Reviewers, Paper Authors, Chairs ]

'''

import openreview
import acm19 as conference_config
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
        print('processing {}'.format(original.id))

        groups.create_and_post(client, original, 'Paper')
        author_group = groups.create_and_post(client, original, 'Paper/Authors', members=original.content['authorids'])

        original.readers = [
            conference_config.CONFERENCE_ID,
            author_group.id
        ]
        client.post_note(original)

        invitations.enable_and_post(client, original, 'Public_Comment')
        invitations.enable_and_post(client, original, 'Official_Comment')
        invitations.enable_and_post(client, original, 'Withdraw_Submission')

    reviewers_group = client.get_group(conference_config.REVIEWERS_ID)
    chairs_group = client.get_group(conference_config.CHAIRS_ID)
    
    print('replacing members with IDs')
    openreview.tools.replace_members_with_ids(client, reviewers_group)
    openreview.tools.replace_members_with_ids(client, chairs_group)
    groups.update_homepage(client, '../webfield/homepagePostSubmission.js')
