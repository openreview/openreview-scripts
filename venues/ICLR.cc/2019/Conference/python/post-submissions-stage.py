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

    original_notes = openreview.tools.iterget_notes(client,invitation = iclr19.submission_inv.id)

    for original_note in original_notes:
        blind_note = client.post_note( notes.create_blind_note(original_note) )

        # create paper and paper-author group

        # paper_group = groups.create_paper_group(blind_note)
        # author_group = groups.create_paper_author_group(blind_note)

        paper_group_id = iclr19.CONFERENCE_ID + "/Paper{0}".format(blind_note.number)
        paper_group = openreview.Group(
            id = paper_group_id,
            signatures = [iclr19.CONFERENCE_ID],
            writers = [iclr19.CONFERENCE_ID],
            members = [],
            readers = [iclr19.CONFERENCE_ID],
            signatories = [paper_group_id]
        )
        author_group_id = iclr19.CONFERENCE_ID + "/Paper{0}/Authors".format(blind_note.number)
        author_group = openreview.Group(
            id = author_group_id,
            signatures = [iclr19.CONFERENCE_ID],
            writers = [iclr19.CONFERENCE_ID],
            members = original_note.content['authorids'] + original_note.signatures,
            readers = [iclr19.CONFERENCE_ID, iclr19.PROGRAM_CHAIRS_ID, author_group_id],
            signatories = [author_group_id]
        )
        client.post_group(paper_group).id
        client.post_group(author_group).id


        # Update Blind note's contents, repost the updated blind note, and freeze and post the original note
        blind_note.content["authorids"] = [author_group.id]
        blind_note.content["_bibtex"] = notes.getBibtex(client, blind_note)

        client.post_note(blind_note)

        client.post_note(notes.freeze_note(original_note))

    # conference_group = client.get_group(iclr19.CONFERENCE_ID)
    # conference_group = groups.update_webfield(
    #     conference_group, '../webfield/post-submission-stage-homepage.js')
    # conference_group = client.post_group(conference_group)

