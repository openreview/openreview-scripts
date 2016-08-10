function () {
  var or3client = lib.or3client;


  var commentProcess = function(){
    var or3client = lib.or3client;

    return true;
  }

  var ratingInvite = 
  {
    'id': 'NIPS.cc/Deep_Learning_Symposium/2016/-/recommendation/'+note.number+'/public/rating',
    'signatures':['NIPS.cc/Deep_Learning_Symposium/2016'],
    'writers': ['NIPS.cc/Deep_Learning_Symposium/2016'],
    'invitees': ['~'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': commentProcess+'',
    'reply': {
      'forum': note.forum,     // links this note (comment) to the previously posted note (paper)
      'parent': note.id,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*|\\(anonymous\\)',
        'description': 'Your displayed identity associated with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*|\\(anonymous\\)'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'value-dropdown': ['everyone','NIPS.cc/Deep_Learning_Symposium/2016/PC'], 
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


  var commentInvite = 
  {
    'id': 'NIPS.cc/Deep_Learning_Symposium/2016/-/comment',
    'signatures':['NIPS.cc/Deep_Learning_Symposium/2016'],
    'writers': ['NIPS.cc/Deep_Learning_Symposium/2016'],
    'invitees': ['~'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': commentProcess+'',
    'reply': {
      'forum': note.forum,     // links this note (comment) to the previously posted note (paper)
      //'parent': note.id,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*|\\(anonymous\\)',
        'description': 'Your displayed identity associated with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*|\\(anonymous\\)'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'value-dropdown': ['everyone','NIPS.cc/Deep_Learning_Symposium/2016/PC'], 
        'description': 'The users who will be allowed to read the above content.'
        },   // the reply must allow ANYONE to read this note (comment)
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
        }
      }
    }
  };
  or3client.or3request(or3client.inviteUrl, commentInvite, 'POST', token).catch(error=>console.log(error));


  var pcCommentInvite = 
  {
    'id': 'NIPS.cc/Deep_Learning_Symposium/2016/-/recommendation/'+note.number+'/program/committee/post',
    'signatures':['NIPS.cc/Deep_Learning_Symposium/2016'],
    'writers': ['NIPS.cc/Deep_Learning_Symposium/2016'],
    'invitees': ['NIPS.cc/Deep_Learning_Symposium/2016/PC'],
    'noninvitees':[],
    'readers': ['NIPS.cc/Deep_Learning_Symposium/2016/PC','NIPS.cc/Deep_Learning_Symposium/2016'],
    'process': commentProcess+'',
    'ddate': 2470017651235,
    'reply': {
      'forum': note.forum,      // links this note (comment) to the previously posted note (paper)
      'parent': note.id,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*|NIPS.cc/Deep_Learning_Symposium/2016/PC',
        'description': 'Your displayed identity associated with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*|NIPS.cc/Deep_Learning_Symposium/2016/PC'},
      'readers': { 
        'value-dropdown': ['everyone','NIPS.cc/Deep_Learning_Symposium/2016/PC'], 
        'description': 'The users who will be allowed to read the above content.'
        },
      'content': {
        'title': {
          'order': 1,
          'value-regex': '.{0,500}',
          'description': 'Brief summary of your comment.'
        },
        'comment': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your comment or reply.'
        },
        'recommendation':{
          'order:':3,
          'value-dropdown': [
            "No Opinion",
            "Recommend for invitation",
            "Do Not Recommend for invitation"
          ],
          'description':'recommendation to organizers'
        }
      }
    }
  };
  or3client.or3request(or3client.inviteUrl, pcCommentInvite, 'POST', token).catch(error=>console.log(error));

  //Send an email to the author of the submitted note, confirming its receipt
  var conference = or3client.prettyConferenceName(note);

  var mail = {
    "groups": note.signatures,
    "subject": "Recommendation for " + conference + " received: \"" + note.content.title + "\".",
    "message": "Your recommended paper for "+ conference +" has been posted.\n\nTo view the note, click here: http://dev.openreview.net/forum?id=" + note.forum
  };
  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )

  return true;
};