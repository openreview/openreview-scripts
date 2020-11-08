def process_update(client, note, invitation, existing_note):
    CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'
    SHORT_PHRASE = "ML Reproducibility Challenge 2020"
    NOTIFICATION_SUBSCRIPTION_ID = CONFERENCE_ID + '/-/Notification_Subscription'

    action = 'posted'
    if existing_note:
        action = 'deleted' if note.ddate else 'updated'

    if action == 'posted':

        # get all notification tags for this paper
        notifications = client.get_tags(forum=note.forum, invitation=NOTIFICATION_SUBSCRIPTION_ID)

        email_list = [tag.signatures[0] for tag in notifications if tag.tag == 'Subscribe']
        all_notifiers = [tag.signatures[0] for tag in notifications]

        # get submission author and add to email list if author hasn't set a notification tag
        forumNote = client.get_note(id=note.forum)

        if email_list:
            # send email to those in the immediate notification group
            subject = '[' + SHORT_PHRASE + '] Paper Title: "' + forumNote.content['title'] + '" received a claim'
            formatted_msg = 'The ' + SHORT_PHRASE + ' submission titled "' + forumNote.content[
                'title'] + '" has received a claim.\n\nComment title: ' \
                            + note.content['title'] + '\n\nTo view the claim, click here: ' + \
                            client.baseurl + '/forum?id=' + note.forum + '&noteId=' + note.id + '\n\nIf you wish to change your email notification preferences for comments on this paper, log into OpenReview.net, visit the link above and change the Notification Subscription frequency.'

            print("formatted_msg:", formatted_msg)
            client.post_message(subject, email_list, formatted_msg, ignoreRecipients=[note.tauthor])

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

        to_send = [note.tauthor]
        if note.content['team_emails'] is not None:
            to_send.extend(note.content['team_emails'])

        client.post_message("ML Reproducibility Challenge 2020 Claim", to_send, msg)

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
