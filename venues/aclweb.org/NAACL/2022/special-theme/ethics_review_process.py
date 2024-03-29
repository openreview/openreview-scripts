def process(client, note, invitation):
    from datetime import datetime
    CONFERENCE_ID = 'aclweb.org/NAACL/2022/Conference'
    CONFERENCE_SHORT_NAME = 'NAACL 2022 Conference'
    

    forum_note = client.get_note(note.forum)

    # Mail to the submission readers
    email_subject = '''{CONFERENCE_SHORT_NAME}: Ethics Review Posted to Paper #{paper_number} titled "{paper_title}"'''.format(
        CONFERENCE_SHORT_NAME=CONFERENCE_SHORT_NAME,
        paper_number=forum_note.number,
        paper_title=forum_note.content['title']
    )
    email_body = f'An ethics review was posted to Paper #{forum_note.number} titled "{forum_note.content["title"]}":\n\nRecommendation: {note.content["recommendation"]}\n\nJustification: {note.content["ethics_review"]}'

    

    recipients = note.readers
    
    client.post_message(subject=email_subject, recipients=recipients, message=email_body, ignoreRecipients=note.nonreaders)
