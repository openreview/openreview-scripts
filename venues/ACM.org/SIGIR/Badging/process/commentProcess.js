function(){
    var or3client = lib.or3client;

    var CONFERENCE_ID = 'ACM.org/SIGIR/Badging';
    var SHORT_PHRASE = "ACM SIGIR Badging";
    var PAPER_AUTHORS = CONFERENCE_ID + '/Paper' + note.number + '/Authors';
    var PAPER_REVIEWERS = CONFERENCE_ID + '/Paper' + note.number + '/Reviewers';
    var PROGRAM_CHAIRS = CONFERENCE_ID + '/Chairs';

    var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;

    Promise.all([
      forumNoteP,
      replytoNoteP
    ]).then(function(result) {

      var forumNote = result[0].notes[0];
      var author_mail;

      var reviewer_mail = {
        'groups': [CONFERENCE_ID + '/Paper' + forumNote.number + '/Reviewers'],
        'subject': 'Comment posted for a submission that you are reviewing. Title: ' + forumNote.content.title,
        'message': 'A comment was posted to a paper for which you are serving as reviewer.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var chair_mail = {
        'groups': [CONFERENCE_ID + '/Chairs'],
        'subject': 'A comment was posted for a submission for which you are the chair. Title: ' + forumNote.content.title,
        'message': 'A comment was posted to a paper with readership restricted to only the Program Chairs.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      author_mail = {
        "groups": forumNote.content.authorids,
        "subject": 'Your submission to ' + SHORT_PHRASE + ' has received a comment. Title: ' + forumNote.content.title,
        "message": 'Your submission to ' + SHORT_PHRASE + ' has received a comment.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var promises = [];

      if(note.readers.includes(PAPER_AUTHORS) || note.readers.includes('everyone')){
        promises.push(or3client.or3request(or3client.mailUrl, author_mail, 'POST', token));
      }

      if(note.readers.includes(PAPER_REVIEWERS) || note.readers.includes('everyone')){
        promises.push(or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token));
      }

      if(note.readers.includes(PAPER_AREACHAIRS) || note.readers.includes('everyone')){
        promises.push(or3client.or3request(or3client.mailUrl, ac_mail, 'POST', token));
      }

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
