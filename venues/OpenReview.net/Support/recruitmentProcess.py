def process(client, note, invitation):
    conference = openreview.helpers.get_conference(client, note.forum)
    print('Conference: ', conference.get_id())

    note.content['invitation_email_subject'] = note.content['invitation_email_subject'].replace('{Abbreviated_Venue_Name}', conference.get_short_name())
    note.content['invitation_email_subject'] = note.content['invitation_email_subject'].replace('{invitee_role}', note.content.get('invitee_role', 'reviewer'))

    note.content['invitation_email_content'] = note.content['invitation_email_content'].replace('{Abbreviated_Venue_Name}', conference.get_short_name())
    note.content['invitation_email_content'] = note.content['invitation_email_content'].replace('{invitee_role}', note.content.get('invitee_role', 'reviewer'))

    note = client.post_note(note)
    invitee_names_str = note.content.get('invitee_names', None)
    invitee_names = [s.strip() for s in invitee_names_str.split(',')] if invitee_names_str else []
    conference.recruit_reviewers(
        emails = [s.strip() for s in note.content['invitee_emails'].split(',')],
        title = note.content['invitation_email_subject'].strip(),
        message = note.content['invitation_email_content'].strip(),
        invitee_names = invitee_names
    )