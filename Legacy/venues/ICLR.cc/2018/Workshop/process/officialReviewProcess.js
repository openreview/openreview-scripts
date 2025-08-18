//EDIT ME

function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token)
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
