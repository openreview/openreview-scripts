//EDIT ME

function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'ACM.org/SIGIR/Badging';
    var PAPER_REVIEWERS;
    var PAPER_CHAIRS;

    var forumNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    forumNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      PAPER_REVIEWERS = CONFERENCE_ID + '/Paper' + note_number + '/Reviewers';
      PAPER_CHAIRS = CONFERENCE_ID + '/Paper' + note_number + '/Chairs';
      console.log(PAPER_REVIEWERS);
      console.log(PAPER_CHAIRS);
      console.log(note_number);
      var chair_mail = {
        "groups": [PAPER_CHAIRS],
        "subject": "Review posted to your assigned submission: \"" + forum.content.title + "\"",
        "message": "An artifact, for which you are a Chair, in " + CONFERENCE_ID + " has received an official review. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      var chairMailP = or3client.or3request( or3client.mailUrl, chair_mail, 'POST', token );

      return chairMailP;
    })
    .then(result => {
      console.log('attempting to add to group ' + PAPER_REVIEWERS + '/Submitted');
      return or3client.addGroupMember(PAPER_REVIEWERS + '/Submitted', note.signatures[0], token);
    })
    .then(result => {
      console.log('attempting to add to group ' + PAPER_REVIEWERS + '/Unubmitted');
      return or3client.removeGroupMember(PAPER_REVIEWERS + '/Unsubmitted', note.signatures[0], token);
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
