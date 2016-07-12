function () {
  var or3client = lib.or3client;

  var open_review_invitation = or3client.createReviewInvitation(
    { 'id': 'ICLR.cc/2017/conference/-/review/'+note.id,
      'signatures': ['ICLR.cc/2017/conference/areachairs/1','ICLR.cc/2017/conference'],
      'writers': ['ICLR.cc/2017/conference/areachairs/1','ICLR.cc/2017/conference'],
      'invitees': ['~'],
      'process':or3client.reviewProcess+'',
      'reply': { 
        'forum': note.id, 
        'parent': note.id,
        'writers': {'values-regex':'~.*|reviewer-.+'},
        'signatures': {'values-regex':'~.*|reviewer-.+'}
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
    'invitees': ['ICLR.cc/2017/conference/areachairs/1'],
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
    'process':or3client.commentProcess+''
  });
  or3client.or3request(or3client.inviteUrl, publicCommentInvite, 'POST', token).catch(error=>console.log(error));

  return true;
};