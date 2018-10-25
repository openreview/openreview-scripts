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

  var commentInvitation = {
    id: CONF + '/-/Paper' + note.number + '/Comment',
    signatures: [CONF],
    writers: [CONF],
    invitees: ['everyone'],
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
    }
  }

  var reviewInvitation = {
    id: CONF + '/-/Paper' + note.number + '/Review',
    signatures: [CONF],
    writers: [CONF],
    invitees: [],
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
        comment: {
          order: 1,
          'value-regex': '[\\S\\s]{1,5000}',
          description: 'Your review.',
          required: true
        }
      }
    }
  }


  or3client.or3request(or3client.mailUrl, authorMail, 'POST', token)
  .then(result => or3client.or3request(or3client.inviteUrl, commentInvitation, 'POST', token))
  .then(result => or3client.or3request(or3client.inviteUrl, reviewInvitation, 'POST', token))
  .then(result => done())
  .catch(error => done(error));
  return true;
};
