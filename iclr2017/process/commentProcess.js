function(){
  var or3client = lib.or3client;
	
  var origNote = or3client.or3request(notesUrl+'?id='+note.forum, {}, 'GET', token);
  var conference = or3client.prettyConferenceName(note);

  origNote.then(function(result){
    var mail = {
      "groups": result.notes[0].content.author_emails.trim().split(","),
      "subject": "Comment on your submission to " + conference + ": \"" + note.content.title + "\".",
      "message": "Your submission to "+ conference +" has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: http://dev.openreview.net/forum?id=" + note.forum
    };
    var mailP = or3client.or3request( mailUrl, mail, 'POST', token )
    
  });

  return true;
};