function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    var list = note.invitation.replace(/_/g,' ').split('/')
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ')

    var getReviewerEmails = function(origNoteNumber){

      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/paper'+origNoteNumber+'/reviewers',{},'GET',token)
      .then(result=>{
        var reviewers = result.groups[0].members;
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if(signatureIdx>=-1){
          reviewers.splice(signatureIdx,1);
        };
        if(note.readers.indexOf('everyone') == -1 && note.readers.indexOf('auai.org/UAI/2017/reviewers_and_ACS_and_organizers') == -1){
          reviewers = [];
        };
        var reviewer_mail = {
        "groups": reviewers,
        "subject": "Pre-review question posted to your assigned paper: \"" + note.content.title + "\"",
        "message": "A submission to "+ conference+", for which you are an official reviewer, has received a pre-review question. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.question+"\n\nTo view the pre-review question, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      })
    };

    origNote.then(function(result){
      var origNoteAuthors = result.notes[0].content.authorids;
      var note_number = result.notes[0].number

      var areachairs = ['auai.org/UAI/2017/paper'+note_number+'/areachairs'];

      var authors = (note.readers.indexOf('everyone') != -1) ? origNoteAuthors : [];
      var author_mail = {
        "groups": authors,
        "subject": "Pre-review question on your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a pre-review question from a reviewer.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.question+"\n\nTo view the pre-review question, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      if(note.readers.indexOf('everyone') == -1 && note.readers.indexOf('auai.org/UAI/2017/ACs_and_organizers') == -1 && note.readers.indexOf('auai.org/UAI/2017/reviewers_and_ACS_and_organizers') == -1){
        areachairs = []
      };
      var areachair_mail = {
        "groups": areachairs,
        "subject": "Pre-review question posted to your assigned paper: \"" + note.content.title + "\"",
        "message": "A submission to "+ conference+", for which you are an official area chair, has received a pre-review question. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.question+"\n\nTo view the pre-review question, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      return or3client.addInvitationInvitee('auai.org/UAI/2017/-/paper'+note_number+'/official/review', note.signatures[0],token)
      .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
      .then(Promise.all([
        getReviewerEmails(note_number),
        or3client.or3request( or3client.mailUrl, author_mail, 'POST', token ),
        or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token )
      ]));
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
