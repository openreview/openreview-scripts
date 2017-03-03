function(){
    var or3client = lib.or3client;

    const CONFERENCE = 'roboticsfoundation.org/RSS/2017';
    const PAPER = CONFERENCE+'/-/paper';
    const DUE_DATE = new Date(2017, 6, 30, 17, 15);

    console.log('PAM - the official Review Process is here');
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result) {
      var forum = result.notes[0];
      var note_number = forum.number;

      var reviewers = [PAPER + note_number + '/reviewers'];
      var authors = forum.content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to "+CONFERENCE+": \"" + forum.content.title + "\"",
        "message": "Your submission to " + conference + " has received an official review.\n\nTitle: " + note.content.title + "\n\nReview: " + note.content.review + "\n\nTo view the review, click here: " + baseUrl+"/forum?id=" + note.forum
      };

      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
 
      return Promise.all([
        authorMailP,
      ])
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };
