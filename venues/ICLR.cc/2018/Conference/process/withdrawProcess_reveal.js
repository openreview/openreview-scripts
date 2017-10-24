function() {
    var or3client = lib.or3client;

    var CONF = 'ICLR.cc/2018/Conference';
    var BLIND_INVITATION = CONF + '/-/Blind_Submission';
    var WITHDRAWN_INVITATION = CONF + '/-/Withdrawn_Submission';

    or3client.or3request(or3client.notesUrl + '?id=' + note.referent, {}, 'GET', token)
    .then(result => {
        var blindedNote = result.notes[0];

        var milliseconds = (new Date).getTime();
        blindedNote.ddate = milliseconds
        return blindedNote;
    })
    .then(blindedNote => or3client.or3request(or3client.notesUrl, blindedNote, 'POST', token))
    .then(result => {
        console.log('result: ' + JSON.stringify(result));
        var withdrawn_submission = {
            original: result.original,
            invitation: WITHDRAWN_INVITATION,
            forum: null,
            parent: null,
            signatures: [CONF],
            writers: [CONF],
            readers: ['everyone'],
            content: {}
        }
        return or3client.or3request(or3client.notesUrl, withdrawn_submission, 'POST', token);
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
}
