def process(client, note, invitation):
    import datetime
    conference = openreview.helpers.get_conference(client, note.forum)
    forum_note = client.get_note(note.forum)
    invitation_type = invitation.id.split('/')[-1]
    if conference.submission_stage.double_blind and (invitation_type in ['Bid_Stage', 'Review_Stage', 'Meta_Review_Stage', 'Decision_Stage']):
        conference.create_blind_submissions()
        conference.set_authors()

    if invitation_type == 'Bid_Stage':
        bid_due_date = None
        if forum_note.content.get('bid_due_date', None):
            try:
                bid_due_date = datetime.datetime.strptime(forum_note.content.get('bid_due_date'), '%Y/%m/%d %H:%M')
            except ValueError:
                bid_due_date = datetime.datetime.strptime(forum_note.content.get('bid_due_date'), '%Y/%m/%d')

        bid_start_date = None
        if forum_note.content.get('bid_start_date', None):
            try:
                bid_start_date = datetime.datetime.strptime(forum_note.content.get('bid_start_date', None), '%Y/%m/%d %H:%M')
            except ValueError:
                bid_start_date = datetime.datetime.strptime(forum_note.content.get('bid_start_date', None), '%Y/%m/%d')

        conference.set_bid_stage(openreview.BidStage(start_date = bid_start_date, due_date = bid_due_date, request_count = forum_note.content.get('bid_count', 50)))

    elif invitation_type == 'Review_Stage':
        review_due_date = None
        if forum_note.content.get('review_deadline', None):
            try:
                review_due_date = datetime.datetime.strptime(forum_note.content.get('review_deadline', None), '%Y/%m/%d %H:%M')
            except ValueError:
                review_due_date = datetime.datetime.strptime(forum_note.content.get('review_deadline', None), '%Y/%m/%d')

        review_start_date = None
        if forum_note.content.get('review_start_date', None):
            try:
                review_start_date = datetime.datetime.strptime(forum_note.content.get('review_start_date', None), '%Y/%m/%d %H:%M')
            except ValueError:
                review_start_date = datetime.datetime.strptime(forum_note.content.get('review_start_date', None), '%Y/%m/%d')

        review_additional_fields = forum_note.content.get('additional_review_options', {})
        if review_additional_fields:
            review_additional_fields = json.loads(review_additional_fields)

        conference.set_review_stage(openreview.ReviewStage(start_date = review_start_date, due_date = review_due_date, allow_de_anonymization = (forum_note.content.get('Author and Reviewer Anonymity', None) == 'No anonymity'), public = (forum_note.content.get('Open Reviewing Policy', None) == 'Submissions and reviews should both be public.'), release_to_authors = (forum_note.content.get('release_reviews_to_authors', False) == 'Yes'), release_to_reviewers = (forum_note.content.get('release_reviews_to_reviewers', False) == 'Yes'), email_pcs = (forum_note.content.get('email_program_Chairs_about_reviews', False) == 'Yes'), additional_fields = review_additional_fields))

    elif invitation_type == 'Meta_Review_Stage':
        meta_review_due_date = None
        if forum_note.content.get('meta_review_deadline', None):
            try:
                meta_review_due_date = datetime.datetime.strptime(forum_note.content.get('meta_review_deadline', None), '%Y/%m/%d %H:%M')
            except ValueError:
                meta_review_due_date = datetime.datetime.strptime(forum_note.content.get('meta_review_deadline', None), '%Y/%m/%d')

        meta_review_start_date = None
        if forum_note.content.get('meta_review_start_date', None):
            try:
                meta_review_start_date = datetime.datetime.strptime(forum_note.content.get('meta_review_start_date', None), '%Y/%m/%d %H:%M')
            except ValueError:
                meta_review_start_date = datetime.datetime.strptime(forum_note.content.get('meta_review_start_date', None), '%Y/%m/%d')

        meta_review_additional_fields = forum_note.content.get('additional_meta_review_options', {})
        if meta_review_additional_fields:
            meta_review_additional_fields = json.loads(meta_review_additional_fields)

        conference.set_meta_review_stage(openreview.MetaReviewStage(start_date = meta_review_start_date, due_date = meta_review_due_date, public = (forum_note.content.get('make_meta_reviews_public', None) == 'Yes'), additional_fields = meta_review_additional_fields))

    elif invitation_type == 'Decision_Stage':
        decision_due_date = None
        if forum_note.content.get('decision_deadline', None):
            try:
                decision_due_date = datetime.datetime.strptime(forum_note.content.get('decision_deadline', None), '%Y/%m/%d %H:%M')
            except ValueError:
                decision_due_date = datetime.datetime.strptime(forum_note.content.get('decision_deadline', None), '%Y/%m/%d')

        decision_start_date = None
        if forum_note.content.get('decision_start_date', None):
            try:
                decision_start_date = datetime.datetime.strptime(forum_note.content.get('decision_start_date', None), '%Y/%m/%d %H:%M')
            except ValueError:
                decision_start_date = datetime.datetime.strptime(forum_note.content.get('decision_start_date', None), '%Y/%m/%d')

        decision_options = forum_note.content.get('decision_options', None)
        if decision_options:
            decision_options = [s.translate(str.maketrans('', '', ' "\'')) for s in decision_options.split(',')]
            conference.set_decision_stage(openreview.DecisionStage(options = decision_options, start_date = decision_start_date, due_date = decision_due_date, public = (forum_note.content.get('make_decisions_public', None) == 'Yes'), release_to_authors = (forum_note.content.get('release_decisions_to_authors', None) == 'Yes'), release_to_reviewers = (forum_note.content.get('release_decisions_to_reviewers', None) == 'Yes')))
        else:
            conference.set_decision_stage(openreview.DecisionStage(start_date = decision_start_date, due_date = decision_due_date, public = (forum_note.content.get('make_decisions_public', None) == 'Yes')))

    print('Conference: ', conference.get_id())