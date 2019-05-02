def process(client, note, invitation):
    conference = openreview.helpers.get_conference(client, note.forum)
    print('Conference: ', conference.get_id())