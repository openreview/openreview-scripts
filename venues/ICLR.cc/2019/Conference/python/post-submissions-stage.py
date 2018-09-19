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
    groups.post_paper_groups(client, blind_notes)
    groups.post_paper_author_groups(client, blind_notes)
    notes.freeze_notes(client, original_notes)

    # groups.create_reviewer_groups(client, blind_notes)
    # groups.create_areachair_groups(client, blind_notes)





    # conference_group = client.get_group(iclr19.CONFERENCE_ID)
    # conference_group = groups.update_webfield(
    #     conference_group, '../webfield/post-submission-stage-homepage.js')
    # conference_group = client.post_group(conference_group)

