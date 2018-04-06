function () {
  var or3client = lib.or3client;

  //<CONSTANTS>
  //<TITLE>
  //<SUBTITLE>
  //<LOCATION>
  //<DATE>
  //<WEBSITE>
  //<DEADLINE>
  //<CONFERENCE>
  //<PROGRAM_CHAIRS>
  //<REVIEWERS>
  //<AREA_CHAIRS>
  //<SUBMISSION_INVITATION>
  //<BLIND_INVITATION>
  //<RECRUIT_REVIEWERS>

  var PAPER_GROUP = CONFERENCE + '/Paper' + note.number
  var PAPER_AUTHORS = PAPER_GROUP + '/Authors';

  var revisionInvitation = {
    id: CONFERENCE + '/-/Paper' + note.number + '/Add_Revision',
    readers: ['everyone'],
    writers: [CONFERENCE],
    invitees: note.content['authorids'],
    signatures: [CONFERENCE],
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
  or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token)
  .then(result=> {
    var paperGroup = {
      id: PAPER_GROUP,
      readers: [CONFERENCE],
      writers: [CONFERENCE],
      members: [],
      signatories: [],
      signatures: [CONFERENCE]
    }
    return or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token);
  })
  .then(result => {
    var authorGroup = {
      id: PAPER_AUTHORS,
      readers: [CONFERENCE, PAPER_AUTHORS],
      writers: [CONFERENCE],
      members: note.content.authorids,
      signatories: [PAPER_AUTHORS],
      signatures: [CONFERENCE]
    };
    return or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token);
  })
  .then(result => { console.log(JSON.stringify(result));
    var blindSubmission = {
      original: note.id,
      invitation: BLIND_INVITATION,
      forum: null,
      parent: null,
      signatures: [CONFERENCE],
      writers: [CONFERENCE],
      readers: ['everyone'],
      content: {
        authors: ['Anonymous'],
        authorids: [PAPER_AUTHORS],
      }
    };
    return or3client.or3request(or3client.notesUrl, blindSubmission, 'POST', token);
  })
  .then(result => { console.log(JSON.stringify(result));
    var authorMail = {
      groups: note.content.authorids,
      subject: 'Your submission to '+ TITLE + ' has been received: ' + note.content.title,
      message: 'Your submission to '+ TITLE + ' has been posted.\n\nTitle: ' + note.content.title + '\n\nAbstract: ' + note.content.abstract + '\n\nTo view your submission, click here: ' + baseUrl + '/forum?id=' + result.forum
    };
    return or3client.or3request(or3client.mailUrl, authorMail, 'POST', token);
  })
  .then(result => done())
  .catch(error => done(error));
  return true;
};
