function(){
// This function assumes the following are already defined:
//            CONFERENCE, CONFERENCE_NAME, PAPERGRP and or3client = lib.or3client;

    console.log('the Comment Process is here');
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    // send email to author of paper submission that comment was added
    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [PAPERGRP + '/Reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to "+CONFERENCE+": \"" + forum.content.title + "\"",
        "message": "Your submission to " + CONFERENCE_NAME + " has received a comment.\n\nTitle: " + note.content.title + "\n\nReview: " + note.content.comment + "\n\n To view the review, click here: " + baseUrl+"/forum?id=" + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );

      return authorMailP;
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
