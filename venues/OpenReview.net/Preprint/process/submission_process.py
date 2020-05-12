def process_update(client, note, invitation, existing_note):

    author_subject = 'OpenReview Preprint has received your submission titled ' + note.content['title']
    action = 'posted'
    if existing_note:
        action = 'deleted' if note.ddate else 'updated'

    author_message = '''Your submission to OpenReview Preprint Server has been {action}.

Submission Number: {number}
Title: {title}
To view your submission, click here: https://openreview.net/forum?id={forum}

'''.format(action=action, number=note.number, title=note.content['title'], forum=note.forum)

    coauthor_message = author_message + '\n\nIf you are not an author of this submission and would like to be removed, please contact the author who added you at {tauthor}'.format(tauthor=note.tauthor)

    client.post_message(subject=author_subject,
        recipients=[note.tauthor],
        message=author_message,
        ignoreRecipients=None,
        sender=None
    )

    client.post_message(subject=author_subject,
        recipients=note.content['authorids'],
        message=coauthor_message,
        ignoreRecipients=[note.tauthor],
        sender=None
    )

