def process(client, note, invitation):
    from datetime import datetime
    CONFERENCE_SHORT_NAME = ''
    WITHDRAWN_SUBMISSION_ID = ''

    forum_note = client.get_note(note.forum)
    forum_note.invitation = WITHDRAWN_SUBMISSION_ID
    
    
    
    forum_note.content = {
    'authors': forum_note.content['authors'],
    'authorids': forum_note.content['authorids']
    }
    forum_note = client.post_note(forum_note)


    # Mail to the submission readers
    email_subject = '''{CONFERENCE_SHORT_NAME}: Paper #{paper_number} titled "{paper_title}" withdrawn by authors'''.format(
        CONFERENCE_SHORT_NAME=CONFERENCE_SHORT_NAME,
        paper_number=forum_note.number,
        paper_title=forum_note.content['title']
    )
    email_body = '''The {CONFERENCE_SHORT_NAME} paper "{paper_title_or_num}" has been withdrawn by the paper authors.'''.format(
        CONFERENCE_SHORT_NAME=CONFERENCE_SHORT_NAME,
        paper_title_or_num=forum_note.content.get('title', '#'+str(forum_note.number))
    )

    PAPER_AUTHORS_ID = ''

    recipients = note.readers
    recipients.append(PAPER_AUTHORS_ID)
    client.post_message(subject=email_subject, recipients=recipients, message=email_body, ignoreRecipients=note.nonreaders)
