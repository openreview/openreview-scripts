function(){
    var SHORT_PHRASE = 'MIDL 2018 Abstract';
    var CONFERENCE_ID = 'MIDL.amsterdam/2018/Abstract';
    var or3client = lib.or3client;

    // send email to author of paper submission
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var author_mail = {
        groups: forum.content.authorids,
        subject: 'Review of your submission to ' + SHORT_PHRASE + ': "' + forum.content.title + '"',
        message: 'Your submission to ' + SHORT_PHRASE + ' has received an official review.\n\nTitle: ' + note.content.title + '\n\nReview: ' + note.content.review + '\n\nTo view the review, click here: ' + baseUrl+'/forum?id=' + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );

      return Promise.all([
        authorMailP,
      ]);
    })
    // do not allow reviewer to post another review for this paper
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };




