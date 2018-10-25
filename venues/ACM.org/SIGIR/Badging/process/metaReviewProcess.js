function() {
    var or3client = lib.or3client;
    var CONFERENCE_ID = 'ACM.org/SIGIR/Badging';
    var SHORT_PHRASE = 'ACM SIGIR Badging'

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);


    var chairs = [CONFERENCE_ID];

    origNote.then(function(result){
      var forum = result.notes[0];

      var c_mail = {
        "groups": chairs,
        "subject": "[" + SHORT_PHRASE + "] Meta-review by a chair has been posted: " + "\"" + forum.content.title + "\".",
        "message": "An artifact submission to " + SHORT_PHRASE + " has received a meta-review by a chair.\n\nTitle: "+note.content.title+"\n\nMeta-review: "+note.content.metareview+"\n\nTo view the meta-review, click here: "+baseUrl+"/forum?id=" + note.forum + "&noteId=" + note.id
      };

      return or3client.or3request( or3client.mailUrl, c_mail, 'POST', token );

    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
