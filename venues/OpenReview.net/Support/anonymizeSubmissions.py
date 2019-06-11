def process(client, note, invitation):
    conference = openreview.helpers.get_conference(client, note.forum)
    print('Creating blind submissions for conference: ', conference.get_id())
    conference.create_blind_submissions()
    blind_notes = list(client.get_notes(conference.get_blind_submission_id()))
    if blind_notes:
        deanonymize_submissions_invitation = client.post_invitation(openreview.Invitation(
                id = 'OpenReview.net/Support/-/Request' + str(note.invitation.split('Request')[1].split('/')[0]) + '/Deanonymize_Submissions',
                super = 'OpenReview.net/Support/-/Deanonymize_Submissions',
                invitees = invitation.invitees,
                reply = {
                    'forum': note.forum,
                    'replyto': note.forum,
                    'readers' : invitation.reply['readers']
                },
                signatures = [conference.get_program_chairs_id()]
            ))