function(){
    const TRACK_NAME = <<param0>>;
    const CONFERENCE = 'roboticsfoundation.org/RSS/2017/RCW_Workshop';
    const TRACK = CONFERENCE+'/-_'+TRACK_NAME;
    const PAPERGRP = TRACK+'/Paper' + note.number;
    var CONFERENCE_NAME = 'RSS 2017 RCW Workshop -'+TRACK_NAME+' Track'
    var or3client = lib.or3client;

    console.log('the Comment Process is here');
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);



    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [PAPERGRP + '/Reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to "+TRACK+": \"" + forum.content.title + "\"",
        "message": "Your submission to " + CONFERENCE_NAME + " has received a comment.\n\nTitle: " + note.content.title + "\n\nReview: " + note.content.comment + "\n\n To view the review, click here: " + baseUrl+"/forum?id=" + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );

      return authorMailP;
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
