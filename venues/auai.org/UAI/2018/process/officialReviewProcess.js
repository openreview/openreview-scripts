function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = ['auai.org/UAI/2018/Paper' + note_number + '/Reviewers'];
      var areachairs = ['auai.org/UAI/2018/Paper' + note_number + '/Area_Chairs'];
      var reviewersUnsubmittedId = 'auai.org/UAI/2018/Paper' + note_number + '/Reviewers/Unsubmitted';
      var reviewersSubmittedId = 'auai.org/UAI/2018/Paper' + note_number + '/Reviewers/Submitted';
      var authors = forum.content.authorids;

      var author_mail = {
        "groups" : authors,
        "subject": "Review posted to your submitted paper: \"" + forum.content.title + "\"",
        "message": "Your submissions to " + conference + " has received an official review. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };

      var reviewer_mail = {
        "groups" : reviewers,
        "subject": "Review posted to your assigned paper: \"" + forum.content.title + "\"",
        "message": "A submission to " + conference + ", for which you are an official reviewer, has received a review. \n\nTitle: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + forum.content.title + "\"",
        "message": "A submission to " + conference + ", for which you are an official area chair, has received a review. \n\nTitle: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
      //var reviewerMailP = or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );

      var removeFromUnsubmittedP = or3client.removeGroupMember(reviewersUnsubmittedId, note.signatures[0], token);
      var addToSubmittedP = or3client.addGroupMember(reviewersSubmittedId, note.signatures[0], token)
      return Promise.all([areachairMailP, authorMailP, removeFromUnsubmittedP, addToSubmittedP]);
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => or3client.or3request(or3client.inviteUrl+'?id='+note.invitation, {}, 'GET', token))
    .then(result => {
      var reviewInvitation = result.invitations[0];
      var signatureComponents = note.signatures[0].split('/');
      console.log('signature components: ' + signatureComponents);
      var revisionInvitation = {
        'id': 'auai.org/UAI/2018/-/' + signatureComponents[4] + '/' + signatureComponents[3] + '/Revise_Review',
        'writers': reviewInvitation.writers,
        'signatures': reviewInvitation.signatures,
        'readers': reviewInvitation.readers,
        'invitees': note.signatures,
        'reply': {
            'forum': note.forum,
            'referent': note.id,
            'writers': reviewInvitation.reply.writers,
            'signatures': reviewInvitation.reply.signatures,
            'readers': reviewInvitation.reply.readers,
            'content': reviewInvitation.reply.content
        }
      };
      return or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token);
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
