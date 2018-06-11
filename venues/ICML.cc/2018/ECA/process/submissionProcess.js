function () {
  var or3client = lib.or3client;

  var SHORT_PHRASE = 'ICML ECA 2018';
  var CONFERENCE_ID = 'ICML.cc/2018/ECA';
  var PROGRAM_CHAIRS = CONFERENCE_ID+'/Program_Chairs'

    // send author a confirmation email
  var author_mail = {
    groups: note.content.authorids,
    subject: 'Your submission to ' + SHORT_PHRASE + ' has been received: "' + note.content.title + '"',
    message: 'Your submission to ' + SHORT_PHRASE + ' has been posted.\n\nTitle: ' + note.content.title + '\n\nAbstract: ' + note.content.abstract + '\n\nTo view your submission, click here: ' + baseUrl + '/forum?id=' + note.forum
  };

    // create revision invitation
  var revisionInvitation = {
        id: CONFERENCE_ID + '/-/Paper'+note.number+'/Add_Revision',
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
            readers: { values: note.readers },
        }
   };

  // create paper group, authors group and Authors_and_Committee group for this paper
  var paperGroup = {
    id: CONFERENCE_ID + '/Paper' + note.number,
    signatures: [CONFERENCE_ID],
    writers: [CONFERENCE_ID],
    members: [],
    readers: [CONFERENCE_ID],
    signatories: []
  };
  return or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token)
  .then(savedPaperGroup => {
    var reviewerGroupId = savedPaperGroup.id + '/Reviewers';
    var authorGroupId = savedPaperGroup.id + '/Authors';
    var authorGroup = {
      id: authorGroupId,
      signatures: [CONFERENCE_ID],
      writers: [CONFERENCE_ID],
      members: note.content.authorids.concat(note.signatures),
      readers: [CONFERENCE_ID, PROGRAM_CHAIRS, authorGroupId],
      signatories: [authorGroupId]
    };
    var authorPlusGroupId = authorGroupId+'_and_Committee';
    var authorPlusGroup = {
      id: authorPlusGroupId,
      signatures: [CONFERENCE_ID],
      writers: [CONFERENCE_ID],
      members: [CONFERENCE_ID, PROGRAM_CHAIRS, authorGroupId, reviewerGroupId],
      readers: [CONFERENCE_ID, PROGRAM_CHAIRS, authorGroupId, reviewerGroupId],
      signatories: [authorPlusGroupId]
    };

    var promises = [
      or3client.or3request(or3client.mailUrl, author_mail, 'POST', token),
      or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token),
      or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
      or3client.or3request(or3client.grpUrl, authorPlusGroup, 'POST', token)];

    if (note.readers[0] == 'ICML.cc/2018/ECA/Authors_and_Committee') {
        note.readers = [authorPlusGroupId];
        promises.push(or3client.or3request(or3client.notesUrl, note, 'POST', token));
    }
    return Promise.all(promises);
    })
  .then(result => done())
  .catch(error => done(error));

  return true;
};
