//EDIT ME

function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');


    var programchairs = ['ICLR.cc/2017/pcs'];

    origNote.then(function(result){
      var forum = result.notes[0];

      var pc_mail = {
        "groups": programchairs,
        "subject": "Meta-review by area chair posted: "+ "\"" + forum.content.title + "\".",
        "message": "A paper submission to "+ conference +" has received a meta-review by an area chair.\n\nTitle: "+note.content.title+"\n\nMeta-review: "+note.content.metareview+"\n\nTo view the meta-review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      return or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token );
    })
    .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
    .then(result => done())
    .catch(error=>done(error));

    return true;
  };
