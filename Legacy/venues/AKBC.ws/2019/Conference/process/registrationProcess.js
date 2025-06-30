function () {
  var or3client = lib.or3client;

  or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token)
  .then(result => done())
  .catch(error => done(error));
  return true;
};
