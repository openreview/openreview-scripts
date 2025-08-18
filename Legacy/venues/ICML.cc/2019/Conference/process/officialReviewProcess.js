//EDIT ME

function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'ICML.cc/2019/Conference';

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [CONFERENCE_ID + '/Paper' + note_number + '/Reviewers'];
      var areachairs = [CONFERENCE_ID + '/Paper' + note_number + '/Area_Chairs'];
      var authors = forum.content.authorids;

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + forum.content.title + "\"",
        "message": "A submission to " + conference + ", for which you are an official area chair, has received an official review. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );

      return areachairMailP;
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
