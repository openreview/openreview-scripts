function () {
  var or3client = lib.or3client;

  var open_review_invitation = or3client.createReviewInvitation(
    { 'id': 'ICLR.cc/2017/conference/-/review/'+note.id,
      'signatures': ['ICLR.cc/2017/conference'],
      'writers': ['ICLR.cc/2017/conference'],
      'invitees': ['~'],
      'process':or3client.reviewProcess+'',
      'reply': { 
        'forum': note.id, 
        'parent': note.id,
        'writers': {'values-regex':'~.*|ICLR.cc/2017/conference/paper.+/reviewer.+'},
        'signatures': {'values-regex':'~.*|ICLR.cc/2017/conference/paper.+/reviewer.+'}
      }
    }
  );
  or3client.or3request(or3client.inviteUrl, open_review_invitation, 'POST', token).catch(error=>console.log(error));

  var messageProcess = function(){
    return true;
  };

  
  var messageInvite = or3client.createCommentInvitation({
    'id': 'ICLR.cc/2017/conference/-/reviewer/message',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'invitees': ['ICLR.cc/2017/areachairs'],
    'readers': ['everyone'],
    'process':messageProcess+'',
    'reply': { 
      'forum': note.forum,
      'readers': { 
        'values-regex': 'reviewer-.*',        
        description: 'The users who will be allowed to read the above content.'
      },
      'content': {
        'Subject': {
          'order': 1,
          'value-regex': '.{1,500}',
          'description': 'Subject line of your message.'
        },
        'Message': {
          'order': 3,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your message.'
        }
      }
    }
  });
  or3client.or3request(or3client.inviteUrl, messageInvite, 'POST', token).catch(error=>console.log(error));
  
  var publicCommentInvite = or3client.createCommentInvitation({
    'id': 'ICLR.cc/2017/conference/-/public/comment',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'invitees': ['~'],
    'readers': ['everyone'],
    'process':or3client.commentProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'parent': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*',
        'description': 'Your displayed identity associated with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'values': ['everyone'], 
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
  });
  or3client.or3request(or3client.inviteUrl, publicCommentInvite, 'POST', token).catch(error=>console.log(error));


  //Send an email to the author of the submitted note, confirming its receipt
  var conference = or3client.prettyConferenceName(note);
  var mail = {
    "groups": note.content.author_emails.trim().split(","),
    "subject": "Confirmation of your submission to " + conference + ": \"" + note.content.title + "\".",
    "message": "Your submission to "+ conference +" has been posted.\n\nTo view the note, click here: http://beta.openreview.net/note?id=" + note.forum
  };
  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )
  
  // Create an empty group for reviewers of this paper, e.g. "ICLR.cc/2017/conference/paper444"
  var reviewer_group = {
    'id': 'ICLR.cc/2017/conference/paper'+note.number,
    'signatures': ['ICLR.cc/2017/conference'],
    'writers': ['ICLR.cc/2017/conference'],
    'members': [],
    'readers': ['everyone'],
    'signatories': ['ICLR.cc/2017/conference']
  };
  or3client.or3request( or3client.grpUrl, reviewer_group, 'POST', token )

  return true;
};