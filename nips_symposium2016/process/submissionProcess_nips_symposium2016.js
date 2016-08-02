function () {
  var or3client = lib.or3client;


  var commentProcess = function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var conference = or3client.prettyConferenceName(note);

    origNote.then(function(result){
      var mail = {
        "groups": result.notes[0].content.author_emails.trim().split(","),
        "subject": "Comment on your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: http://dev.openreview.net/forum?id=" + note.forum
      };
      var mailP = or3client.or3request( mailUrl, mail, 'POST', token )
      
    });

    note.readers=note.readers.concat(note.writers[0]);

    or3client.or3request( or3client.notesUrl, note, 'POST', token)

    return true;
  }

  var publicCommentInvite = 
  {
    'id': 'NIPS.cc/Symposium/2016/-/submission/'+note.number+'/public/comment',
    'signatures':['NIPS.cc/Symposium/2016'],
    'writers': ['NIPS.cc/Symposium/2016'],
    'invitees': ['~'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': commentProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'parent': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*|\\(anonymous\\)',
        'description': 'Your displayed identity associated with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*|\\(anonymous\\)'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'values-regex': ['everyone'], 
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
        },
        'rating':{
          'order:':3,
          'value-radio': [
            Array(6).join(String.fromCharCode(9733)),
            Array(5).join(String.fromCharCode(9733)),
            Array(4).join(String.fromCharCode(9733)),
            Array(3).join(String.fromCharCode(9733)),
            Array(2).join(String.fromCharCode(9733))
          ]
        }
      }
    }
  };
  or3client.or3request(or3client.inviteUrl, publicCommentInvite, 'POST', token).catch(error=>console.log(error));

  var pcCommentInvite = 
  {
    'id': 'NIPS.cc/Symposium/2016/-/submission/'+note.number+'/program/committee/post',
    'signatures':['NIPS.cc/Symposium/2016'],
    'writers': ['NIPS.cc/Symposium/2016'],
    'invitees': ['NIPS.cc/Symposium/2016/PC'],
    'noninvitees':[],
    'readers': ['NIPS.cc/Symposium/2016/PC','NIPS.cc/Symposium/2016'],
    'process': commentProcess+'',
    'ddate': 2470017651235,
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'parent': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*',
        'description': 'Your displayed identity associated with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'values-regex': ['NIPS.cc/Symposium/2016/PC'], 
        'description': 'The users who will be allowed to read the above content.'
        },   // the reply must allow ANYONE to read this note (comment)
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
        'recommendation to organizers':{
          'order:':3,
          'value-dropdown': [
            "No Opinion",
            "Recommend for invitation",
            "Do Not Recommend for invitation"
          ]
        }
      }
    }
  };
  or3client.or3request(or3client.inviteUrl, pcCommentInvite, 'POST', token).catch(error=>console.log(error));

  //Send an email to the author of the submitted note, confirming its receipt
  // var conference = or3client.prettyConferenceName(note);
  // var mail = {
  //   "groups": note.content.author_emails.trim().split(","),
  //   "subject": "Confirmation of your submission to " + conference + ": \"" + note.content.title + "\".",
  //   "message": "Your submission to "+ conference +" has been posted.\n\nTo view the note, click here: http://dev.openreview.net/forum?id=" + note.forum
  // };
  // var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )

  return true;
};