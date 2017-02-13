function() {

  var or3client = lib.or3client;
  var hashKey = or3client.createHash(note.content.username, "2810398440804348173");
  if(hashKey == note.content.key) {
    if (note.content.response == 'Yes') {
      console.log("Invitation replied Yes");
      //if a user is in the declined group, remove them from that group and add them to the reviewers group
      or3client.removeGroupMember('auai.org/UAI/2017/Program_Committee/declined', note.content.username, token)
      .then(function(result){
        return or3client.addGroupMember('auai.org/UAI/2017/Program_Committee', note.content.username, token);
      })
      .then(function(result) {
        return "The user " + note.content.username + " has accepted the invitation to serve as a reviewer.";
      })
      .then(result => done())
      .catch(error => done(error));
    } else if (note.content.response == 'No'){
      console.log("Invitation replied No");
      //if a user is in the reviewers group, remove them from that group and add them to the reviewers-declined group
      or3client.removeGroupMember('auai.org/UAI/2017/Program_Committee', note.content.username, token)
      .then(function(result){
        return or3client.addGroupMember('auai.org/UAI/2017/Program_Committee/declined', note.content.username, token);
      })
      .then(function(result) {
        return "The user " + note.content.username + " has rejected the invitation to serve as a reviewer.";
      })
      .then(result => done())
      .catch(error => done(error));
    }
    return true;
  } else {
    done('Invalid key: ',note.content.key);
    return false;
  }
}
