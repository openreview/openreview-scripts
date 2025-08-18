function(){
    var or3client = lib.or3client;

    var SHORT_PHRASE = 'NIPS 2018 Spatiotemporal Workshop';

    var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);

    Promise.all([
      origNoteP,
    ]).then(function(result) {

      var origNote = result[0].notes[0];

      var author_mail = {
        groups: origNote.content.authorids,
        subject: 'Your submission to ' + SHORT_PHRASE + ' has received a comment',
        message: 'Your submission to ' + SHORT_PHRASE + ' has received a comment.\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl+'/forum?id=' + note.forum +'&noteId='+note.id
      };

      return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
