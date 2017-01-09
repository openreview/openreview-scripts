function() {

    var or3client = lib.or3client;

    var overwritingNote = {
        original: note.id,
        invitation: 'auai.org/UAI/2017/-/blind-submission',
        forum: null,
        parent: null,
        signatures: ['auai.org/UAI/2017'],
        writers: ['auai.org/UAI/2017'],
        readers: ["auai.org/UAI/2017/Program_Co-Chairs", "auai.org/UAI/2017/Senior_Program_Committee", "auai.org/UAI/2017/Program_Committee"],
        content: {
            authors: [],
            authorids: []
        }
    }

    //Send an email to the author of the submitted note, confirming its receipt
    var mail = {
        "groups": note.content.authorids,
        "subject": "Confirmation of your submission to UAI 2017: \"" + note.content.title + "\".",
        "message": `Your submission to UAI 2017 has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
    };



    or3client.or3request(or3client.notesUrl, overwritingNote, 'POST', token)
    .then(result => or3client.or3request(or3client.mailUrl, mail, 'POST', token))
    .then(result => done())
    .catch(error => done(error));

    return true;
}
