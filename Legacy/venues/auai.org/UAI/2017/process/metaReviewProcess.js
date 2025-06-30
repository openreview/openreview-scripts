function() {
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    var programchairs = ['auai.org/UAI/2017/Program_Co-Chairs'];

    origNote.then(function(result){
      var forum = result.notes[0];

      var pc_mail = {
        "groups": programchairs,
        "subject": "[UAI 2017] Meta-review by an area chair has been posted: " + "\"" + forum.content.title + "\".",
        "message": "A paper submission to UAI 2017 has received a meta-review by an area chair.\n\nTitle: "+note.content.title+"\n\nMeta-review: "+note.content.metareview+"\n\nTo view the meta-review, click here: "+baseUrl+"/forum?id=" + note.forum + "&noteId=" + note.id
      };

      var reviewers = ['auai.org/UAI/2017/Paper' + forum.number + '/Reviewers'];
      var reviewer_mail = {
        "groups": reviewers,
        "subject": "[UAI 2017] Meta-review by an area chair has been posted: " + "\"" + forum.content.title + "\".",
        "message": "A paper submission to UAI 2017, for which you are a reviewer, has received a meta-review by an area chair.\n\nTitle: "+note.content.title+"\n\nMeta-review: "+note.content.metareview+"\n\nTo view the meta-review, click here: "+baseUrl+"/forum?id=" + note.forum + "&noteId=" + note.id
      };

      var promises = [
        or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token ),
        or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token )
      ];
      return Promise.all(promises)

    })
    .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
