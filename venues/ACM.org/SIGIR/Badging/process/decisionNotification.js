function() {
  var or3client = lib.or3client;
  console.log('Tag process');

  var SHORT_PHRASE = 'ACM SIGIR Badging';
  
  var tagsP = or3client.or3request(or3client.tagsUrl + '?forum=' + note.forum, {}, 'GET', token)
  .then(result => result.tags.map(tagItem => tagItem.tag));

  var forumNotesP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);

  Promise.all([
    forumNotesP,
    tagsP
  ])
  .then(result => {
    var forumNote = result[0].notes[0];
    var assignedBadges = result[1];
    var authorMail;
    var authorMail = {
      groups: forumNote.content.authorids,
      subject: '[' + SHORT_PHRASE + '] A new badge has been posted on your submission. Title : "' + forumNote.content.title + '"',
      message: 'Your submission to ' + SHORT_PHRASE + ' has received a new badge.\n\nSubmission title: ' + forumNote.content.title + 
      '\n\nRequested Badges: ' + forumNote.content["requested badges"] + '\n\nAssigned Badges: ' + assignedBadges
    };
    return or3client.or3request(or3client.mailUrl, authorMail, 'POST', token);
  })
  .then(result => done())
  .catch(error => done(error));
  return true;
}