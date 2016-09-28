function() {
  "use strict";
  var or3client = lib.or3client;
  var hashKey = or3client.createHash(note.content.email, "4813408173804203984");
  if(hashKey == note.content.key) {
    if (note.content.response == 'Yes') {
      or3client.removeGroupMember(invitation.signatures[0]+'/reviewers-declined', note.content.email, token)
      .then(result => or3client.addGroupMember(invitation.signatures[0]+'/reviewers', note.content.email, token))
      .then(result => done())
      .catch(error => console.log(error));
    } else if (note.content.response == 'No'){
      or3client.removeGroupMember(invitation.signatures[0]+'/reviewers', note.content.email, token)
      .then(result=> or3client.addGroupMember(invitation.signatures[0] + '/reviewers-declined', note.content.email, token))
      .then(result => done())
      .catch(error => console.log(error));
    }
    return true;
  } else {
    console.log('Invalid key', note.content.key);
    done();
    return false;
  }
}