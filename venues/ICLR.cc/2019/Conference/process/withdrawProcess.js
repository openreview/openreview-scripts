function(){
  var or3client = lib.or3client;

  var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
  var SHORT_PHRASE = "ICLR 2019";
  var PAPER_AUTHORS = CONFERENCE_ID + '/Paper' + note.number + '/Authors';

  var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);

  forumNoteP.then(function(result) {
    var forumNote = result.notes[0];
    author_mail = {
      "groups": forumNote.content.authorids,
      "subject": "Your submission to " + SHORT_PHRASE + " has been withdrawn",
      "message": "Your submission to " + SHORT_PHRASE + " has been withdrawn by one of the authors.\
Per ICLR policy, the identity of all authors will be revealed to the public. \
The record of this submission (including all existing reviews and comments) \
will remain publicly accessible on OpenReview.\n\nIf you believe that this withdrawal was an error, please contact info@openreview.net as soon as possible."
    };
  })
  .then(result => done())
  .catch(error => done(error));

  return true;
};
