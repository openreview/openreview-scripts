//EDIT ME

function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'AKBC.ws/2019/Conference';
    var PAPER_REVIEWERS;
    var PAPER_AREACHAIRS;

    var forumNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    forumNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      PAPER_REVIEWERS = CONFERENCE_ID + '/Paper' + note_number + '/Reviewers';
      PAPER_AREACHAIRS = CONFERENCE_ID + '/Paper' + note_number + '/Area_Chairs';
      console.log(PAPER_REVIEWERS);
      console.log(PAPER_AREACHAIRS);
      console.log(note_number);
      var areachair_mail = {
        "groups": [PAPER_AREACHAIRS],
        "subject": "Review posted to your assigned paper: \"" + forum.content.title + "\"",
        "message": "A submission to " + CONFERENCE_ID + ", for which you are an official area chair, has received an official review. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );

      return areachairMailP;
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
