function(){
  var or3client = lib.or3client;

  var CONFERENCE_ID = 'ACM.org/SIGIR/Badging';
  var SHORT_PHRASE = "ACM SIGIR Badging";
  var PAPER_AUTHORS = CONFERENCE_ID + '/Paper' + note.number + '/Authors';

  var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);

  forumNoteP.then(function(result) {
    var forumNote = result.notes[0];
    author_mail = {
      "groups": forumNote.content.authorids,
      "subject": "Your submission to " + SHORT_PHRASE + " has been withdrawn",
      "message": "Your submission, \""+ forumNote.content.title +"\", has been withdrawn by one \
       of the authors. To view your withdrawn submission, click here: " + baseUrl + "/forum?id=" + forumNote.forum + "\n\n\ \
       If you believe that this withdrawal was an error, please contact info@openreview.net \
       as soon as possible."
    };
    return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token);
  })
  .then(result => done())
  .catch(error => done(error));

  return true;
};
