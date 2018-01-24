function(){
    var or3client = lib.or3client;

    var CONFERENCEPHRASE = "ICLR 2018"

    var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
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
      origNoteP,
      replytoNoteP
    ]).then(function(result) {

      var origNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : [];
      var author_mail;

      var ac_mail = {
        'groups': ['ICLR.cc/2018/Conference/Paper' + origNote.number + '/Area_Chair'],
        'subject': 'Comment posted to a paper in your area. Title: ' + origNote.content.title,
        'message': 'A comment was posted to a paper for which you are serving as Area Chair.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var reviewer_mail = {
        'groups': ['ICLR.cc/2018/Conference/Paper' + origNote.number + '/Reviewers'],
        'subject': 'Comment posted to a paper you are reviewing. Title: ' + origNote.content.title,
        'message': 'A comment was posted to a paper for which you are serving as reviewer.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var pc_mail = {
        'groups': ['ICLR.cc/2018/Conference/Program_Chairs'],
        'subject': 'A Program Chair-only comment was posted',
        'message': 'A comment was posted to a paper with readership restricted to only the Program Chairs.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      author_mail = {
        "groups": origNote.content.authorids,
        "subject": "Your submission to " + CONFERENCEPHRASE + " has received a comment",
        "message": "Your submission to " + CONFERENCEPHRASE + " has received a comment.\n\nComment title: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum + '&noteId=' + note.id
      };

      var promises = [];

      if(checkReadersMatch(/ICLR.cc\/2018\/Conference\/Paper[0-9]+\/Authors_and_Higher/) ||
        checkReadersMatch(/everyone/)) {
        promises.push(or3client.or3request(or3client.mailUrl, author_mail, 'POST', token));
        promises.push(or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token));
        promises.push(or3client.or3request(or3client.mailUrl, ac_mail, 'POST', token));
      } else if(checkReadersMatch(/ICLR.cc\/2018\/Conference\/Paper[0-9]+\/Reviewers_and_Higher/)){
        promises.push(or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token));
        promises.push(or3client.or3request(or3client.mailUrl, ac_mail, 'POST', token));
      } else if(checkReadersMatch(/ICLR.cc\/2018\/Conference\/Paper[0-9]+\/Area_Chairs_and_Higher/)){
        promises.push(or3client.or3request(or3client.mailUrl, ac_mail, 'POST', token));
      } else if(note.readers.indexOf('ICLR.cc/2018/Conference/Program_Chairs') > -1){
        promises.push(or3client.or3request(or3client.mailUrl, pc_mail, 'POST', token));
      }

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
