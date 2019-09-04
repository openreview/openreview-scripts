def process(client, note, invitation):
    conference_id = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'

    # send confirmation email
    msg = 'Your report submission to NeurIPS 2019 Reproducibility Challenge has been posted. \n\nTitle: {title}'.format(
        title=note.content['title'])
    client.send_mail("NeurIPS Reproducibility Challenge report received", note.content['authorids'], msg)

    authors = client.get_group(conference_id+'/Authors')
    authors.members.extend(note.content['authorids'])
    client.post_group(authors)
