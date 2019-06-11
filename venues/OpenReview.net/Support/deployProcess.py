def process(client, note, invitation):
    print('client:', client.baseurl)
    print('note:', note.id)
    print('invitation:', invitation.id)
    conference = openreview.helpers.get_conference(client, note.forum)
    print(conference.get_id())
    forum = client.get_note(id=note.forum)
    readers = forum.content['Contact Emails']
    readers.append('OpenReview.net/Support')
    comment_note = openreview.Note(
        invitation = 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Comment',
        forum = forum.id,
        replyto = forum.id,
        readers = readers,
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

    revision_invitation = client.get_invitation(id= 'OpenReview.net/Support/-/Request' + str(forum.number) + '/Revision')
    revision_invitation.reply['readers'] = {
        'values':  readers
    }
    revision_invitation.invitees = readers
    client.post_invitation(revision_invitation)

    forum.writers = ['OpenReview.net']
    forum_readers_list = forum.signatures[:]
    forum_readers_list.extend(['OpenReview.net/Support', conference.get_program_chairs_id()])
    forum.readers = forum_readers_list
    client.post_note(forum)

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
