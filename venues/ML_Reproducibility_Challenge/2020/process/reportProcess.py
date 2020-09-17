def process(client, note, invitation):
    conference_id = 'NeurIPS.cc/2019/Reproducibility_Challenge'

    # send confirmation email
    msg = 'Your report submission to NeurIPS 2019 Reproducibility Challenge has been posted. \n\nTitle: {title}'.format(
        title=note.content['title'])
    client.send_mail("NeurIPS Reproducibility Challenge report received", note.content['authorids'], msg)

    authors = client.get_group(conference_id+'/Authors')
    authors.members.extend(note.content['authorids'])
    client.post_group(authors)
