function(){
    var or3client = lib.or3client;

    var mailPayload = {
      'groups': ['info@openreview.net'],
      'subject': 'A request for service has been submitted',
      'message': 'A request for service has been submitted. Check it here: ' + or3client.baseUrl + '/forum?id=' + note.forum
    };

    or3client.or3request(or3client.mailUrl, mailPayload, 'POST', token)
    .then(result => done())
    .catch(error => done(error));

    return true;
};
