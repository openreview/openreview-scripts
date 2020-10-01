def process_update(client, note, invitation, existing_note):
    CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'

    action = 'posted'
    if existing_note:
        action = 'deleted' if note.ddate else 'updated'

    if action == 'posted':
        # create and post claim_hold note
        hold_invite_id = invitation.id.replace('Claim', 'Claim_Hold')
        client.post_note(openreview.Note(
            id=None,
            original=note.id,
            invitation=hold_invite_id,
            forum=note.forum,
            signatures=[CONFERENCE_ID],
            writers=[CONFERENCE_ID],
            readers=['everyone'],
            content={
                "title": "Claimed",
                "plan": "",
                "team_members": "",
                "team_emails": ""
            }
            ))

        # send confirmation email
        submission = client.get_note(note.forum)
        msg = 'Your claim to ML Reproducibility Challenge 2020 for paper {title} has been posted.'.format(
            title=submission.content['title']) + '\n\nTo view the claim, click here: ' + \
                            client.baseurl + '/forum?id=' + note.forum + '&noteId=' + note.id
        client.send_mail("ML Reproducibility Challenge 2020 Claim", [note.tauthor], msg)

        claimants = client.get_group(CONFERENCE_ID + '/Claimants')
        claimants.members.append(note.tauthor)
        client.post_group(claimants)

    # if action == 'deleted':
    #     claim_hold_notes = client.get_notes(original=note.id)
    #     if claim_hold_notes:
    #         ## delete note
    #         note = claim_hold_notes[0]
    #         note.ddate = now()
    #         client.post_note(note)
