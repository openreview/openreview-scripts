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
            return blindedNote;
        } else {
            console.log('No notes with the referent ' + note.referent + ' were found');
        }
    })
    .then(blindedNote => or3client.or3request(or3client.notesUrl, blindedNote, 'POST', token))
    .then(result => done())
    .catch(error => done(error));
    return true;
}
