function(){
    var or3client = lib.or3client;

    var CONFERENCEPHRASE = "DeSemWeb2017"

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

      var selfReview = replytoNoteSignatures.indexOf(note.signatures[0]) > -1 ? true : false;
      console.log('self comment detected');
      if(!selfReview){
        author_mail = {
          "groups": origNote.content.authorids,
          "subject": "Your submission to "+CONFERENCEPHRASE+" has received a review",
          "message": "Your submission to "+CONFERENCEPHRASE+" has received a review.\n\nReview title: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl+"/forum?id=" + note.forum +'&noteId='+note.id
        };
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
