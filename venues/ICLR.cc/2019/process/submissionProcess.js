function() {
  var or3client = lib.or3client;
  console.log('submission process');

  var SHORT_PHRASE = 'ICLR 2019';
  var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
  var PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs';
  var REVIEWERS_ID = CONFERENCE_ID + '/Reviewers';
  var AREA_CHAIRS_ID = CONFERENCE_ID + '/Area_Chairs';
  var BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission';

  var PAPER_GROUP_ID = CONFERENCE_ID + '/Paper' + note.number;
  var PAPER_AUTHORS_ID = PAPER_GROUP_ID + '/Authors';

  console.log('constants declared');

  var revisionInvitation = {
    id: CONFERENCE_ID + '/-/Paper' + note.number + '/Add_Revision',
    readers: ['everyone'],
    writers: [CONFERENCE_ID],
    invitees: [],
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
  or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token)
  .then(result=> {
    console.log('revision invitation posted');
    var paperGroup = {
      id: PAPER_GROUP_ID,
      readers: [CONFERENCE_ID],
      writers: [CONFERENCE_ID],
      members: [],
      signatories: [],
      signatures: [CONFERENCE_ID]
    }
    return or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token);
  })
  .then(result => {
    console.log('papergroup posted');
    var authorGroup = {
      id: PAPER_AUTHORS_ID,
      readers: [CONFERENCE_ID, PAPER_AUTHORS_ID],
      writers: [CONFERENCE_ID],
      members: note.content.authorids,
      signatories: [PAPER_AUTHORS_ID],
      signatures: [CONFERENCE_ID]
    };
    return or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token);
  })
  .then(result => { console.log(JSON.stringify(result));
    console.log('author group posted');
    var blindSubmission = {
      original: note.id,
      invitation: BLIND_SUBMISSION_ID,
      forum: null,
      parent: null,
      signatures: [CONFERENCE_ID],
      writers: [CONFERENCE_ID],
      readers: ['everyone'],
      content: {
        authors: ['Anonymous'],
        authorids: [CONFERENCE_ID + '/Paper' + note.number + '/Authors'],
      }
    };
    return or3client.or3request(or3client.notesUrl, blindSubmission, 'POST', token);
  })
  .then(result => { console.log(JSON.stringify(result));
    console.log('blind note posted');
    var authorMail = {
      groups: note.content.authorids,
      subject: 'Your submission to ' + SHORT_PHRASE + ' has been received: ' + note.content.title,
      message: 'Your submission to ' + SHORT_PHRASE + ' has been posted.\n\nTitle: ' + note.content.title + '\n\nAbstract: ' + note.content.abstract + '\n\nTo view your submission, click here: ' + baseUrl + '/forum?id=' + result.forum
    };
    return or3client.or3request(or3client.mailUrl, authorMail, 'POST', token);
  })
  .then(result => done())
  .catch(error => done(error));
  return true;
};
