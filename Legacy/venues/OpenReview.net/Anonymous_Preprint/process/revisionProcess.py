def process(client, note, invitation):
    import datetime

    # update bibtex
    def getBibtex(note) :
        year = str(datetime.datetime.now().year)
        first_word = note.content['title'].split(' ')[0].lower()
        first_author = note.content['authors'][0]
        last_name = first_author.split(' ')[-1].lower()
        return '@unpublished{\
              \n' + last_name + year + first_word + ',\
              \ntitle={' + note.content['title'] + '},\
              \nauthor={' + ','.join(note.content['authors']) + '},\
              \njournal={OpenReview Preprint},\
              \nyear={' + year + '},\
              \nnote={anonymous preprint under review}\
          \n}'

    notes = client.get_notes(original=note.forum)
    forum_note = None
    for note in notes:
        if note.invitation.endswith("Blind_Submission"):
            forum_note=note

    if forum_note:
        forum_content = {
                'authors': forum_note.content['authors'],
                'authorids': forum_note.content['authorids'],
                '_bibtex': getBibtex(forum_note)
              }
        forum_note.content = forum_content
        client.post_note(forum_note)

    else:
        raise openreview.OpenReviewException('Revision process: Blind submission not found for forum '+note.forum)