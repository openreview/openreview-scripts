function () {
  var or3client = lib.or3client;

  var openReviewInvitation = or3client.createReviewInvitation(
    { 'id': 'ICLR.cc/2017/conference/-/paper/'+note.number+'/public/review',
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
  or3client.or3request(or3client.inviteUrl, openReviewInvitation, 'POST', token).catch(error=>console.log(error));

  // var messageProcess = function(){
  //   return true;
  // };

  // var messageInvite = or3client.createCommentInvitation({
  //   'id': 'ICLR.cc/2017/conference/-/reviewer/message',
  //   'signatures':['ICLR.cc/2017/conference'],
  //   'writers':['ICLR.cc/2017/conference'],
  //   'invitees': ['ICLR.cc/2017/areachairs'],
  //   'readers': ['everyone'],
  //   'process':messageProcess+'',
  //   'reply': { 
  //     'forum': note.forum,
  //     'readers': { 
  //       'values-regex': 'reviewer-.*',        
  //       description: 'The users who will be allowed to read the above content.'
  //     },
  //     'content': {
  //       'Subject': {
  //         'order': 1,
  //         'value-regex': '.{1,500}',
  //         'description': 'Subject line of your message.'
  //       },
  //       'Message': {
  //         'order': 3,
  //         'value-regex': '[\\S\\s]{1,5000}',
  //         'description': 'Your message.'
  //       }
  //     }
  //   }
  // });
  // or3client.or3request(or3client.inviteUrl, messageInvite, 'POST', token).catch(error=>console.log(error));
  

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

    return true;
  };

  var publicCommentInvite = or3client.createCommentInvitation({
    'id': 'ICLR.cc/2017/conference/-/paper/'+note.number+'/public/comment',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'invitees': ['~'],
    'readers': ['everyone'],
    'process':commentProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'parent': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*',
        'description': 'How your identity will be displayed with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'values-regex': ['everyone|ICLR.cc/2017/conference/paper'+note.number+'/(reviewer.*|areachair|authors)'], 
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


  var conference = or3client.prettyConferenceName(note);
  //Send an email to the author of the submitted note, confirming its receipt

  var mail = {
    "groups": note.content.author_emails.trim().split(","),
    "subject": "Confirmation of your submission to " + conference + ": \"" + note.content.title + "\".",
    "message": `Your submission to `+ conference +` has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: http://dev.openreview.net/forum?id=` + note.forum
  };
  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )
  
  // Create an empty group for reviewers of this paper, e.g. "ICLR.cc/2017/conference/paper444"
  var paperGroup = {
    'id': 'ICLR.cc/2017/conference/paper'+note.number,
    'signatures': ['ICLR.cc/2017/conference'],
    'writers': ['ICLR.cc/2017/conference'],
    'members': [],
    'readers': ['everyone'],
    'signatories': ['ICLR.cc/2017/conference', 'ICLR.cc/2017/conference/paper'+note.number]
  };

  var reviewerGroup = {
    'id': paperGroup.id+'/reviewers',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'members':[],
    'readers':['everyone'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/reviewers']
  }
  
  

  var reviewer1 = {
    'id': paperGroup.id+'/reviewer1',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'members':[],
    'readers':['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/reviewer1']
  }

  var reviewer2 = {
    'id': paperGroup.id+'/reviewer2',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'members':[],
    'readers':['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/reviewer2']
  }

  var reviewer3 = {
    'id': paperGroup.id+'/reviewer3',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'members':[],
    'readers':['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/reviewer3']
  }

  var authorGroup = {
    'id':paperGroup.id+'/authors',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'members': note.content.author_emails.trim().split(","),
    'readers':['everyone'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/authors']
  }

  var areachairGroup = {
    'id':paperGroup.id+'/areachair',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'members':[],
    'readers':['everyone'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/areachair']
  }
  
  or3client.or3request( or3client.grpUrl, paperGroup, 'POST', token ).then(
  result=>or3client.or3request( or3client.grpUrl, reviewerGroup, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, reviewer1, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, reviewer2, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, reviewer3, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, authorGroup, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, areachairGroup, 'POST', token ))

  return true;
};