def process(client, note, invitation):
    # create new reference with only the updated bibtex
    import datetime

    # Get the blinded submission in order to reveal author info
    blind_note = client.get_note(id=note.forum)
    blind_note.content={'_bibtex': blind_note.content['_bibtex']}
    # Post blinded note w/o covering author info
    blind_note = client.post_note(blind_note)

    # then use author info to update bibtex
    first_word = blind_note.content['title'].split(' ')[0].lower()
    year = str(datetime.datetime.now().year)
    first_author = blind_note.content['authors'][0]
    last_name = first_author.split(' ')[-1].lower()

    bibtex_text = 'unpublished{\
              \n' + last_name + year + first_word + ',\
              \ntitle={' + blind_note.content['title'] + '},\
              \nauthor={' + ', '.join(blind_note.content['authors']) + '},\
              \njournal={OpenReview Preprint},\
              \nyear={' + year + '},\
              \nnote={preprint under review}\
          \n}'

    print("Reveal process: "+bibtex_text)
    blind_note.content = {'_bibtex': bibtex_text}
    client.post_note(blind_note)
