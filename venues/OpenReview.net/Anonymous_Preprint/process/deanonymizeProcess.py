def process(client, note, invitation):

    import re

    original = client.get_note(note.forum)

    notes = client.get_notes(original = note.forum)
    assert len(notes) == 1, 'there should be a single blind note'
    blind = notes[0]

    references = client.get_references(referent=blind.id)
    assert len(references) == 1, 'something went wrong; multiple blind references'

    blind_reference = references[0]

    first_word = re.sub('[^a-zA-Z]', '', original.content['title'].split(' ')[0].lower())
    first_author_last_name = original.content['authors'][0].split(' ')[-1].lower()

    blind_reference.content = {
        '_bibtex': None
    #     '_bibtex': '@unpublished{\
    #       \nanonymous2018' + first_word + ',\
    #       \ntitle={' + note.content.title + '},\
    #       \nauthor=' + ', '.join(original.content['authors']) + ',\
    #       \njournal={OpenReview Preprint},\
    #       \nyear={2018},\
    #       \nnote={anonymous preprint under review}\
    #   \n}'
    }

    client.post_note(blind_reference)



