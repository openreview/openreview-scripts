function(){
    const TRACK_NAME = <<param0>>;
    const CONFERENCE = 'roboticsfoundation.org/RSS/2017/Workshop';
    const TRACK = CONFERENCE+'/'+TRACK_NAME;
    const PAPERGRP = TRACK+'/Paper' + note.number;

    var or3client = lib.or3client;

    console.log('PAM - the official Review Process is here');
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    var conference = 'RSS 2017 Workshop '+TRACK_NAME+' Track'

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

      return authorMailP;
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
