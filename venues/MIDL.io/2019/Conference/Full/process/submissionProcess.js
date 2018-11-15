function () {
  var or3client = lib.or3client;

  var SHORT_PHRASE = 'MIDL 2019 Conference Full Paper';
  var CONFERENCE_ID = 'MIDL.io/2019/Conference/Full';

    // send author a confirmation email
  var author_mail = {
    groups: note.content.authorids,
    subject: 'Your submission to ' + SHORT_PHRASE + ' has been received: "' + note.content.title + '"',
    message: 'Your submission to ' + SHORT_PHRASE + ' has been posted.\n\nTitle: ' + note.content.title + '\n\nAbstract: ' + note.content.abstract + '\n\nTo view your submission, click here: ' + baseUrl + '/forum?id=' + note.forum
  };

    // create revision invitation
  var revisionInvitation = {
        id: CONFERENCE_ID + '/-/Paper'+note.number+'/Add/Revision',
        readers: ['everyone'],
        writers: [CONFERENCE_ID],
        invitees: note.content['authorids'],
        signatures: [CONFERENCE_ID],
        duedate: invitation.duedate,
        reply: {
            referent: note.id,
            forum: note.forum,
            content: invitation.reply.content,
            signatures: invitation.reply.signatures,
            writers: invitation.reply.writers,
            readers: invitation.reply.readers
        }
   };
   var commentInvitation = {
        id: CONFERENCE_ID + '/-/Paper'+note.number+'/Pams_Comment',
        readers: ['everyone'],
        writers: [CONFERENCE_ID],
        invitees: ['~'],
        signatures: [CONFERENCE_ID],
        reply: {
            forum: note.forum,
            content: = {
                'title': {
                    'order': 0,
                    'value-regex': '.{1,500}',
                    'description': 'Brief summary of your comment.',
                    'required': True
                },
                'comment': {
                    'order': 1,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Your comment or reply (max 5000 characters).',
                    'required': True
                }
            }
            signatures: = {
                'description': 'Your authorized identity to be associated with the above content.',
                'values-regex': '~.*'
            },
            writers: [CONFERENCE_ID],
            readers: ['everyone'],
            nonreaders: [CONFERENCE_ID+'/Paper'+note.number+'/Reviewers']
        }
   };

  return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token)
  .then(result => or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token))
  .then(result => done())
  .catch(error => done(error));

  return true;
};
