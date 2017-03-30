function(){
    const TRACK_NAME = <<param0>>;
    const CONFERENCE = 'roboticsfoundation.org/RSS/2017/Workshop';
    const TRACK = CONFERENCE+'/'+TRACK_NAME;
    const PAPERGRP = TRACK+'/Paper' + note.number;
    const CONFERENCE_NAME = 'RSS 2017 Workshop '+TRACK_NAME+' Track';
    var or3client = lib.or3client;

    console.log('PAM - the official Review Process is here Review'+note.number);

    // send email to author of paper submission
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [PAPERGRP + '/Reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to "+TRACK+": \"" + forum.content.title + "\"",
        "message": "Your submission to " + CONFERENCE_NAME + " has received an official review.\n\nTitle: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl+"/forum?id=" + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );

      // allow this reviewer to see other reviews
      var non_reviewer_group = TRACK+'/Paper'+note_number+'/Reviewers/NonReaders';
      console.log('PAM group:'+non_reviewer_group+'  signature:'+note.signatures[0]);
      var reviewReader = or3client.removeGroupMember(non_reviewer_group, note.signatures[0], token);

      return Promise.all([
        authorMailP,
        reviewReader
      ]);
    })
    // do not allow reviewer to post another review for this paper
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };




