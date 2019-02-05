function() {
  var or3client = lib.or3client;

  var individualGroupId = note.invitation.split('/-/')[0];
  var reviewersDeclinedGroupId = individualGroupId + '/Reviewers_Declined';
  var reviewersGroupId = individualGroupId + '/Reviewers';
  var HASH_SEED = '1234';

  var hashKey = or3client.createHash(note.content.email, HASH_SEED);
  var removeGroupId = '';
  var addGroupId = '';

  if (hashKey == note.content.key) {
    if (note.content.response == 'Yes') {
      console.log("Invitation replied Yes")
      removeGroupId = reviewersDeclinedGroupId;
      addGroupId = reviewersGroupId;
    } else if (note.content.response == 'No'){
      console.log("Invitation replied No")
      removeGroupId = reviewersGroupId;
      addGroupId = reviewersDeclinedGroupId;
    } else {
      return done('Invalid response: ' + note.content.response);
    }
  } else {
    done('Invalid key: ' + note.content.key);
  }

  or3client.removeGroupMember(removeGroupId, note.content.email, token)
  .then(result => or3client.addGroupMember(addGroupId, note.content.email, token))
  .then(result => done())
  .catch(error => done(error));

  return true;
}
