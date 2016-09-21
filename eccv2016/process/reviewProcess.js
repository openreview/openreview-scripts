function(){
    var or3client = lib.or3client;
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    
    var conference = or3client.prettyConferenceName(note);

    origNote.then(function(result){
      var mail = {
        "groups": result.notes[0].content.author_emails.trim().split(","),
        "subject": "Review of your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, mail, 'POST', token )
      
    })
    .then(result => or3client.fulfillInvitation(invitation, note, token))
    .then(result => done())
    .catch(error => done(error));
    
    return true;
  };