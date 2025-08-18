def process(client, note, invitation):
    CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'

    # send confirmation email
    msg = 'Your report submission to ML Reproducibility Challenge 2020 has been posted. \n\nTitle: {title}'.format(
        title=note.content['title'])
    client.send_mail("ML Reproducibility Challenge 2020 report received", note.content['authorids'], msg)

    authors = client.get_group(CONFERENCE_ID + '/Authors')
    authors.members.extend(note.content['authorids'])
    client.post_group(authors)
