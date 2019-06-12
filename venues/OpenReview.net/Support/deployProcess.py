def process(client, note, invitation):
    print('client:', client.baseurl)
    print('note:', note.id)
    print('invitation:', invitation.id)
    conference = openreview.helpers.get_conference(client, note.forum)
    print(conference.get_id())
    forum = client.get_note(id=note.forum)
    comment_readers = forum.content['Contact Emails'][:]
    comment_readers.append('OpenReview.net/Support')
    comment_note = openreview.Note(
        invitation = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Comment',
        forum = forum.id,
        replyto = forum.id,
        readers = comment_readers,
        writers = ['OpenReview.net/Support'],
        signatures = ['OpenReview.net/Support'],
        content = {
            'title': 'Your venue is available in OpenReview',
            'comment': '''
Hi Program Chairs,

Thanks for submitting a venue request.

We have set up the venue based on the information that you provided here: https://openreview.net/forum?id={noteId}

You can use the following links to access to the conference:

Venue home page: https://openreview.net/group?id={conference_id}
Venue Program Chairs console: https://openreview.net/group?id={program_chairs_id}

If you need to make a change to the information provided in your request form, please edit/revise it directly. We will update your venue accordingly.

If you need special features that are not included in your request form, you can create a comment here or contact us at info@openreview.net and we will assist you.

Thanks!

OpenReview Team
            '''.format(noteId = forum.id, conference_id = conference.get_id(), program_chairs_id = conference.get_program_chairs_id())
        }
    )
    client.post_note(comment_note)

    readers = [conference.get_program_chairs_id(), 'OpenReview.net/Support']
    readers.extend(forum.signatures[:])

    forum.writers = ['OpenReview.net']
    forum.readers = readers
    client.post_note(forum)

    revision_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Revision',
        super = 'OpenReview.net/Support/-/Revision',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'referent': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = ['OpenReview.net/Support']
    ))

    reviewer_recruitment_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Reviewer_Recruitment',
        super = 'OpenReview.net/Support/-/Reviewer_Recruitment',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'replyto': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = ['OpenReview.net/Support']
    ))

    if (forum.content['Area Chairs (Metareviewers)'] == "Yes, our venue has Area Chairs") :
        ac_recruitment_invitation = client.post_invitation(openreview.Invitation(
            id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Area_Chair_Recruitment',
            super = 'OpenReview.net/Support/-/Area_Chair_Recruitment',
            invitees = readers,
            reply = {
                'forum': forum.id,
                'replyto': forum.id,
                'readers' : {
                    'description': 'The users who will be allowed to read the above content.',
                    'values' : readers
                }
            },
            signatures = ['OpenReview.net/Support']
        ))

        configure_metareviews_invitation = client.post_invitation(openreview.Invitation(
            id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Configure_Meta_Reviews',
            super = 'OpenReview.net/Support/-/Configure_Meta_Reviews',
            invitees = readers,
            reply = {
                'forum': forum.id,
                'referent': forum.id,
                'readers' : {
                    'description': 'The users who will be allowed to read the above content.',
                    'values' : readers
                }
            },
            signatures = [conference.get_program_chairs_id()]
        ))

    if forum.content.get('Author and Reviewer Anonymity', None) == 'Double-blind':
        anonymize_submissions_invitation = client.post_invitation(openreview.Invitation(
            id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Anonymize_Submissions',
            super = 'OpenReview.net/Support/-/Anonymize_Submissions',
            invitees = readers,
            reply = {
                'forum': forum.id,
                'replyto': forum.id,
                'readers' : {
                    'description': 'The users who will be allowed to read the above content.',
                    'values' : readers
                }
            },
            signatures = [conference.get_program_chairs_id()]
        ))

    configure_reviews_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Configure_Reviews',
        super = 'OpenReview.net/Support/-/Configure_Reviews',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'referent': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = [conference.get_program_chairs_id()]
    ))

    configure_decisions_invitation = client.post_invitation(openreview.Invitation(
        id = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Configure_Decisions',
        super = 'OpenReview.net/Support/-/Configure_Decisions',
        invitees = readers,
        reply = {
            'forum': forum.id,
            'referent': forum.id,
            'readers' : {
                'description': 'The users who will be allowed to read the above content.',
                'values' : readers
            }
        },
        signatures = [conference.get_program_chairs_id()]
    ))
