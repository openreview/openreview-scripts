def process(client, note, invitation):
    CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'
    # create and post claim_hold note
    hold_invite_id = invitation.id.replace('Claim', 'Claim_Hold')
    client.post_note(openreview.Note(
        id=None,
        original=None,
        invitation=hold_invite_id,
        forum=note.forum,
        signatures=[CONFERENCE_ID],
        writers=[CONFERENCE_ID],
        readers=['everyone'],
        content={"title": "Claimed by "+ note.content['institution']}
        ))

    # send confirmation email
    submission = client.get_note(note.forum)
    msg = 'Your claim to ML Reproducibility Challenge 2020 Reproducibility Challenge for paper {title} has been posted.'.format(
        title=submission.content['title'])
    client.send_mail("ML Reproducibility Challenge 2020 Claim", [note.tauthor], msg)

    claimants = client.get_group(CONFERENCE_ID + '/Claimants')
    claimants.members.append(note.tauthor)
    client.post_group(claimants)
