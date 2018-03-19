function(){
    var or3client = lib.or3client;

    var CONFERENCEPHRASE = "ICLR 2018"

    var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;

    Promise.all([
      origNoteP,
      replytoNoteP
    ]).then(function(result) {

      var origNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : [];
      var author_mail;

      var selfComment = replytoNoteSignatures.indexOf(note.signatures[0]) > -1;
      if(selfComment){
        console.log('self comment detected');
      }

      var readableComment = true;

      //make sure that all readers in note.readers is also in replytoNotes.readers

      for(var i=0; i<note.readers.length; i++){
        if(!replytoNote.readers.includes(note.readers[i])) {
          readableComment = false;
        }
      };

      var reviewer_mail = {
        'groups': ['ICLR.cc/2018/Workshop/Paper' + origNote.number + '/Reviewers'],
        'subject': 'Comment posted to a paper you are reviewing. Title: ' + origNote.content.title,
        'message': 'A comment was posted to a paper for which you are serving as reviewer.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var pc_mail = {
        'groups': ['ICLR.cc/2018/Workshop/Program_Chairs'],
        'subject': 'A Program Chair-only comment was posted',
        'message': 'A comment was posted to a paper with readership restricted to only the Program Chairs.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var promises = [];

      if(note.readers.indexOf('ICLR.cc/2018/Conference/Reviewers_and_Higher') > -1 ||
        note.readers.indexOf('ICLR.cc/2018/Conference/Authors_and_Higher') > -1 ||
        note.readers.indexOf('everyone') > -1){
        promises.push(or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token));
      } else if(note.readers.indexOf('ICLR.cc/2018/Workshop/Program_Chairs') > -1){
        promises.push(or3client.or3request(or3client.mailUrl, pc_mail, 'POST', token));
      }

      if(!selfComment && readableComment){
        if(replytoNote.id == origNote.id){
          author_mail = {
            "groups": origNote.content.authorids,
            "subject": "Your submission to " + CONFERENCEPHRASE + " has received a comment",
            "message": "Your submission to " + CONFERENCEPHRASE + " has received a comment.\n\nComment title: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum + '&noteId=' + note.id
          };
        } else {
          author_mail = {
            "groups": replytoNote.signatures == '(anonymous)' ? [] : replytoNote.signatures,
            "subject": "Your comment has received a response",
            "message": "Your comment titled \"" + replytoNote.content.title + "\" has received a response.\n\nComment title: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum + '&noteId=' + note.id
          };
        }
        promises.push(or3client.or3request(or3client.mailUrl, author_mail, 'POST', token));
      }

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
