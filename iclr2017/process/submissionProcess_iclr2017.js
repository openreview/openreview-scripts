function () {
  var or3client = lib.or3client;

  var reviewProcess = function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result){
      var mail = {
        "groups": result.notes[0].content.author_emails.trim().split(","),
        "subject": "Review of your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: http://dev.openreview.net/forum?id=" + note.forum
      };
      var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )
    });

    var fulfilledP = or3client.fulfillInvitation(invitation, note, token);
    return true;
  };
  var openReviewInvitation = {
    'id': 'ICLR.cc/2017/conference/-/paper'+note.number+'/public/review',
    'signatures': ['ICLR.cc/2017/conference'],
    'writers': ['ICLR.cc/2017/conference'],
    'invitees': ['~'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': reviewProcess+'',
    'reply': {
      'forum': note.id, 
      'parent': note.id,
      'writers': {'values-regex':'~.*'},
      'signatures': {'values-regex':'~.*'},
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

  var officialReviewInvitation = {
    'id': 'ICLR.cc/2017/conference/-/paper'+note.number+'/official/review',
    'signatures': ['ICLR.cc/2017/conference'],
    'writers': ['ICLR.cc/2017/conference'],
    'invitees': ['ICLR.cc/2017/conference/paper'+note.number+'/reviewers'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': reviewProcess+'',
    'duedate': 1481932799000,
    'reply': {
      'forum': note.id, 
      'parent': note.id,
      'writers': {'values-regex':'ICLR.cc/2017/conference/paper'+note.number+'/reviewer[0-9]+'},
      'signatures': {'values-regex':'ICLR.cc/2017/conference/paper'+note.number+'/reviewer[0-9]+'},
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
  or3client.or3request(or3client.inviteUrl, officialReviewInvitation, 'POST', token).catch(error=>console.log(error));


  var commentProcess = function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    
    var list = note.invitation.replace(/_/g,' ').split('/')
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ')

    origNote.then(function(result){
      var note_authors = result.notes[0].content.author_emails.trim().split(",");
      console.log('note authors before splice',note_authors)
      console.log('note', note.tauthor)

      //is note.signatures[0] a member of any of the values in note_authors?
      // var comment_author = note.tauthor
      // var auth = comment_authors
      // var index = note_authors.indexOf(auth);
      // if(index > -1){
      //   note_authors.splice(index,1)
      // };

      console.log('note authors after splice',note_authors)

      var mail = {
        "groups": note_authors,
        "subject": "Comment on your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: http://dev.openreview.net/forum?id=" + note.forum
      };
      var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )

    },
    function(error){
        return error
    });

    if(note.forum!=note.parent){
      var mail = {
        "groups": note.signatures,
        "subject":"You have received a comment",
        "message": "You have received a comment on your comment/review.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: http://dev.openreview.net/forum?id=" + note.forum
      }
      var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )
    };


    return true;
  };

  var publicCommentInvite = {
    'id': 'ICLR.cc/2017/conference/-/paper'+note.number+'/public/comment',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'],
    'invitees': ['~'],
    'noninvitees':[],
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
        'values-regex': ['everyone|ICLR.cc/2017/(pcs|conference/organizers|conference/paper'+note.number+'/reviewers_and_organizers)'], 
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
  or3client.or3request(or3client.inviteUrl, publicCommentInvite, 'POST', token).catch(error=>console.log(error));
  
  var acceptanceProcess = function(){
    return true;
  };

  var acceptanceInvite = {
    'id': 'ICLR.cc/2017/conference/-/paper'+note.number+'/acceptance',
    'signatures': ['ICLR.cc/2017/conference'],
    'writers': ['ICLR.cc/2017/conference'],
    'invitees': ['ICLR.cc/2017/pcs'],
    'noninvitees': [],
    'readers': ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
    'process': acceptanceProcess+'',
    'reply': {
      'forum': note.id,
      'parent': note.id,
      'signatures': {
        'values-regex':'ICLR.cc/2017/pcs',
        'description':'Your displayed identity associated with the above content.'
        },
      'writers': {'values-regex':'ICLR.cc/2017/pcs'}, 
      'readers': { 
        'values': ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'], 
        'description': 'The users who will be allowed to read the above content.'
        },
      'content': {
        'ICLR2017': {
          'order': 1,
          'value-radio': [
            'Accepted',
            'Rejected'
          ]
        }
      } 
    }
  };

  or3client.or3request(or3client.inviteUrl, acceptanceInvite, 'POST', token).catch(error=>console.log(error));

  var list = note.invitation.replace(/_/g,' ').split('/')
  list.splice(list.indexOf('-',1));
  var conference = list.join(' ')
  //Send an email to the author of the submitted note, confirming its receipt

  var mail = {
    "groups": note.content.author_emails.trim().split(","),
    "subject": "Confirmation of your submission to " + conference + ": \"" + note.content.title + "\".",
    "message": `Your submission to `+ conference +` has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: http://dev.openreview.net/forum?id=` + note.forum
  };
  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )
  
  // Create an empty group for this paper, e.g. "ICLR.cc/2017/conference/paper444"
  var paperGroup = {
    'id': 'ICLR.cc/2017/conference/paper'+note.number,
    'signatures': ['ICLR.cc/2017/conference'],
    'writers': ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
    'members': [],
    'readers': ['everyone'],
    'signatories': ['ICLR.cc/2017/conference', 'ICLR.cc/2017/conference/paper'+note.number]
  };

  var reviewerGroup = {
    'id': paperGroup.id+'/reviewers',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
    'members':[],
    'readers':['everyone'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/reviewers']
  };

  var reviewNonreadersGroup = {
    'id': paperGroup.id+'/review-nonreaders',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
    'members':[],
    'readers':['everyone'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/review-nonreaders']
  }

  var authorGroup = {
    'id':paperGroup.id+'/authors',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
    'members': note.content.author_emails.trim().split(","),
    'readers':['everyone'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/authors']
  };

  var areachairGroup = {
    'id':paperGroup.id+'/areachair',
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
    'members':[],
    'readers':['everyone'],
    'signatories':['ICLR.cc/2017/conference',paperGroup.id+'/areachair']
  };

  var reviewersAndOrganizers = {
    'id': paperGroup.id+'/reviewers_and_organizers',
    'readers': ['everyone'],
    'writers': ['ICLR.cc/2017/conference', 'ICLR.cc/2017/pcs'],
    'signatures': ['ICLR.cc/2017/conference'],
    'signatories': [paperGroup.id+'/reviewers_and_organizers'],
    'members':[reviewerGroup.id,'ICLR.cc/2017/conference/organizers']
  };

  or3client.or3request( or3client.grpUrl, paperGroup, 'POST', token ).then(
  result=>or3client.or3request( or3client.grpUrl, reviewerGroup, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, reviewNonreadersGroup, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, authorGroup, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, areachairGroup, 'POST', token )).then(
  result=>or3client.or3request( or3client.grpUrl, reviewersAndOrganizers, 'POST', token))

  return true;
};