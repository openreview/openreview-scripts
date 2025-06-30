function(){
    "use strict";
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    var conference = or3client.getConference(note);

    origNote.then(function(result){
      var authors = result.notes[0].content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to " + conference + ": \"" + note.content.title + "\"",
        "message": "Your submission to "+ conference +" has received an official review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var promises = [
        or3client.or3request(or3client.mailUrl, author_mail, 'POST', token)
      ];
      return Promise.all(promises);
    })
    .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
    .then(result=>done())
    .catch(error=>done(error));

    return true;
  }