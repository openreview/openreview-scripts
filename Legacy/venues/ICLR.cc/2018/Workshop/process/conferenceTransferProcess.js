function() {
  var or3client = lib.or3client;

  var CONF = 'ICLR.cc/2018/Workshop';
  var PROGRAM_CHAIRS = CONF + '/Program_Chairs';
  var AUTHORS = CONF + '/Authors';

  or3client.or3request(or3client.notesUrl + '?id=' + note.content['paper id'], {}, 'GET', token)
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
      content: originalNote.content,
      original: originalNote.id,
      invitation: CONF + '/-/Submission'
    }
    return or3client.or3request(or3client.notesUrl, workshopSubmission, 'POST', token);
  })
  .catch(error => {
    var mail = {
        "groups": note.signatures,
        "subject": "ICLR 2018: Error during transfer (invalid ID)",
        "message": 'You recently tried to transfer a paper submission from the ICLR 2018 Conference Track to the Workshop Track, but something went wrong with the ID (' + note.content['paper id'] + ') that you provided. Please double check the ID of your paper and try again. If you have questions, please contact the OpenReview team at info@openreview.net'
    };
    or3client.or3request(or3client.mailUrl, mail, 'POST', token);
    done(error)
  })
  .then(result => done())
  .catch(error => done(error));

  return true;
}
