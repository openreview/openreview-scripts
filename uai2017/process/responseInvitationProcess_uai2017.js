function() {

  var or3client = lib.or3client;
  var hashKey = or3client.createHash(note.content.email, "2810398440804348173");
  if(hashKey == note.content.key) {
    if (note.content.response == 'Yes') {
      console.log("Invitation replied Yes")
      //if a user is in the declined group, remove them from that group and add them to the reviewers group
      or3client.removeGroupMember('UAI.org/2017/conference/SrProgramCommittee/declined', note.content.email, token)
      or3client.addGroupMember('UAI.org/2017/conference/SrProgramCommittee', note.content.email, token)
      .then(function(result) {
        var message = "The user " + note.content.email + " has accepted the invitation to serve as a reviewer."
        //return or3client.or3request(or3client.mailUrl, { groups: [invitation.signatures[0]], subject: "OpenReview invitation accepted" , message: message}, 'POST', token);
      })
      .then(result => done())
      .catch(error => console.log(error));
    } else if (note.content.response == 'No'){
      console.log("Invitation replied No")
      //if a user is in the reviewers group, remove them from that group and add them to the reviewers-declined group
      or3client.removeGroupMember('UAI.org/2017/conference/SrProgramCommittee', note.content.email, token)
      or3client.addGroupMember('UAI.org/2017/conference/SrProgramCommittee/declined', note.content.email, token)
      .then(function(result) {
        var message = "The user " + note.content.email + " has rejected the invitation to serve as a reviewer."
        //return or3client.or3request(or3client.mailUrl, { groups: [invitation.signatures[0]], subject: "OpenReview invitation rejected" , message: message}, 'POST', token);
      })
      .then(result => done())
      .catch(error => console.log(error));
    }
    return true;
  } else {
    console.log('Invalid key', note.content.key);
    return false;
  }
}
