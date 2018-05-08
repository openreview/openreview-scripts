function() {
  var or3client = lib.or3client;

  var CONFERENCE_ID = 'ICML.cc/2018/Workshop/NAMPI'
  var PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'
  var REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'
  var REVIEWERS_INVITE_ID = REVIEWERS_ID + '/Invited'
  var REVIEWERS_DECLINE_ID = REVIEWERS_ID + '/Declined'
  var HASH_SEED = "2810398440804348173"

  var hashKey = or3client.createHash(note.content.email, HASH_SEED);

  if(hashKey == note.content.key) {
    if (note.content.response == 'Yes') {
      console.log("Invitation replied Yes")
      //if a user is in the declined group, remove them from that group and add them to the reviewers group
      or3client.removeGroupMember(REVIEWERS_DECLINE_ID, note.content.email, token);
      or3client.addGroupMember(REVIEWERS_ID, note.content.email, token)
      .then(result => done())
      .catch(error => done(error));
    } else if (note.content.response == 'No'){
      console.log("Invitation replied No")
      //if a user is in the reviewers group, remove them from that group and add them to the reviewers-declined group
      or3client.removeGroupMember(REVIEWERS_ID, note.content.email, token)
      or3client.addGroupMember(REVIEWERS_DECLINE_ID, note.content.email, token)
      .then(result => done())
      .catch(error => done(error));
    } else {
      done('Invalid response', note.content.response);
    }
    return true;
  } else {
    done('Invalid key', note.content.key);
    return false;
  }
}
