function () {
  var or3client = lib.or3client;

  var SHORT_PHRASE = 'MIDL 2019 Conference Full Paper';
  var CONFERENCE_ID = 'MIDL.io/2019/Conference/Full';
  var PROGRAM_CHAIRS = 'MIDL.io/2019/Conference/Program_Chairs';
  var SAVED_PAPER_ID = CONFERENCE_ID + '/-/Paper'+note.number;
    // send author a confirmation email
  var author_mail = {
    groups: note.content.authorids,
    subject: 'Your submission to ' + SHORT_PHRASE + ' has been received: "' + note.content.title + '"',
    message: 'Your submission to ' + SHORT_PHRASE + ' has been posted.\n\nTitle: ' + note.content.title + '\n\nAbstract: ' + note.content.abstract + '\n\nTo view your submission, click here: ' + baseUrl + '/forum?id=' + note.forum
  };

    // create revision invitation
  var revisionInvitation = {
        id: SAVED_PAPER_ID+'/Add_Revision',
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

  var paperGroup = {
        id: CONFERENCE_ID + '/Paper'+note.number,
        signatures: [CONFERENCE_ID],
        writers: [CONFERENCE_ID],
        members: [],
        readers: [CONFERENCE_ID],
        signatories: []
      };

  var authorGroupId = CONFERENCE_ID + '/Paper'+note.number+'/Authors';
  var authorGroup = {
      id: authorGroupId,
      signatures: [CONFERENCE_ID],
      writers: [CONFERENCE_ID],
      members: note.content['authorids'].concat(note.signatures),
      readers: [CONFERENCE_ID, PROGRAM_CHAIRS, authorGroupId],
      signatories: [authorGroupId]
  };

  var commentInvitation = {
        id: SAVED_PAPER_ID+'/Comment',
        readers: ['everyone'],
        writers: [CONFERENCE_ID],
        invitees: ['~'],
        signatures: [CONFERENCE_ID],
        reply: {
            forum: note.forum,
            content: {
                'title': {
                    'order': 0,
                    'value-regex': '.{1,500}',
                    'description': 'Brief summary of your comment.',
                    'required': true
                },
                'comment': {
                    'order': 1,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Your comment or reply (max 5000 characters).',
                    'required': true
                }
            },
            signatures: {
                'description': 'Your authorized identity to be associated with the above content.',
                'values-regex': '~.*'
            },
            writers: {'values-regex':'~.*'},
            readers: {
                'description': 'The users who will be allowed to read the above content.',
                'values': [PROGRAM_CHAIRS, CONFERENCE_ID + '/Paper'+note.number+'/Area_Chairs', authorGroupId]
             }

        }
   };

  return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token)
  .then(result => or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token))
  .then(result => or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token))
  .then(result => or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token))
  .then(result => or3client.or3request(or3client.inviteUrl, commentInvitation, 'POST', token))
  .then(result => done())
  .catch(error => done(error));

  return true;
};
