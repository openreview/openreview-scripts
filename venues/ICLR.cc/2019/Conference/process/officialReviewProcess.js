//EDIT ME

function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
    var SHORT_PHRASE = "ICLR 2019";
    var PAPER_REVIEWERS;
    var PAPER_AREACHAIRS;

    var forumNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    forumNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      PAPER_REVIEWERS = CONFERENCE_ID + '/Paper' + note_number + '/Reviewers';
      PAPER_AREACHAIRS = CONFERENCE_ID + '/Paper' + note_number + '/Area_Chairs';
      PAPER_AUTHORS = CONFERENCE_ID + '/Paper' + note_number + '/Authors'
      var areachair_mail = {
        "groups": [PAPER_AREACHAIRS],
        "subject": "[" + SHORT_PHRASE + "] Review posted to your assigned paper: \"" + forum.content.title + "\"",
        "message": "A submission to " + SHORT_PHRASE + ", for which you are an official area chair, has received an official review. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      var author_mail = {
        "groups": [PAPER_AUTHORS],
        "subject": "[" + SHORT_PHRASE + "] Review posted to your submission: \"" + forum.content.title + "\"",
        "message": "Your submission to " + SHORT_PHRASE + " has received an official review. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );
      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );

      return areachairMailP, authorMailP;
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
