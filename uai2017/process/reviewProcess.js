function(){
  var or3client = lib.or3client;

  var origNote = or3client.or3request(notesUrl+'?id='+note.forum, {}, 'GET', token);

  origNote.then(function(result){
    var mail = {
      "groups": result.notes[0].content.authorids,
      "subject": "Review of your submission to UAI 2017: \"" + result.notes[0].content.title + "\".",
      "message": "Your submission to UAI 2017 has received a review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: http://dev.openreview.net/forum?id=" + note.forum
    };
    var mailP = or3client.or3request( mailUrl, mail, 'POST', token )

  });

  var fulfilledP = or3client.fulfillInvitation(invitation, note, token);
  return true;
};
