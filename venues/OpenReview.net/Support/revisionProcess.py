def process(client, note, invitation):
    print('client:', client.baseurl)
    print('note:', note.id)
    print('invitation:', invitation.id)
    conference = openreview.helpers.get_conference(client, note.forum)
    print('Conference: ', conference.get_id())