function() {
  var or3client = lib.or3client;
  console.log('submission process');

  var SHORT_PHRASE = 'ACM SIGIR Badging';
  var CONF = 'ACM.org/SIGIR/Badging';

  var authorMail = {
    groups: note.content.authorids,
    subject: 'Your submission to ' + SHORT_PHRASE + ' has been received: ' + note.content.title,
    message: 'Your submission to ' + SHORT_PHRASE + ' has been posted.\n\nTitle: ' + note.content.title + '\n\nTo view your submission, click here: ' + baseUrl + '/forum?id=' + note.forum
  };


  var commentProcess = function(){
    var or3client = lib.or3client;

    var SHORT_PHRASE = 'ACM SIGIR Badging';
    var CONF = 'ACM.org/SIGIR/Badging';
    var Conf_Chairs = CONF + '/Chairs';
    var Conf_Reviewers = CONF + '/Reviewers';

    or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
    .then(function(result) {
      var forumNote = result.notes[0];

      var reviewer_mail = {
        'groups': [Conf_Reviewers],
        'subject': '[' + SHORT_PHRASE + '] Comment posted to a paper you are reviewing. Paper Number: ' + forumNote.number + ', Paper Title: \"' + forumNote.content.title + '\"',
        'message': 'A comment was posted to a paper for which you are serving as reviewer.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var pc_mail = {
        'groups': [Conf_Chairs],
        'subject': '[' + SHORT_PHRASE + '] A comment was posted. Paper Number: ' + forumNote.number + ', Paper Title: \"' + forumNote.content.title + '\"',
        'message': 'A comment was posted.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      author_mail = {
        'groups': forumNote.content.authorids,
        'subject': '[' + SHORT_PHRASE + '] Your submission to ' + SHORT_PHRASE + ' has received a comment. Paper Title: \"' + forumNote.content.title + '\"',
        'message': 'Your submission to ' + SHORT_PHRASE + ' has received a comment.\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
      };

      var promises = [];

      promises.push(or3client.or3request(or3client.mailUrl, author_mail, 'POST', token));
      promises.push(or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token));
      promises.push(or3client.or3request(or3client.mailUrl, pc_mail, 'POST', token));
      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };

  var commentInvitation = {
    id: CONF + '/-/Paper' + note.number + '/Comment',
    signatures: [CONF],
    writers: [CONF],
    invitees: ['~'],
    readers: ['everyone'],
    reply: {
      forum: note.id,
      replyto: null,
      readers: {
        description: 'The users who will be allowed to read the above content.',
        'values': ['everyone']
      },
      signatures: {
        description: 'How your identity will be displayed with the above content.',
        'values-regex': '~.*'
      },
      writers: {
        'values-regex': '~.*'
      },
      content:{
        title: {
          order: 0,
          'value-regex': '.{1,500}',
          description: 'Brief summary of your comment.',
          required: true
        },
        comment: {
          order: 1,
          'value-regex': '[\\S\\s]{1,5000}',
          description: 'Your comment or reply.',
          required: true
        }
      }
    },
    process: commentProcess + ''
  };

  var Conf_Chairs = CONF + '/Chairs';
  var Conf_Reviewers = CONF + '/Reviewers';
  var reviewProcess = function(){
    var or3client = lib.or3client;

    var CONF = 'ACM.org/SIGIR/Badging';
    var SHORT_PHRASE = 'ACM SIGIR Badging';
    var CONF_CHAIRS = 'ACM.org/SIGIR/Badging/Chairs';

    var forumNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    forumNote.then(function(result) {
      var forum = result.notes[0];

      var chair_mail = {
        'groups': [CONF_CHAIRS],
        'subject': 'Review posted to a paper: \"' + forum.content.title + '\"',
        'message': 'A submission to ' + SHORT_PHRASE + ' has received a review. \n\nTitle: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the review, click here: ' + baseUrl + '/forum?id=' + note.forum
      };

      return chairMailP = or3client.or3request( or3client.mailUrl, chair_mail, 'POST', token );
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };

  var reviewInvitation = {
    id: CONF + '/-/Paper' + note.number + '/Review',
    duedate: 1575732251000,
    signatures: [CONF],
    writers: [CONF, Conf_Chairs],
    invitees: [Conf_Reviewers],
    readers: ['everyone'],
    reply: {
      forum: note.id,
      replyto: note.id,
      readers: {
        description: 'The users who will be allowed to read the above content.',
        'values': ['everyone']
      },
      signatures: {
        description: 'How your identity will be displayed with the above content.',
        'values-regex': '~.*'
      },
      writers: {
        'values-regex': '~.*'
      },
      content:{
        title: {
          order: 0,
          'value-regex': '.{1,500}',
          description: 'Brief summary of your review.',
          required: true
        },
        'awarded badges': {
          'description': 'Please select all the badges that you are awarding to this artifact.',
          'order': 1,
          'values-dropdown': [
              'No Badges',
              'Artifacts Available',
              'Artifacts Evaluated – Functional and Reusable',
              'Results Replicated',
              'Results Reproduced'
          ],
          'required': true
        },
        comment: {
          order: 2,
          'value-regex': '[\\S\\s]{1,5000}',
          description: 'Your review comment.',
          required: false
        }
      }
    },
    process: reviewProcess + ''
  };


  or3client.or3request(or3client.mailUrl, authorMail, 'POST', token)
  .then(result => or3client.or3request(or3client.inviteUrl, commentInvitation, 'POST', token))
  .then(result => or3client.or3request(or3client.inviteUrl, reviewInvitation, 'POST', token))
  .then(result => done())
  .catch(error => done(error));
  return true;
};
