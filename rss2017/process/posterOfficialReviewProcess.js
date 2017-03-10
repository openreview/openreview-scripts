function(){
    var or3client = lib.or3client;

    const CONFERENCE = 'roboticsfoundation.org/RSS/2017/Workshop';
    const COCHAIRS = CONFERENCE+"/Program_Co-Chairs"
    const TRACK = CONFERENCE+"/Poster"
    const PAPERGRP = TRACK+'/Paper' + note.number;
    const PAPERINV = TRACK+'/-/Paper' + note.number;
    const DUE_DATE = new Date(2017, 6, 30, 17, 15);

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    var conference = 'RSS 2017 Workshop - Poster Track'

    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [PAPERGRP + '/Reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to "+TRACK+": \"" + forum.content.title + "\"",
        "message": "Your submission to " + conference + " has received an official review.\n\nTitle: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl+"/forum?id=" + note.forum
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
