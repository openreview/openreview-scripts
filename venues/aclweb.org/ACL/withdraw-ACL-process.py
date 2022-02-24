def process(client, note, invitation):
    from datetime import datetime
    CONFERENCE_ID = 'aclweb.org/ACL/2022/Conference'
    CONFERENCE_SHORT_NAME = 'ACL 2022 Conference'
    WITHDRAWN_SUBMISSION_ID = 'aclweb.org/ACL/2022/Conference/-/Withdrawn_Submission'

    forum_note = client.get_note(note.forum)
    forum_note.invitation = WITHDRAWN_SUBMISSION_ID
    forum_note.content = {
        'authors': forum_note.content['authors'],
        'authorids': forum_note.content['authorids']
    }
    forum_note = client.post_note(forum_note)

    # Expire available invitations
    invitation_regex = CONFERENCE_ID + '/Paper' + str(forum_note.number) + '/-/.*'
    all_paper_invitations = openreview.tools.iterget_invitations(client, regex=invitation_regex)
    now = openreview.tools.datetime_millis(datetime.utcnow())
    for invitation in all_paper_invitations:
        invitation.expdate = now
        client.post_invitation(invitation)

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

    PAPER_AUTHORS_ID = f'aclweb.org/ACL/2022/Conference/Paper{forum_note.number}/Authors'

    recipients = note.readers
    recipients.append(PAPER_AUTHORS_ID)
    client.post_message(subject=email_subject, recipients=recipients, message=email_body, ignoreRecipients=note.nonreaders)
