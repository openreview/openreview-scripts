function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'ICLR.cc/2020/Conference';
    var SHORT_PHRASE = 'ICLR 2020';

    or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
    .then(function(result) {

      var forumNote = result.notes[0];
      var AREA_CHAIRS_ID = CONFERENCE_ID + '/Paper' + forumNote.number + '/Area_Chair1';
      var BUDDY_AREA_CHAIRS_ID = CONFERENCE_ID + '/Paper' + forumNote.number + '/Buddy_Area_Chair1';
      var buddy_ac_regex = /Buddy/;

      var ac_mail = {
        groups: [AREA_CHAIRS_ID],
        subject: '[' + SHORT_PHRASE + '] Comment posted by your buddy AC to a paper in your area. Paper Number: ' + forumNote.number + ', Paper Title: "' + forumNote.content.title + '"',
        message: 'A comment was posted by your buddy Area Chair to a paper for which you are serving as the primary Area Chair.\n\nPaper Number: ' + forumNote.number + '\n\nPaper Title: "' + forumNote.content.title + '"\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var buddy_ac_mail = {
        groups: [BUDDY_AREA_CHAIRS_ID],
        subject: '[' + SHORT_PHRASE + '] Comment posted to a paper for which you are a buddy AC. Paper Number: ' + forumNote.number + ', Paper Title: "' + forumNote.content.title + '"',
        message: 'A comment was posted by the primary Area Chair to a paper for which you are serving as buddy Area Chair.\n\nPaper Number: ' + forumNote.number + '\n\nPaper Title: "' + forumNote.content.title + '"\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var comment_author_mail = {
        groups: [note.tauthor],
        subject: '[' + SHORT_PHRASE + '] Your comment was received on Paper Number: ' + forumNote.number + ', Paper Title: "' + forumNote.content.title + '"',
        message: 'Your comment was received on a submission to ' + SHORT_PHRASE + '.\n\nPaper Number: ' + forumNote.number + '\n\nPaper Title: "' + forumNote.content.title + '"\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var promises = [];
      promises.push(or3client.or3request(or3client.mailUrl, comment_author_mail, 'POST', token));
      if (note.signatures[0].match(buddy_ac_regex)){
        promises.push(or3client.or3request(or3client.mailUrl, ac_mail, 'POST', token));
      } else {
        promises.push(or3client.or3request(or3client.mailUrl, buddy_ac_mail, 'POST', token));
      }

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
};
