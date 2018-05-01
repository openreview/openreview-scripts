function(){
    var or3client = lib.or3client;

    var CONFERENCEPHRASE = "UAI 2018"

    var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;

    var checkReadersMatch = function(regex) {
      for(reader of note.readers){
        if(reader.match(regex)){
          return true;
        }
      }
      return false;
    };

    Promise.all([
      forumNoteP,
      replytoNoteP
    ]).then(function(result) {

      var forumNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : [];
      var author_mail;

      var areachairs_group_id = 'auai.org/UAI/2018/Paper' + forumNote.number + '/Area_Chairs';
      var reviewers_group_id = 'auai.org/UAI/2018/Paper' + forumNote.number + '/Reviewers';
      var pc_group_id = 'auai.org/UAI/2018/Program_Chairs';
      var ac_mail = {
        'groups': [areachairs_group_id],
        'subject': 'Comment posted to a paper in your area. Title: ' + forumNote.content.title,
        'message': 'A comment was posted to a paper for which you are serving as Area Chair.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var reviewer_mail = {
        'groups': [reviewers_group_id],
        'subject': 'Comment posted to a paper you are reviewing. Title: ' + forumNote.content.title,
        'message': 'A comment was posted to a paper for which you are serving as reviewer.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var pc_mail = {
        'groups': [pc_group_id],
        'subject': 'A Program Chair-only comment was posted',
        'message': 'A comment was posted directed at the Program Chairs.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      author_mail = {
        "groups": forumNote.content.authorids,
        "subject": "Your submission to " + CONFERENCEPHRASE + " has received a comment",
        "message": "Your submission to " + CONFERENCEPHRASE + " has received a comment.\n\nComment title: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum + '&noteId=' + note.id
      };

      var promises = [];

      if (checkReadersMatch(/auai.org\/UAI\/2018\/Paper[0-9]+\/All_Users/)) {
        promises.push(or3client.or3request(or3client.mailUrl, author_mail, 'POST', token));
        promises.push(or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token));
        promises.push(or3client.or3request(or3client.mailUrl, ac_mail, 'POST', token));
      } else {
        if (checkReadersMatch(/auai.org\/UAI\/2018\/Paper[0-9]+\/Reviewers/)){
          promises.push(or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token));
        }
        if (checkReadersMatch(/auai.org\/UAI\/2018\/Paper[0-9]+\/Area_Chairs/)){
          promises.push(or3client.or3request(or3client.mailUrl, ac_mail, 'POST', token));
        }
        if(note.readers.indexOf('auai.org/UAI/2018/Program_Chairs') > -1){
          promises.push(or3client.or3request(or3client.mailUrl, pc_mail, 'POST', token));
        }
      }

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
