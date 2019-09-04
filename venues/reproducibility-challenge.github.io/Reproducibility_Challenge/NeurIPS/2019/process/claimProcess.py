def process(client, note, invitation):
    conference_id = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'
    # create and post claim_hold note
    hold_invite_id = invitation.id.replace('Claim', 'Claim_Hold')
    client.post_note(openreview.Note(
        id=None,
        original=None,
        invitation=hold_invite_id,
        forum=note.forum,
        signatures=[conference_id],
        writers=[conference_id],
        readers=['everyone'],
        content={"title": "Claimed by "+ note.content['institution']}
        ))

    # send confirmation email
    submission = client.get_note(note.forum)
    msg = 'Your claim to NeurIPS 2019 Reproducibility Challenge for paper {title} has been posted.'.format(
        title=submission.content['title'])
    client.send_mail("NeurIPS Reproducibility Claim", [note.tauthor], msg)

    claimants = client.get_group(conference_id+'/Claimants')
    claimants.members.append(note.tauthor)
    client.post_group(claimants)
