function(){
  var or3client = lib.or3client;
  var mailP = or3client.emailToAuthors(note, token);
  var fulfilledP = or3client.fulfillInvitation(invitation, note, token);
  return true;
};