function() {
  console.log('process initiated');

  var invitationSplits = note.invitation.split('/');
  var paperNumber = invitationSplits[4];
  console.log('paperNumber identified: ' + paperNumber);

  var or3client = lib.or3client;
  var hashKey = or3client.createHash(note.content.email, "2810398440804348173");
  console.log('hashKey generated: ' + hashKey);

  var orteamMessageAccept = 'MIDL 2018 Recruitment acceptance received:\n\n\
navigate to openreview-scripts/venues/MIDL.amsterdam/2018/Conference/python\n\n\
then run the following:\n\n\
python approve-recommendation.py\n\n\
Contact Michael with questions.';

  var orteamMessageDecline = 'MIDL 2018 Recruitment declination received:\n\n\
navigate to openreview-scripts/venues/MIDL.amsterdam/2018/Conference/python\n\n\
then run the following:\n\n\
python assign-reviewers.py ' + note.content.email + ',' + paperNumber + '\n\n\
Contact Michael with questions.';


  if (hashKey == note.content.key) {
    var acceptP = Promise.resolve();
    var declineP = Promise.resolve();
    var messageP = Promise.resolve();

    if (note.content.response == 'Yes'){
      acceptP = or3client.removeGroupMember('MIDL.amsterdam/2018/Conference/' + paperNumber + '/Reviewers/Declined', note.content.email, token);
      declineP = or3client.addGroupMember('MIDL.amsterdam/2018/Conference/' + paperNumber + '/Reviewers/Accepted', note.content.email, token);

      var orteamMessageBody = {
        groups: ['info@openreview.net'],
        subject: '[MIDL 2018] Recruitment Acceptance Received',
        message: orteamMessageAccept
      };
      messageP = or3client.or3request(or3client.mailUrl, orteamMessageBody, 'POST', token);
    } else {
      acceptP = or3client.removeGroupMember('MIDL.amsterdam/2018/Conference/' + paperNumber + '/Reviewers/Accepted', note.content.email, token);
      declineP = or3client.addGroupMember('MIDL.amsterdam/2018/Conference/' + paperNumber + '/Reviewers/Declined', note.content.email, token);

      var orteamMessageBody = {
        groups: ['info@openreview.net'],
        subject: '[MIDL 2018] Recruitment Acceptance Received',
        message: orteamMessageDecline
      };
      messageP = or3client.or3request(or3client.mailUrl, orteamMessageBody, 'POST', token);

    }

    Promise.all([acceptP, declineP, messageP])
    .then(result => {
      done();
      return true;
    })
    .catch(error => {
      done(error);
      return false;
    })

  } else {
    done('Invalid key', note.content.key);
    return false;
  }
}
