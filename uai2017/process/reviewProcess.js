function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');


    origNote.then(function(result) {
      var forumNote = result.notes[0];
      var note_number = forumNote.number;
      var origNoteTitle = forumNote.content.title;
      var reviewers = ['auai.org/UAI/2017/Paper' + note_number + '/Reviewers'];
      var areachairs = ['auai.org/UAI/2017/Paper' + note_number + '/Area_Chair'];

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + origNoteTitle + "\"",
        "message": "A submission to UAI 2017, for which you are the area chair, has received a review. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );

      return Promise.all([
        areachairMailP
      ])
      .then(result => {
        var reviewRevisionInvitation = {
          id: 'auai.org/UAI/2017/-/Review' + note.number + '/Add/Revision',
          signatures: ['auai.org/UAI/2017'],
          writers: ['auai.org/UAI/2017'],
          invitees: note.signatures,
          noninvitees: [],
          readers: ['everyone'],
          process: 'function() { done() return true; }',
          reply: {
            forum: forumNote.id,
            referent: note.id,
            signatures: invitation.reply.signatures,
            writers: invitation.reply.writers,
            readers: invitation.reply.readers,
            content: invitation.reply.content
          }
        }
        return or3client.or3request(or3client.inviteUrl, reviewRevisionInvitation, 'POST', token)
      });
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
