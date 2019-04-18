def process(client, note, invitation):
    print('client:', client.baseurl)
    print('note:', note.id)
    print('invitation:', invitation.id)
    conference = openreview.helpers.get_conference(client, note.forum)
    forum = client.get_note(note.forum)
    if 'conference_id' in forum.content:
        # This means that we just updated a live venue
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
                'title': 'Your venue has been updated',
                'comment': '''
Hi Program Chairs,

We have updated the venue based on the updated information that you provided here: https://openreview.net/forum?id={noteId} .

If you need to make a change to the venue, please edit the information provided in your request form directly. We will update your venue accordingly.

If you need special features that are not included in your request form, you can create a comment here or contact us at info@openreview.net and we will assist you.

Thanks!

OpenReview Team'''.format(noteId = forum.id)
            }
        )
        client.post_note(comment_note)

    print('Conference: ', conference.get_id())