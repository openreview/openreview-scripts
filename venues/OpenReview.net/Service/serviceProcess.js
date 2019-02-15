function(){
    var or3client = lib.or3client;

    var openreviewMailPayload = {
      'groups': ['info@openreview.net'],
      'subject': 'A request for service has been submitted',
      'message': 'A request for service has been submitted. Check it here: ' + or3client.baseUrl + '/forum?id=' + note.forum
    };

    var programchairMailPayload = {
      'groups': note.content['Contact Emails'],
      'subject': 'Your request for OpenReview service has been received.',
      'message': 'You recently requested conference management services from OpenReview. A member of our support team will contact you shortly. You can view the request here: ' + or3client.baseUrl + '/forum?id=' + note.forum
    };

    or3client.or3request(or3client.mailUrl, openreviewMailPayload, 'POST', token)
    .then(result => or3client.or3request(or3client.mailUrl, programchairMailPayload, 'POST', token))
    .then(result => done())
    .catch(error => done(error));

    return true;
};
