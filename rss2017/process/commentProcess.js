function(){
    var or3client = lib.or3client;

    const CONFERENCE = 'roboticsfoundation.org/RSS/2017/Workshop';
    const COCHAIRS = CONFERENCE+"/Program_Co-Chairs"
    const PAPERGRP = CONFERENCE+'/Paper' + note.number;
    const PAPERINV = CONFERENCE+'/-/Paper' + note.number;
    const DUE_DATE = new Date(2017, 6, 30, 17, 15);

    console.log('the Public Comment Process is here');
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    var conference = 'RSS 2017 Workshop'

    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [PAPERGRP + '/Reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to "+CONFERENCE+": \"" + forum.content.title + "\"",
        "message": "Your submission to " + conference + " has received a public comment.\n\n
            Title: " + note.content.title + "\n\nReview: " + note.content.comment + "\n\n
            To view the review, click here: " + baseUrl+"/forum?id=" + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );

      return Promise.all([
        authorMailP
      ])
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
