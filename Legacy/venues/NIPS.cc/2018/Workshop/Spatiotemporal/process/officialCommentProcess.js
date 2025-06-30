function(){
    var or3client = lib.or3client;

    var CONF_TITLE= "NIPS 2018 Spatiotemporal Workshop";
    var CONFERENCE_ID = 'NIPS.cc/2018/Workshop/Spatiotemporal';
    var PROG_CHAIRS = CONFERENCE_ID+'/Program_Chairs';

    // This is to support discussion between PCs and a reviewer
    // If the comment is added to the original submission or a regular comment
    // then send emails to PCs and Reviewers
    // If the comment is added to a review or evaluation or an official review
    // then send email to the author of that note

    var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;

    Promise.all([
      forumNoteP,
      replytoNoteP
    ]).then(function(result) {
      var forumNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : [];
      var reviewer_group = CONFERENCE_ID+'/Paper'+forumNote.number+'/Reviewers';
      var send_to = replytoNoteSignatures;
      if (send_to[0] != PROG_CHAIRS) {
        send_to.push(PROG_CHAIRS)
      }
      if (replytoNote) {
        var invite_name = replytoNote.invitation;
        if (invite_name.lastIndexOf('\/Comment') >= 0) {
          // this is an official comment on a regular comment
          send_to = [PROG_CHAIRS, reviewer_group];
        }
      }
      if (replytoNoteSignatures==[]) {
        // if replytoNoteSignatures empty then signifies official comment on forum note
        send_to = [PROG_CHAIRS, reviewer_group];
      }

      var response_mail = {
        "groups": send_to,
        "subject": "Confidential comment posted to paper: \"" + forumNote.content.title + "\"",
        "message": 'Your entry has received a response.\n\nComment = '+note.content.comment+'\n\nTo view the comment, click here: ' + baseUrl+'/forum?id=' + note.forum +'&noteId='+note.id
      };
      var responseMailP = or3client.or3request( or3client.mailUrl, response_mail, 'POST', token );

      return responseMailP;
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };