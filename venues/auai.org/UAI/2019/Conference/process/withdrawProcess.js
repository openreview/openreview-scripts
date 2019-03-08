function(){
  var or3client = lib.or3client;

  var CONFERENCE_ID = 'auai.org/UAI/2019/Conference';
  var SHORT_PHRASE = "UAI 2019";
  
  var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);

  forumNoteP.then(function(result) {
    var forumNote = result.notes[0];

    var author_mail = {
      'groups': forumNote.content.authorids,
      'subject': SHORT_PHRASE + ' : Notification of withdrawal of your submission "' + forumNote.content.title + '"',
      'message': 'Your submission, "' + forumNote.content.title + '", has been withdrawn by one of the authors. \
      To view your withdrawn submission, click here: ' + baseUrl + '/forum?id=' + forumNote.forum + '\n\n\
      The record of this submission (including all existing reviews and comments) \
      will remain on OpenReview visible only to the Authors of this paper and the Program Chairs.\n\n\
      If you believe that this withdrawal was an error, please contact info@openreview.net as soon as possible.'
    };

    var current_timestamp = Date.now();

    forumNote.invitation = CONFERENCE_ID + '/-/Withdrawn_Submission';
    forumNote.readers = [CONFERENCE_ID + '/Program_Chairs', forumNote.content.authorids[0]];
    forumNote.content = {
      'authors': forumNote.content.authors,
      'authorids': forumNote.content.authorids
    };
    return or3client.or3request(or3client.notesUrl, forumNote , 'POST', token)
    .then(result => or3client.or3request(or3client.mailUrl, author_mail, 'POST', token))
    .then(result => {
      return or3client.or3request(or3client.inviteUrl + '?id=' + CONFERENCE_ID + '/-/Paper' + forumNote.number + '/Revision', {}, 'GET', token)
      .then(result => {
        var revisionInvitation = result.invitations[0];
        revisionInvitation.expdate = current_timestamp;
        return or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token);
      })
    })
  })
  .then(result => done())
  .catch(error => done(error));

  return true;
};
