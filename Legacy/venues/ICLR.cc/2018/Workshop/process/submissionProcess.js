function() {
  var or3client = lib.or3client;

  var CONF = 'ICLR.cc/2018/Workshop';
  var PROGRAM_CHAIRS = CONF + '/Program_Chairs';
  var AUTHORS = CONF + '/Authors';

  var getBibtex = function(note) {
    var firstWord = note.content.title.split(' ')[0].toLowerCase();

    return '@article{\
        \nanonymous2018' + firstWord + ',\
        \ntitle={' + note.content.title + '},\
        \nauthor={Anonymous},\
        \njournal={Submission to International Conference on Learning Representations 2018: Workshop Track},\
        \nyear={2018}\
    \n}'
  };


  var addRevisionInvitation = {
    id: CONF + '/-/Paper' + note.number + '/Add_Revision',
    signatures: [CONF],
    writers: [CONF],
    invitees: note.content.authorids.concat(note.signatures),
    noninvitees: [],
    readers: ['everyone'],
    reply: {
      forum: note.id,
      referent: note.id,
      signatures: invitation.reply.signatures,
      writers: invitation.reply.writers,
      readers: invitation.reply.readers,
      content: invitation.reply.content
    }
  }

  //Send an email to the author of the submitted note, confirming its receipt
  var mail = {
      "groups": note.content.authorids,
      "subject": "Confirmation of your submission to ICLR 2018: \"" + note.content.title + "\".",
      "message": `Your submission to ICLR 2018 has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
  };

  var paperGroup = {
    id: CONF + '/Paper' + note.number,
    signatures: [CONF],
    writers: [CONF],
    members: [],
    readers: [CONF],
    signatories: []
  };

  or3client.or3request(or3client.mailUrl, mail, 'POST', token)
  .then(result => {
    return or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token);
  })
  .then(group_result => {
    var authorGroupId = group_result.id + '/Authors';
    var authorGroup = {
      id: authorGroupId,
      signatures: [CONF],
      writers: [CONF],
      members: note.content.authorids.concat(note.signatures),
      readers: [CONF, 'everyone'],
      signatories: [authorGroupId]
    };
    return or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token);
  })
  .then(result => {
    return or3client.or3request(or3client.inviteUrl, addRevisionInvitation, 'POST', token);
  })
  .then(result => done())
  .catch(error => done(error));

  return true;
}
