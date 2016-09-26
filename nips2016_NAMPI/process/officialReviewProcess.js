function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');


    origNote.then(function(result){
      var note_number = result.notes[0].number

      var authors = result.notes[0].content.author_emails.trim().split(",");

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to " + conference + ": \"" + note.content.title + "\"",
        "message": "Your submission to "+ conference +" has received an official review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var promises = [
        or3client.or3request( or3client.mailUrl, author_mail, 'POST', token )
      ];
      return Promise.all(promises)
    })
    .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
    .then(result=>done())
    .catch(error=>done(error));

    return true;
  };