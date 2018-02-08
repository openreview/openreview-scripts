function() {
  var or3client = lib.or3client;

  var CONF = 'ICLR.cc/2018/Workshop';
  var PROGRAM_CHAIRS = CONF + '/Program_Chairs';
  var AUTHORS = CONF + '/Authors';

  or3client.or3request(or3client.notesUrl + '?id=' + note.content['paper id'], {}, 'GET', token)
  .then(result => {
    console.log('result: ');
    console.log(JSON.stringify(result));
    var submittedNote = result.notes[0];
    if (submittedNote.hasOwnProperty('original')) {
      console.log('BLIND NOTE SUBMITTED; getting original');
      return or3client.or3request(or3client.notesUrl + '?id=' + submittedNote.original, {}, 'GET', token);
    } else {
      console.log('ORIGINAL NOTE SUBMITTED');
      return submittedNote;
    }
  })
  .then(result => {
    console.log('result: ');
    console.log(JSON.stringify(result));
    var originalNote = result.notes[0];
    console.log('original note retrieved: ')
    console.log(originalNote);
    var workshopSubmission = {
      writers: [CONF],
      signatures: [CONF],
      readers: ['everyone'],
      content: {},
      original: originalNote.id,
      invitation: CONF + '/-/Submission'
    }
    return or3client.or3request(or3client.notesUrl, workshopSubmission, 'POST', token);
  })
  .then(result => done())
  .catch(error => done(error));

  return true;
}
