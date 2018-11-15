
function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result) {
      var forum = result.notes[0];
      var sendto = forum.content.authorids;
      sendto.push('NIPS.cc/2018/Workshop/IRASL/Program_Chairs')

      var programchair_mail = {
        "groups": sendto,
        "subject": "Review posted to paper: \"" + forum.content.title + "\"",
        "message": "A submission to " + conference + ", has received an official review. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      var programchairMailP = or3client.or3request( or3client.mailUrl, programchair_mail, 'POST', token );

      return programchairMailP;
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
