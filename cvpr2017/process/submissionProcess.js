function () {
  var or3client = lib.or3client;

  var CONFERENCE = 'cv-foundation.org/CVPR/2017/BNMW'
  var PAPERINV = CONFERENCE+'/-/Paper' + note.number;

  var commentProcess = function(){
    var or3client = lib.or3client;

    var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;

    Promise.all([
      origNoteP,
      replytoNoteP
    ]).then(function(result) {

      var origNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;

      var author_mail;

      if(replytoNote.id == origNote.id){
        author_mail = {
          "groups": origNote.content.authorids,
          "subject": "Your submission to CVPR 2017 Workshop (BNMW) has received a comment",
          "message": "Your submission to the Brave New Motion Representations workshop has received a comment.\n\nComment title: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl+"/forum?id=" + note.forum +'&noteId='+note.id
        };
      } else {
        author_mail = {
          "groups": replytoNote.signatures == '(anonymous)' ? [] : replytoNote.signatures,
          "subject": "Your comment has received a response",
          "message": "Your comment titled \""+replytoNote.content.title+"\" has received a response.\n\nComment title: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl+"/forum?id=" + note.forum +'&noteId='+note.id
        };
      }

      promises = [or3client.or3request(or3client.mailUrl, author_mail, 'POST', token)];

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };


  var openCommentInvite = {
    'id': PAPERINV + '/Open/Comment',
    'signatures': [CONFERENCE],
    'writers': [CONFERENCE],
    'invitees': ['~'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': commentProcess + '',
    'reply': {
      'forum': note.forum,      // links this note (comment) to the previously posted note (paper)
      'signatures': {
        'values-regex': '~.*|\\(anonymous\\)',
        'description': 'How your identity will be displayed with the above content.'
        },
      'writers': { 'values-regex': '~.*|\\(anonymous\\)' },
      'readers': {
        'values': ['everyone'],
        'description': 'The users who will be allowed to read the above content.'
      },
      'content': {
        'title': {
          'order': 1,
          'value-regex': '.{1,500}',
          'description': 'Brief summary of your comment.',
          'required':true
        },
        'comment': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your comment or reply.',
          'required':true
        }
      }
    }
  };

  var author_mail = {
    "groups": note.content.authorids,
    "subject": "Your submission to CVPR 2017 Workshop (BNMW) has been received: \"" + note.content.title + "\"",
    "message": "Your submission to the Brave New Motion Representations workshop has been posted.\n\nTitle: " + note.content.title + "\n\nAbstract: " + note.content.abstract + "\n\nTo view your submission, click here: " + baseUrl+"/forum?id=" + note.forum
  };

  return or3client.or3request(or3client.inviteUrl, openCommentInvite, 'POST', token)
  .then(result => or3client.or3request(or3client.mailUrl, author_mail, 'POST', token))
  .then(result => done())
  .catch(error => done(error));

  return true;
};
