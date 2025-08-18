function(){
    var or3client = lib.or3client;

    var SHORT_PHRASE = 'NIPS 2018 Spatiotemporal Workshop';

    var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;

    Promise.all([
      origNoteP,
      replytoNoteP
    ]).then(function(result) {

      var origNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : [];
      var author_mail = {
        groups: origNote.content.authorids,
        subject: 'Your submission to ' + SHORT_PHRASE +  ' has received an evaluation',
        message: 'Your submission to ' + SHORT_PHRASE + ' has received an evaluation.\n\nEvaluation: ' + note.content.evaluation + '\n\nTo view the evaluation, click here: ' + baseUrl+'/forum?id=' + note.forum +'&noteId='+note.id
      };

      return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token);

    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
