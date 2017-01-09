function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result){
      var note_number = result.notes[0].number;
      var origNoteTitle = result.notes[0].content.title;
      var reviewers = ['auai.org/UAI/2017/Paper'+note_number+'/Reviewers'];
      var areachairs = ['auai.org/UAI/2017/Paper'+note_number+'/Area_Chair'];
      var authors = result.notes[0].content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to UAI 2017: \"" + origNoteTitle + "\"",
        "message": "Your submission to UAI 2017 has received an official review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + origNoteTitle + "\"",
        "message": "A submission to UAI 2017, for which you are an official area chair, has received an official review. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );

      return Promise.all([
        authorMailP,
        areachairMailP
      ])
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
