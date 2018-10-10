
function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result) {
      var forum = result.notes[0];
      var prog_chair = ['NIPS.cc/2018/Workshop/Spatiotemporal/Program_Chairs'];

      var progchair_mail = {
        "groups": prog_chair,
        "subject": "Review posted to paper: \"" + forum.content.title + "\"",
        "message": "A submission to " + conference + ", has received a confidential review.\n\nRelevance to the workshop: " + note.content.relevance + '\n\nNovelty: ' + note.content.novelty + '\n\nPotential impact: ' + note.content.impact + '\n\nTo view the evaluation, click here: ' + baseUrl+'/forum?id=' + note.forum +'&noteId='+note.id
      };
      var progchairMailP = or3client.or3request( or3client.mailUrl, progchair_mail, 'POST', token );

      return progchairMailP;
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
