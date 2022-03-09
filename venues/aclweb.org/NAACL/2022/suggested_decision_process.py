def process(client, note, invitation):
    from datetime import datetime
    
    
    forum_note = client.get_note(note.forum)
    CONFERENCE_ID = 'aclweb.org/NAACL/2022/Conference'
    CONFERENCE_SHORT_NAME = 'NAACL 2022 Conference'
    
    
    email_subject = f'{CONFERENCE_SHORT_NAME}: A suggested decision has been posted to a paper in your area'
    email_body = f'A suggested decision has been posted to Paper {forum_note.number} in {CONFERENCE_SHORT_NAME} track {forum_note.content["track"]}. \n\nSuggested decision: {note.content["suggested_decision"]}\n\nView it here: https://openreview.net/forum?id={note.forum}&noteId={note.id}'
    client.post_message(subject=email_subject, recipients=note.readers, message=email_body, ignoreRecipients=note.nonreaders)
