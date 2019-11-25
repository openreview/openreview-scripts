function(){
    var or3client = lib.or3client;
    var CONFERENCE_ID = 'ICLR.cc/2020/Conference';
    var forumNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    forumNote.then(function(result) {
        var forum = result.notes[0];
        return or3client.or3request(or3client.inviteUrl + '?id=' + CONFERENCE_ID + '/Paper' + forum.number + '/-/Official_Review', {}, 'GET', token)
        .then(function(result) {
            var invitation = result.invitations[0];
            invitation.expdate = Date.now();
            return or3client.or3request(or3client.inviteUrl, invitation, 'POST', token);
        });
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
};
