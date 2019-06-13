def process(client, note, invitation):
    import datetime
    conference = openreview.helpers.get_conference(client, note.forum)
    forum_note = client.get_note(note.forum)
    invitation_type = invitation.id.split('/')[-1]
    if conference.submission_stage.double_blind and invitation_type in ['Review_Stage', 'Meta_Review_Stage', 'Decision_Stage']:
        conference.create_blind_submissions()
        conference.set_authors()

        if invitation_type == 'Review_Stage':
            review_due_date = None
            try:
                review_due_date = datetime.datetime.strptime(forum_note.content.get('Review Deadline', None), '%Y/%m/%d %H:%M')
            except ValueError:
                review_due_date = datetime.datetime.strptime(forum_note.content.get('Review Deadline', None), '%Y/%m/%d')

            review_start_date = None

            if forum_note.content.get('Review Start Date', None):
                try:
                    review_start_date = datetime.datetime.strptime(forum_note.content.get('Review Start Date', None), '%Y/%m/%d %H:%M')
                except ValueError:
                    review_start_date = datetime.datetime.strptime(forum_note.content.get('Review Start Date', None), '%Y/%m/%d')

            review_additional_fields = forum_note.content.get('Additional Review Options', {})
            if review_additional_fields:
                review_additional_fields = json.loads(review_additional_fields)

            conference.set_review_stage(openreview.ReviewStage(start_date = review_start_date, due_date = review_due_date, allow_de_anonymization = forum_note.content.get('Author and Reviewer Anonymity', None), public = (forum_note.content.get('Open Reviewing Policy', None) == 'Submissions and reviews should both be public.'), release_to_authors = (forum_note.content.get('Release Reviews to Authors', False) == 'Yes'), release_to_reviewers = (forum_note.content.get('Release Reviews to Reviewers', False) == 'Yes'), email_pcs = (forum_note.content.get('Email Program Chairs about Reviews', False) == 'Yes'), additional_fields = review_additional_fields))

        elif invitation_type == 'Meta_Review_Stage':
            meta_review_due_date = None
            try:
                meta_review_due_date = datetime.datetime.strptime(forum_note.content.get('Meta Review Deadline', None), '%Y/%m/%d %H:%M')
            except ValueError:
                meta_review_due_date = datetime.datetime.strptime(forum_note.content.get('Meta Review Deadline', None), '%Y/%m/%d')

            meta_review_start_date = None
            if forum_note.content.get('Meta Review Start Date', None):
                try:
                    meta_review_start_date = datetime.datetime.strptime(forum_note.content.get('Meta Review Start Date', None), '%Y/%m/%d %H:%M')
                except ValueError:
                    meta_review_start_date = datetime.datetime.strptime(forum_note.content.get('Meta Review Start Date', None), '%Y/%m/%d')

            meta_review_due_date = None

            meta_review_additional_fields = forum_note.content.get('Additional Meta Review Options', {})
            if meta_review_additional_fields:
                meta_review_additional_fields = json.loads(meta_review_additional_fields)

            conference.set_meta_review_stage(openreview.MetaReviewStage(start_date = meta_review_start_date, due_date = meta_review_due_date, public = (forum_note.content.get('Make Meta Reviews Public', None) == 'Yes'), additional_fields = meta_review_additional_fields))

        elif invitation_type == 'Decision_Stage':
            decision_due_date = None
            try:
                decision_due_date = datetime.datetime.strptime(forum_note.content.get('Decision Deadline', None), '%Y/%m/%d %H:%M')
            except ValueError:
                decision_due_date = datetime.datetime.strptime(forum_note.content.get('Decision Deadline', None), '%Y/%m/%d')

            decision_start_date = None
            if forum_note.content.get('Decision Start Date', None):
                try:
                    decision_start_date = datetime.datetime.strptime(forum_note.content.get('Decision Start Date', None), '%Y/%m/%d %H:%M')
                except ValueError:
                    decision_start_date = datetime.datetime.strptime(forum_note.content.get('Decision Start Date', None), '%Y/%m/%d')

            decision_options = forum_note.content.get('Decision Options', None)
            if decision_options:
                decision_options = [s.translate(str.maketrans('', '', ' "\'')) for s in decision_options.split(',')]
                conference.set_decision_stage(openreview.DecisionStage(options = decision_options, start_date = decision_start_date, due_date = decision_due_date, public = (forum_note.content.get('Make Decisions Public', None) == 'Yes'), release_to_authors = (forum_note.content.get('Release Decisions to Authors', None) == 'Yes'), release_to_reviewers = (forum_note.content.get('Release Decisions to Reviewers', None) == 'Yes')))
            else:
                conference.set_decision_stage(openreview.DecisionStage(start_date = decision_start_date, due_date = decision_due_date, public = (forum_note.content.get('Make Decisions Public', None) == 'Yes')))
        else:
            raise openreview.OpenReviewException('Invitation not found!!')

    print('Conference: ', conference.get_id())