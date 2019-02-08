function(){
  var or3client = lib.or3client;

  var CONFERENCE_ID = 'learningtheory.org/COLT/2019/Conference';
  var PAPER_PROGRAM_COMMITTEE;

  var forumNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

  forumNote.then(function(result) {
    var forum = result.notes[0];
    var note_number = forum.number;
    PAPER_PROGRAM_COMMITTEE = CONFERENCE_ID + '/Paper' + note_number + '/Program_Committee';
  })
  .then(result => {
    console.log('attempting to add to group ' + PAPER_PROGRAM_COMMITTEE + '/Submitted');
    return or3client.addGroupMember(PAPER_PROGRAM_COMMITTEE + '/Submitted', note.signatures[0], token);
  })
  .then(result => {
    console.log('attempting to remove from group ' + PAPER_PROGRAM_COMMITTEE + '/Unubmitted');
    return or3client.removeGroupMember(PAPER_PROGRAM_COMMITTEE + '/Unsubmitted', note.signatures[0], token);
  })
  .then(result => done())
  .catch(error => done(error));
  return true;
};