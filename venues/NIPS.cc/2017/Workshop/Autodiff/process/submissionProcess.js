function () {
  var or3client = lib.or3client;

  var CONFERENCEPHRASE = "NIPS 2017 Autodiff Workshop";
  var CONF = "NIPS.cc/2017/Workshop/Autodiff";

    // send author a confirmation email
  var author_mail = {
    "groups": note.content.authorids,
    "subject": "Your submission to "+ CONFERENCEPHRASE +" has been received: \"" + note.content.title + "\"",
    "message": "Your submission to "+ CONFERENCEPHRASE + " has been posted.\n\nTitle: " + note.content.title + "\n\nAbstract: " + note.content.abstract + "\n\nTo view your submission, click here: " + baseUrl+"/forum?id=" + note.forum
  };

    // create revision invitation
  var revisionInvitation = {
        id: CONF + '/-/Paper'+note.number+'/Add/Revision',
        readers: ['everyone'],
        writers: [CONF],
        invitees: note.content['authorids'],
        signatures: [CONF],
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
  return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token)
  .then(result => or3client.or3request(or3client.inviteUrl, revisionInvitation, 'POST', token))
  .then(result => done())
  .catch(error => done(error));

  return true;
};
