function() {

  var or3client = lib.or3client;
  var hashKey = or3client.createHash(note.content.email, invitation.id);
  if(hashKey == note.content.key) {
    if (note.content.response == 'Yes') {
      console.log("Invitation replied Yes")
      //if a user is in the declined group, remove them from that group and add them to the reviewers group
      or3client.removeGroupMember(invitation.signatures[0]+'/reviewers-declined', note.content.email, token)
      or3client.addGroupMember(invitation.signatures[0]+'/reviewers', note.content.email, token)
      .then(function(result) {
        var message = "The user " + note.content.email + " has accepted the invitation to do the review process."
        return or3client.or3request(or3client.mailUrl, { groups: [invitation.signatures[0]], subject: "OpenReview invitation accepted" , message: message}, 'POST', token);
      })
      .catch(error => console.log(error));
    } else if (note.content.response == 'No'){
      console.log("Invitation replied No")
      //if a user is in the reviewers group, remove them from that group and add them to the reviewers-declined group
      or3client.removeGroupMember(invitation.signatures[0]+'/reviewers', note.content.email, token)
      or3client.addGroupMember(invitation.signatures[0] + '/reviewers-declined', note.content.email, token)
      .then(function(result) {
        var message = "The user " + note.content.email + " has rejected the invitation to do the review process."
        return or3client.or3request(or3client.mailUrl, { groups: [invitation.signatures[0]], subject: "OpenReview invitation rejected" , message: message}, 'POST', token);
      })  
      .catch(error => console.log(error));
    }
    return true;
  } else {
    console.log('Invalid key', note.content.key);
    return false;
  }
}