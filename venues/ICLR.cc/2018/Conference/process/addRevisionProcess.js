function() {
    var or3client = lib.or3client;

    var number = note.invitation.split('/')[4].split('Paper')[1];

    var CONF = 'ICLR.cc/2018/Conference';

    console.log('number: '+ number);

    var reviewerMail = {
      "groups": ['ICLR.cc/2018/Conference/Paper' + number + '/Reviewers'],
      "subject": "Revision posted to a paper that you reviewed",
      "message": "A paper that you reviewed has been revised. \n\nTo view the paper, click here: " + baseUrl + "/forum?id=" + note.forum + "\n\nYou can see the changes made at " + baseUrl + "/revisions?id=" + note.forum
    };

    or3client.or3request(or3client.mailUrl, reviewerMail, 'POST', token)
    .then(result => done())
    .catch(error => done(error));
    return true;
}
