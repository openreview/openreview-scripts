function(){
  var or3client = lib.or3client;

  var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
  var SHORT_PHRASE = "ICLR 2019";
  var PAPER_AUTHORS = CONFERENCE_ID + '/Paper' + note.number + '/Authors';

  var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);

  forumNoteP.then(function(result) {
    var forumNote = result.notes[0];
    console.log(JSON.stringify(forumNote));
  })
  .then(result => done())
  .catch(error => done(error));

  return true;
};
