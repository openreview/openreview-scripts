def process(client, note, invitation):
    SHORT_PHRASE = "ML Reproducibility Challenge 2020"
    CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'
    NOTIFICATION_SUBSCRIPTION_ID = CONFERENCE_ID + '/-/Notification_Subscription'
    # get all notification tags for this paper
    notifications = client.get_tags(forum=note.forum, invitation=NOTIFICATION_SUBSCRIPTION_ID)

# TODO check for subscribe instead
    email_list = [tag.signatures[0] for tag in notifications if tag.tag == 'Subscribe']
    all_notifiers = [tag.signatures[0] for tag in notifications]

    # get submission author and add to email list if author hasn't set a notification tag
    forumNote = client.get_note(id=note.forum)

    # add comment author to email list if does not have a tag
    if note.signatures[0] and note.signatures[0] not in all_notifiers:
        email_list.append(note.signatures[0])

    if email_list:
        # send email to those in the immediate notification group
        subject = '[' + SHORT_PHRASE + '] Paper Title: "' + forumNote.content['title'] + '" received a comment'
        formatted_msg = 'The ' + SHORT_PHRASE + ' submission titled "' + forumNote.content['title'] + '" has received a comment.\n\nComment title: ' \
                        + note.content['title'] + '\n\nComment: ' + note.content['comment'] + '\n\nTo view the comment, click here: ' + \
                        client.baseurl + '/forum?id=' + note.forum + '&noteId=' + note.id + '\n\nIf you wish to change your email notification preferences for comments on this paper, log into OpenReview.net, visit the link above and change the Notification Subscription frequency.'

        client.send_mail(subject, email_list, formatted_msg)
