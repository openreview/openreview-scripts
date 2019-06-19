def process(client, note, invitation):
    import datetime
    conference = openreview.helpers.get_conference(client, note.forum)
    forum_note = client.get_note(note.forum)
    invitation_type = invitation.id.split('/')[-1]
    if invitation_type in ['Bid_Stage', 'Review_Stage', 'Meta_Review_Stage', 'Decision_Stage']:
        if conference.submission_stage.double_blind:
            conference.create_blind_submissions()
        conference.set_authors()

    if invitation_type == 'Bid_Stage':
        conference.set_bid_stage(openreview.helpers.get_bid_stage(client, note.forum))

    elif invitation_type == 'Review_Stage':
        conference.set_review_stage(openreview.helpers.get_review_stage(client, note.forum))

    elif invitation_type == 'Meta_Review_Stage':
        conference.set_meta_review_stage(openreview.helpers.get_meta_review_stage(client, note.forum))

    elif invitation_type == 'Decision_Stage':
        conference.set_decision_stage(openreview.helpers.get_decision_stage(client, note.forum))

    print('Conference: ', conference.get_id())