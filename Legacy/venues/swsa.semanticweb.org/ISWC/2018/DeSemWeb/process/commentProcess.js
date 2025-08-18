function(){
    var or3client = lib.or3client;

    var SHORT_PHRASE = 'DeSemWeb 2018';

    var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;

    Promise.all([
      origNoteP,
      replytoNoteP
    ]).then(function(result) {

      var origNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : [];
      var author_mail;

      var selfComment = replytoNoteSignatures.indexOf(note.signatures[0]) > -1 ? true : false;
      console.log('self comment detected');
      if(!selfComment){
        if(replytoNote.id == origNote.id){
          author_mail = {
            groups: origNote.content.authorids,
            subject: 'Your submission to ' + SHORT_PHRASE +  ' has received a comment',
            message: 'Your submission to ' + SHORT_PHRASE + ' has received a comment.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl+'/forum?id=' + note.forum +'&noteId='+note.id
          };
        } else {
          author_mail = {
            groups: replytoNote.signatures == '(anonymous)' ? [] : replytoNote.signatures,
            subject: 'Your comment has received a response',
            message: 'Your comment titled "'+replytoNote.content.title+'" has received a response.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl+'/forum?id=' + note.forum +'&noteId='+note.id
          };
        }
        promises = [or3client.or3request(or3client.mailUrl, author_mail, 'POST', token)];
      } else {
        promises = []
      }

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
