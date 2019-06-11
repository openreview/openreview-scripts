def process(client, note, invitation):
    conference = openreview.helpers.get_conference(client, note.forum)
    print('Conference: ', conference.get_id())
    note.content['invitation_email_subject'] = note.content['invitation_email_subject'].replace('{Abbreviated_Venue_Name}', conference.get_short_name())
    note.content['invitation_email_content'] = note.content['invitation_email_content'].replace('{Abbreviated_Venue_Name}', conference.get_short_name())
    note = client.post_note(note)
    area_chair_names_str = note.content.get('area_chair_names', None)
    area_chair_names = [s.strip() for s in area_chair_names_str.split(',')] if area_chair_names_str else []
    conference.recruit_reviewers(
        reviewers_name = 'Area_Chairs',
        emails = [s.strip() for s in note.content['area_chair_emails'].split(',')],
        title = note.content['invitation_email_subject'].strip(),
        message = note.content['invitation_email_content'].strip(),
        invitee_names = area_chair_names
    )