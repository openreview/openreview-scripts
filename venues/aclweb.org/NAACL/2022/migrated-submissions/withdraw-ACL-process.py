def process(client, note, invitation):
    from datetime import datetime
    CONFERENCE_ID = 'aclweb.org/NAACL/2022/Conference'
    CONFERENCE_SHORT_NAME = 'NAACL 2022 Conference'
    WITHDRAWN_SUBMISSION_ID = 'aclweb.org/NAACL/2022/Conference/-/Withdrawn_Commitment_Submission'

    forum_note = client.get_note(note.forum)
    forum_note.invitation = WITHDRAWN_SUBMISSION_ID
    
    if len(forum_note.readers) == 1: 
        content = {}
        keep_keys = ['title', 'pdf', 'abstract','paper_link','paper_type']
        for key in forum_note.content: 
            if key not in keep_keys:
                content[key] = ''
        forum_note.content = content
    else:
        forum_note.content = {
        'authors': forum_note.content['authors'],
        'authorids': forum_note.content['authorids'],
        'country_of_affiliation_of_corresponding_author': ''
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

    PAPER_AUTHORS_ID = f'aclweb.org/NAACL/2022/Conference/Commitment{forum_note.number}/Authors'

    recipients = note.readers
    recipients.append(PAPER_AUTHORS_ID)
    client.post_message(subject=email_subject, recipients=recipients, message=email_body, ignoreRecipients=note.nonreaders)
