function() {
    var or3client = lib.or3client;

    var number = note.invitation.split('/')[4].split('Paper')[1];

    var CONF = 'ICLR.cc/2018/Conference';

    or3client.or3request(or3client.notesUrl + '?forum=' + note.forum, {}, 'GET', token)
    .then(result => result.notes.filter(n => n.forum === n.id)[0])
    .then(originalNote => originalNote.overwriting[0])
    .then(overwritingId => {
      var reviewerMail = {
        "groups": ['ICLR.cc/2018/Conference/Paper' + number + '/Reviewers'],
        "subject": "Revision posted to a paper that you reviewed",
        "message": "A paper that you reviewed has been revised. \n\nTo view the paper, click here: " + baseUrl + "/forum?id=" + overwritingId + "\n\nYou can see the changes made at " + baseUrl + "/revisions?id=" + overwritingId
      };
      return or3client.or3request(or3client.mailUrl, reviewerMail, 'POST', token)
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
}
