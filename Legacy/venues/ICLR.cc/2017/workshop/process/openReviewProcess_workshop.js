function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    origNote.then(function(result){
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = ['ICLR.cc/2017/workshop/paper'+note_number+'/reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to ICLR 2017 Workshop: \"" + forum.content.title + "\"",
        "message": "Your submission to ICLR 2017 Workshop has received a public review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token);

    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
