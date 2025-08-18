function(){
    var or3client = lib.or3client;
    var confData = <<cvprdata.js>>

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    const PAPERGRP = confData.CONFERENCE+'/Paper' + note.number;
    const PAPERINV = confData.CONFERENCE+'/-/Paper' + note.number;

    origNote.then(function(result) {
      var forumNote = result.notes[0];
      var note_number = forumNote.number;
      var origNoteTitle = forumNote.content.title;
      var reviewers = ['auai.org/UAI/2017/Paper' + note_number + '/Reviewers'];
      var areachairs = ['auai.org/UAI/2017/Paper' + note_number + '/Area_Chair'];
      var authors = forumNote.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to UAI 2017: \"" + origNoteTitle + "\"",
        "message": "Your submission to UAI 2017 has received an review.\n\nTitle: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl+"/forum?id=" + note.forum
      };

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + origNoteTitle + "\"",
        "message": "A submission to UAI 2017, for which you are the area chair, has received a review. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );

      return Promise.all([
        authorMailP,
        areachairMailP
      ])
      .then(result => {
        var reviewRevisionInvitation = {
          id: 'auai.org/UAI/2017/-/Paper' + note_number + '/Review' + note.number + '/Add/Revision',
          signatures: ['auai.org/UAI/2017'],
          writers: ['auai.org/UAI/2017'],
          invitees: note.signatures,
          noninvitees: [],
          readers: ['everyone'],
          reply: {
            forum: forumNote.id,
            referent: note.id,
            signatures: invitation.reply.signatures,
            writers: invitation.reply.writers,
            readers: invitation.reply.readers,
            content: invitation.reply.content
          }
        }
        return or3client.or3request(or3client.inviteUrl, reviewRevisionInvitation, 'POST', token);
      })
      .then(result => or3client.removeGroupMember('auai.org/UAI/2017/Paper' + note_number + '/Reviewers/NonReaders', note.signatures[0], token));
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
