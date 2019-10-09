def process(client, note, invitation):
    SHORT_PHRASE = "NeurIPS Reproducibility Challenge"
    # get all notification tags for this paper
    notify_inv = invitation.id.replace('Comment', 'Comment_Notification')
    # TODO change to iterget
    notifications = client.get_tags(invitation=notify_inv)

    email_list = []
    all_notifiers = []
    for tag in notifications:
        if tag.tag == 'Immediate':
            email_list.append(tag.signatures[0])
        all_notifiers.append(tag.signatures[0])

    # get submission author and add to email list if author hasn't set a notification tag
    forumNote = client.get_note(id=note.forum)

    if email_list:
        # send email to those in the immediate notification group
        subject = '[' + SHORT_PHRASE + '] Paper Title: "' + forumNote.content['title'] + '" received a comment'
        formatted_msg = 'The NeurIPS submission titled "' + forumNote.content['title'] + '" has received a comment.\n\nComment title: ' \
                        + note.content['title'] + '\n\nComment: ' + note.content['comment'] + '\n\nTo view the comment, click here: ' + \
                        client.baseurl + '/forum?id=' + note.forum + '&noteId=' + note.id + '\n\nIf you do not wish to receive notifications for comments on this paper, visit the link above and change the Notification frequency.'

        response = client.send_mail(subject, email_list, formatted_msg)

    # if comment author doesn't have notifications set up,
    # send email on how to set notifications
    if note.signatures[0] not in all_notifiers:
        print("comment author needs instructions")
        subject = '[' + SHORT_PHRASE + '] Paper Title: "' + forumNote.content['title'] + '" received your comment'
        message = "If you wish to receive email when people comment on this paper, go to "+client.baseurl + '/forum?id=' + note.forum + \
            " and select the Comment Notification frequency."
        response = client.send_mail(subject, [note.signatures[0]], message)