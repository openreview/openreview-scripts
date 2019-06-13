def process(client, note, invitation):
    conference = openreview.helpers.get_conference(client, note.forum)
    if conference.submission_stage.double_blind and invitation.id.split('/')[-1] in ['Review_Stage', 'Meta_Review_Stage', 'Decision_Stage']:
        conference.create_blind_submissions()
        conference.set_authors()
    print('Conference: ', conference.get_id())