def process(client, note, invitation):
    SHORT_PHRASE = "NeurIPS Reproducibility Challenge"
    # get all notification tags for this paper
    notify_inv = invitation.id.replace('Comment', 'Notification_Subscription')
    # TODO change to iterget
    notifications = client.get_tags(invitation=notify_inv)

    email_list = [tag.signatures[0] for tag in notifications if tag.tag == 'Immediate']
    all_notifiers = [tag.signatures[0] for tag in notifications]

    # get submission author and add to email list if author hasn't set a notification tag
    forumNote = client.get_note(id=note.forum)

    # add comment author to email list if does not have a tag
    if note.signatures[0] and note.signatures[0] not in all_notifiers:
        email_list.append[note.signatures[0]]

    if email_list:
        # send email to those in the immediate notification group
        subject = '[' + SHORT_PHRASE + '] Paper Title: "' + forumNote.content['title'] + '" received a comment'
        formatted_msg = 'The NeurIPS submission titled "' + forumNote.content['title'] + '" has received a comment.\n\nComment title: ' \
                        + note.content['title'] + '\n\nComment: ' + note.content['comment'] + '\n\nTo view the comment, click here: ' + \
                        client.baseurl + '/forum?id=' + note.forum + '&noteId=' + note.id + '\n\nIf you wish to change your email notification preferences for comments on this paper, log into OpenReview.net, visit the link above and change the Notification Subscription frequency.'

        response = client.send_mail(subject, email_list, formatted_msg)
