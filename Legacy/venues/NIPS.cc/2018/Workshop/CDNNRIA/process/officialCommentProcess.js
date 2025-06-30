function(){
    var or3client = lib.or3client;

    var CONF_TITLE= "NIPS 2018 CDNNRIA Workshop";
    var CONFERENCE_ID = 'NIPS.cc/2018/Workshop/CDNNRIA';
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
      var author_group = CONFERENCE_ID+'/Paper'+forumNote.number+'/Authors';

      var response_mail = {
        "groups": [PROG_CHAIRS, author_group],
        "subject": "Official comment posted to paper: \"" + forumNote.content.title + "\"",
        "message": 'Your entry has received a response.\n\nComment = '+note.content.comment+'\n\nTo view the comment, click here: ' + baseUrl+'/forum?id=' + note.forum +'&noteId='+note.id
      };
      var responseMailP = or3client.or3request( or3client.mailUrl, response_mail, 'POST', token );

      return responseMailP;
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };