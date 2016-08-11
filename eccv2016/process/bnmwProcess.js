function () {
  var or3client = lib.or3client;
  
  var commentProcess = function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(notesUrl+'?id='+note.forum, {}, 'GET', token);

    var conference = or3client.prettyConferenceName(note);

    origNote.then(function(result){
      var mail = {
        "groups": result.notes[0].content.author_emails.trim().split(","),
        "subject": "Comment on your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: http://beta.openreview.net/forum?id=" + note.forum
      };
      var mailP = or3client.or3request( mailUrl, mail, 'POST', token )
      
    });

    return true;
  };

  var reviewProcess = function(){
    var or3client = lib.or3client;
    var origNote = or3client.or3request(notesUrl+'?id='+note.forum, {}, 'GET', token);
    
    var conference = or3client.prettyConferenceName(note);

    origNote.then(function(result){
      var mail = {
        "groups": result.notes[0].content.author_emails.trim().split(","),
        "subject": "Review of your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: http://beta.openreview.net/forum?id=" + note.forum
      };
      var mailP = or3client.or3request( mailUrl, mail, 'POST', token )
      
    });
    var fulfilledP = or3client.fulfillInvitation(invitation, note, token);
    return true;
  };

  var commentInvite = {
    'id': 'ECCV2016.org/BNMW/paper/-/'+note.number+'/comment',
    'signatures':['ECCV2016.org/BNMW'],
    'writers':['ECCV2016.org/BNMW'],
    'invitees': ['~'],
    'noninvitees': [],
    'readers': ['everyone'],
    'process': commentProcess+'',
    'reply': {
      'forum': note.forum,      // 'parent' not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*',
        'description': 'Your displayed identity associated with the above content.' 
        },
      'writers': {'values-regex':'~.*'},
      'readers': { 
        'values': ['everyone'], 
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
        }
      }
    }
  };
  or3client.or3request(or3client.inviteUrl, commentInvite, 'POST',token).catch(error=>console.log(error));

  var openReviewInvitation = { 
    'id': 'ECCV2016.org/BNMW/paper/-/open/review/'+note.number,
    'signatures': ['ECCV2016.org/BNMW'],
    'writers': ['ECCV2016.org/BNMW'],
    'invitees': ['~'],
    'noninvitees':[],
    'readers':['everyone'],
    'process': reviewProcess+'',
    'reply': {
      'forum': note.id, 
      'parent': note.id,
      'signatures': {
        'values-regex':'~.*|reviewer-.+',
        'description': 'Your displayed identity associated with the above content.' 
      },
      'writers': {'values-regex':'~.*|reviewer-.+'},
      'readers': { 
        'values': ['everyone'], 
        'description': 'The users who will be allowed to read the above content.'
        },
      'content': {
        'title': {
          'order': 1,
          'value-regex': '.{0,500}',
          'description': 'Brief summary of your review.'
        },
        'review': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.'
        },
        'rating': {
          'order': 3,
          'value-dropdown': [
            '10: Top 5% of accepted papers, seminal paper', 
            '9: Top 15% of accepted papers, strong accept', 
            '8: Top 50% of accepted papers, clear accept', 
            '7: Good paper, accept',
            '6: Marginally above acceptance threshold',
            '5: Marginally below acceptance threshold',
            '4: Ok but not good enough - rejection',
            '3: Clear rejection',
            '2: Strong rejection',
            '1: Trivial or wrong'
          ]
        },
        'confidence': {
          'order': 4,
          'value-radio': [
            '5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature', 
            '4: The reviewer is confident but not absolutely certain that the evaluation is correct', 
            '3: The reviewer is fairly confident that the evaluation is correct',
            '2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper',
            '1: The reviewer\'s evaluation is an educated guess'
          ]
        }
      } 
    }
  };

  or3client.or3request(or3client.inviteUrl, openReviewInvitation, 'POST', token).catch(error=>console.log(error));

  //Send an email to the author of the submitted note, confirming its receipt
  var conference = or3client.prettyConferenceName(note);

  var mail = {
    "groups": note.signatures,
    "subject": "Submission to " + conference + " received: \"" + note.content.title + "\".",
    "message": "Your submission to "+ conference +" has been posted.\n\nTo view the note, click here: http://beta.openreview.net/forum?id=" + note.forum
  };
  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )

  return true;
};