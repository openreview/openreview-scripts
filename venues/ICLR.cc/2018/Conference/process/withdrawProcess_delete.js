function() {
    var or3client = lib.or3client;

    var CONF = 'ICLR.cc/2018/Conference';
    var BLIND_INVITATION = CONF + '/-/Blind_Submission';

    or3client.or3request(or3client.notesUrl + '?id=' + note.referent, {}, 'GET', token)
    .then(result => {
        if (result.notes.length > 0){
            var blindedNote = result.notes[0];

            var milliseconds = (new Date).getTime();
            blindedNote.ddate = milliseconds
            return or3client.or3request(or3client.notesUrl, blindedNote, 'POST', token);
        } else {
            return Promise.reject('No notes with the id ' + note.referent + ' were found');
        }
    })
    .then(result => or3client.or3request(or3client.notesUrl + '?id=' + result.original, {}, 'GET', token))
    .then(result => {
        if (result.notes.length > 0){
            var originalNote = result.notes[0];

            var milliseconds = (new Date).getTime();
            originalNote.ddate = milliseconds;
            originalNote.signatures = [CONF];
            return or3client.or3request(or3client.notesUrl, originalNote, 'POST', token);
        } else {
            return Promise.reject('No notes with the id ' + note.original + ' were found');
        }
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
}
