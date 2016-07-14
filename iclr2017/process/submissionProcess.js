function(){
  var or3client = lib.or3client;
  var list = note.invitation.split('/')
  list.splice(list.indexOf('-',1));
  var conference = list.join('/')

  var comment_invite = or3client.createCommentInvitation(
    { 'id': conference + '/-/' + count + '/comment',
      'signatures':[conference],
      'writers':[conference],
      'invitees': ['~'],
      'reply': {
        'forum': note.forum,
        'process':or3client.commentProcess+''          
      }
    }
  );
  or3client.or3request(or3client.inviteUrl, comment_invite, 'POST',token).catch(error=>console.log(error));

  var review_invitation = or3client.createReviewInvitation(
    { 'id': conference + '/-/' + count + '/review',
      'signatures': [conference],
      'writers': [conference],
      'invitees': ['~'],
      'noninvitees': note.content.author_emails.trim().split(','),
      'reply': {
        'forum': note.id,
        'parent': note.id,
        'writers': {'values-regex':'~.*'},
        'signatures': {'values-regex':'~.*'},
        'process': or3client.reviewProcess+''
      }
    }
  );
  or3client.or3request(or3client.inviteUrl, review_invitation, 'POST', token).catch(error=>console.log(error));

  return true;
};