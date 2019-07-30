def process(client, note, invitation):
    import datetime
    conference = openreview.helpers.get_conference(client, note.forum)
    forum_note = client.get_note(note.forum)
    invitation_type = invitation.id.split('/')[-1]
    if invitation_type in ['Bid_Stage', 'Review_Stage', 'Meta_Review_Stage', 'Decision_Stage']:
        if conference.submission_stage.double_blind:
            conference.create_blind_submissions()
        conference.set_authors()
        conference.set_reviewers()
        if conference.use_area_chairs:
            conference.set_area_chairs(enable_reviewer_reassignment = True if "OpenReview Affinity" in forum_note.content.get("Paper Matching", []) else False)
        conference.set_program_chairs(enable_reviewer_reassignment = True if "OpenReview Affinity" in forum_note.content.get("Paper Matching", []) else False)

    if invitation_type == 'Bid_Stage':
        conference.set_bid_stage(openreview.helpers.get_bid_stage(client, forum_note))

    elif invitation_type == 'Review_Stage':
        conference.set_review_stage(openreview.helpers.get_review_stage(client, forum_note))

    elif invitation_type == 'Meta_Review_Stage':
        conference.set_meta_review_stage(openreview.helpers.get_meta_review_stage(client, forum_note))

    elif invitation_type == 'Decision_Stage':
        conference.set_decision_stage(openreview.helpers.get_decision_stage(client, forum_note))

    print('Conference: ', conference.get_id())