import openreview
import iclr19
import notes
import groups
import invitations

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('invitations', nargs='*', help="any of the following: " + ", ".join(invitation_templates.keys()))
    parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    client.post_invitation(iclr19.blind_submission_inv)

    original_notes = openreview.tools.iterget_notes(client,invitation = iclr19.submission_inv.id)

    for original_note in original_notes:
        blind_note = notes.create_blind_note(original_note)

        #create paper and paper-author group
        paper_group = groups.create_paper_group(blind_note)
        author_group = groups.create_paper_author_group(blind_note)

        blind_note.content["authorids"] = [author_group.id]
        blind_note.content["_bibtex"] = notes.getBibtex(blind_note)

        client.post_note(blind_note)

        client.post_note(notes.freeze_note(original_note))

    conference_group = client.get_group(iclr19.CONFERENCE_ID)
    conference_group = groups.update_webfield(
        conference_group, '../webfield/post-submission-stage-homepage.js')
    conference_group = client.post_group(conference_group)

