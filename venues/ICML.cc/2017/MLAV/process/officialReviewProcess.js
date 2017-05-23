function(){
// This function assumes the following are already defined:
//            CONFERENCE, CONFERENCE_NAME, PAPERGRP and or3client = lib.or3client;

    // send email to author of paper submission
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [PAPERGRP + '/Reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to "+CONFERENCE_NAME+": \"" + forum.content.title + "\"",
        "message": "Your submission to " + CONFERENCE_NAME + " has received an official review.\n\nTitle: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl+"/forum?id=" + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );

      // allow this reviewer to see other reviews
      var non_reviewer_group = CONFERENCE_NAME+'/Paper'+note_number+'/Reviewers/NonReaders';
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




