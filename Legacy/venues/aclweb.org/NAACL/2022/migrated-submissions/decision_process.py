def process(client, note, invitation):
    from datetime import datetime
    CONFERENCE_ID = 'aclweb.org/NAACL/2022/Conference'
    CONFERENCE_SHORT_NAME = 'NAACL 2022 Conference'
    #DESK_REJECTED_SUBMISSION_ID = 'aclweb.org/ACL/2022/Conference/-/Desk_Rejected_Submission'

    forum_note = client.get_note(note.forum)
    
   

    # Mail to the submission readers
    email_subject = '''{CONFERENCE_SHORT_NAME}: Decision posted to Commitment #{paper_number} titled "{paper_title}" by program chairs'''.format(
        CONFERENCE_SHORT_NAME=CONFERENCE_SHORT_NAME,
        paper_number=forum_note.number,
        paper_title=forum_note.content['title']
        
    )
    email_body = f'A decision was posted to Commitment #{forum_note.number} titled "{forum_note.content["title"]}"".\n\n Decision: {note.content["decision"]}.\n\nView it here: https://openreview.net/forum?id={forum_note.forum}&noteId={note.id}'

    

    recipients = note.readers
    client.post_message(subject=email_subject, recipients=recipients, message=email_body, ignoreRecipients=note.nonreaders)

   