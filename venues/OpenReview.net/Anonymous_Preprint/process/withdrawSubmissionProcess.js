function() {
    var or3client = lib.or3client;

    var CONF = 'OpenReview.net/Anonymous_Preprint';
    var CONFERENCEPHRASE = "OpenReview Anonymous Preprint";
    or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
    .then(result => {
        if (result.notes.length > 0){
            var blindedNote = result.notes[0];

            var milliseconds = (new Date).getTime();
            blindedNote.ddate = milliseconds
            blindedNote.content = {
                    authorids: blindedNote.content.authorids,
                    authors: blindedNote.content.author,
                    _bibtex: blindedNote.content._bibtex
                  }
            return or3client.or3request(or3client.notesUrl, blindedNote, 'POST', token);
        } else {
            return Promise.reject('No notes with the id ' + note.referent + ' were found');
        }
    })
    .then(result => or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token))
    .then(result => {
      var blindedNote = result.notes[0];
      author_mail ={
        "groups": blindedNote.content.authorids,
        "subject": "Your submission to " + CONFERENCEPHRASE + " has been withdrawn",
        "message": "Your submission to " + CONFERENCEPHRASE + " has been withdrawn. If this was a mistake, please contact OpenReview Support."
      };
      return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token);
      
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
}
