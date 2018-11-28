function() {
  var or3client = lib.or3client;

  var paperId = note.forum;
  var CONFERENCE_ID = 'learningtheory.org/COLT/2019/Conference';
  var HASH_SEED = '1234';

  var hashKey = or3client.createHash(note.content.email, HASH_SEED);


  or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
  .then(result => {
    if (result && result.notes && result.notes.length) {
      var forum = result.notes[0];
      var reviewersGroupId = CONFERENCE_ID + '/Paper' + forum.number + '/Program_Committee';
      var reviewersDeclinedGroupId = reviewersGroupId + '/Declined';

      if(hashKey == note.content.key) {
        if (note.content.response == 'Yes') {
          console.log("Invitation replied Yes")
          //if a user is in the declined group, remove them from that group and add them to the reviewers group
          return or3client.removeGroupMember(reviewersDeclinedGroupId, note.content.email, token)
          .then(result => or3client.addGroupMember(reviewersGroupId, note.content.email, token));
        } else if (note.content.response == 'No'){
          console.log("Invitation replied No")
          //if a user is in the reviewers group, remove them from that group and add them to the reviewers-declined group
          return or3client.removeGroupMember(reviewersGroupId, note.content.email, token)
          .then(result => or3client.addGroupMember(reviewersDeclinedGroupId, note.content.email, token));
        } else {
          return Promise.reject('Invalid response: ' + note.content.response);
        }
      } else {
        return Promise.reject('Invalid key: ' + note.content.key);
      }
    } else {
      return Promise.reject('Forum not found: ' + note.forum);
    }
  })
  .then(result => done())
  .catch(error => done(error));


  return true;
}
