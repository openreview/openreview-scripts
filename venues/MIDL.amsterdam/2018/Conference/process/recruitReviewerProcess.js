function() {

  console.log('process initiated');
  var or3client = lib.or3client;
  var hashKey = or3client.createHash(note.content.email, "2810398440804348173");
  console.log('hashKey generated: ' + hashKey);


  or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
  .then(function(result){
    var paper = result.notes[0];
    console.log('paper info retrieved: ' + paper.id);
    if(hashKey == note.content.key) {
      console.log('hashKey accepted');
      if (note.content.response == 'Yes') {
        console.log("Invitation replied Yes")
        //if a user is in the declined group, remove them from that group and add them to the reviewers group
        var acceptP = or3client.removeGroupMember('MIDL.amsterdam/2018/Conference/Paper'+paper.number+'/Reviewers/Declined', note.content.email, token);
        var declineP = or3client.addGroupMember('MIDL.amsterdam/2018/Conference/Paper'+paper.number+'/Reviewers/Accepted', note.content.email, token);

        var orteamMessage = 'MIDL 2018 Recruitment acceptance received:\n\n\
navigate to openreview-scripts/venues/MIDL.amsterdam/2018/Conference/python\n\n\
then run the following:\n\n\
python approve-recommendation.py --baseurl https://openreview.net\n\n\
Contact Michael with questions.';

        var orteamMessageBody = {
          groups: ['info@openreview.net'],
          subject: '[MIDL 2018] Recruitment Acceptance Received',
          message: orteamMessage
        };
        var messageP = or3client.or3request(or3client.mailUrl, orteamMessageBody, 'POST', token);
      } else if (note.content.response == 'No'){
        console.log("Invitation replied No");
        //if a user is in the reviewers group, remove them from that group and add them to the reviewers-declined group
        var acceptP = or3client.removeGroupMember('MIDL.amsterdam/2018/Conference/Paper'+paper.number+'/Reviewers/Accepted', note.content.email, token);
        var declineP = or3client.addGroupMember('MIDL.amsterdam/2018/Conference/Paper'+paper.number+'/Reviewers/Declined', note.content.email, token);
        var orteamMessage = 'MIDL 2018 Recruitment declination received:\n\n\
navigate to openreview-scripts/venues/MIDL.amsterdam/2018/Conference/python\n\n\
then run the following:\n\n\
python assign-reviewers.py ' + note.content.email + ',' + paper.number + ' --remove --baseurl https://openreview.net\n\n\
Contact Michael with questions.';

        var orteamMessageBody = {
          groups: ['info@openreview.net'],
          subject: '[MIDL 2018] Recruitment Acceptance Received',
          message: orteamMessage
        };
        var messageP = or3client.or3request(or3client.mailUrl, orteamMessageBody, 'POST', token);
      } else {
        done('Invalid response', note.content.response);
      }

      return Promise.all([acceptP, declineP, messageP]);
    } else {
      done('Invalid key', note.content.key);
      return false;
    }
  })
  .then(result=>done())
  .catch(error=>done(error))

  return true
}
