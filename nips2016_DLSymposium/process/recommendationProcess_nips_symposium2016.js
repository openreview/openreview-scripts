function () {
  var or3client = lib.or3client;

  var commentProcess = function(){
    var or3client = lib.or3client;

    return true;
  }

  var ratingInvite = 
  {
    'id': 'NIPS.cc/2016/Deep_Learning_Symposium/-/paper/'+note.number+'/comment',
    'signatures':['NIPS.cc/2016/Deep_Learning_Symposium'],
    'writers': ['NIPS.cc/2016/Deep_Learning_Symposium'],
    'invitees': ['~'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': commentProcess+'',
    'reply': {
      'forum': note.forum,     // links this note (comment) to the previously posted note (paper)
      //'replyto': note.id,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*|\\(anonymous\\)',
        'description': 'Your displayed identity associated with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*|\\(anonymous\\)'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'value-dropdown': ['everyone','NIPS.cc/2016/Deep_Learning_Symposium/PC'], 
        'description': 'The users who will be allowed to read the above content.'
        }, 
      'content': {
        'title': {
          'order': 1,
          'value-regex': '.{1,500}',
          'description': 'Brief summary of your comment.'
        },
        'comment': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your comment or reply.'
        },
        'rating':{
          'order:':3,
          'description':'Your rating of the paper being discussed',
          'value-dropdown': [
            "No Rating",
            "1 - Do Not Recommend",
            "2 - Recommended",
            "3 - Strongly Recommended"
          ]
        }
      }
    }
  };
  or3client.or3request(or3client.inviteUrl, ratingInvite, 'POST', token).catch(error=>console.log(error));

  //Send an email to the author of the submitted note, confirming its receipt

  var message = "The NIPS 2016 Deep Learning Symposium has received your paper recommendation.\n\n"

  message = message + "To view the paper, click here: "+baseUrl+"/forum?id="+note.forum+"\n\n"

  message = message+"\""+note.content.title+"\"\n\n"
  message = message+note.content.authors+"\n\n"
  message = message+"Abstract: "+note.content.abstract

  var mail = {
    "groups": note.signatures,
    "subject": "Recommendation for NIPS 2016 Deep Learning Symposium received: \"" + note.content.title + "\"",
    "message": message
  };

  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )

  return true;
};