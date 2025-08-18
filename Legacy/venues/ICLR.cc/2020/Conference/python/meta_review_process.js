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
        })
        .then(function(result) {
            return or3client.or3request(or3client.inviteUrl + '?id=' + CONFERENCE_ID + '/Paper' + forum.number + '/-/Official_Comment', {}, 'GET', token)
        })
        .then(function(result) {
            var comment_invitation = result.invitations[0];
            comment_invitation.reply.signatures['values-regex'] = 'ICLR.cc/2020/Conference/Paper' + forum.number + '/Area_Chair[0-9]+|ICLR.cc/2020/Conference/Program_Chairs|ICLR.cc/2020/Conference/Paper' + forum.number + '/Buddy_Area_Chair1';
            var invitee_list = comment_invitation.invitees.filter(function(invitee){
                return invitee !== CONFERENCE_ID+'/Paper'+forum.number+'/Reviewers'
            });
            comment_invitation.invitees = invitee_list;
            return or3client.or3request(or3client.inviteUrl, comment_invitation, 'POST', token);
        });
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
};
