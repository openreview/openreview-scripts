function () {
  var or3client = lib.or3client;
  
  var metaReviewProcess = function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');


    var programchairs = ['UAI.org/2017/pcs'];

    origNote.then(function(result){
      var authors = result.notes[0].content.author_emails.trim().split(",");
      var author_mail = {
        "groups": authors,
        "subject": "Meta-review of your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a meta-review by an area chair.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the meta-review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var pc_mail = {
        "groups": programchairs,
        "subject": "["+conference+"] Meta-review by area chair posted: "+ "\"" + note.content.title + "\".",
        "message": "A paper submission to "+ conference +" has received a meta-review by an area chair.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the meta-review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var promises = [
        or3client.or3request( or3client.mailUrl, author_mail, 'POST', token ),
        or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token )
      ];
      return Promise.all(promises)

    })
    .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))   
    .then(result => done())
    .catch(error=>done(error));

    return true;
  };


  var metaReviewInvitation = {
    'id': 'UAI.org/2017/conference/-/paper'+note.number+'/meta/review',
    'signatures': ['UAI.org/2017/conference'],
    'writers': ['UAI.org/2017/conference'],
    'invitees': ['UAI.org/2017/conference/paper'+note.number+'/areachairs'],
    'noninvitees':[],
    'readers': ['UAI.org/2017/conference/ACs_and_organizers'],
    'process': metaReviewProcess+'',
    'duedate': 1481932799000,
    'reply': {
      'forum': note.id, 
      'replyto': note.id,
      'writers': {'values-regex':'UAI.org/2017/conference/paper'+note.number+'/areachair[0-9]+'},
      'signatures': {'values-regex':'UAI.org/2017/conference/paper'+note.number+'/areachair[0-9]+'},
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
        'metareview': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.'
        },
        'recommendation': {
          'order': 3,
          'value-dropdown': [
            'Oral', 
            'Poster', 
            'Workshop', 
            'Reject'
          ]
        }
      } 
    }
  };  

  var openReviewProcess = function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');


    origNote.then(function(result){
      var note_number = result.notes[0].number

      var reviewers = ['UAI.org/2017/conference/paper'+note_number+'/reviewers'];
      var areachairs = ['UAI.org/2017/conference/paper'+note_number+'/areachairs'];

      var authors = result.notes[0].content.author_emails.trim().split(",");
      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to " + conference + ": \"" + note.content.title + "\"",
        "message": "Your submission to "+ conference +" has received a public review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + note.content.title + "\"",
        "message": "A submission to "+ conference+", for which you are an official area chair, has received a public review. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var promises = [
        or3client.or3request( or3client.mailUrl, author_mail, 'POST', token ),
        or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token )
      ];
      return Promise.all(promises)
    })
    .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
    .then(result=>done())
    .catch(error=>done(error));

    return true;
  };

  var openReviewInvitation = {
    'id': 'UAI.org/2017/conference/-/paper'+note.number+'/public/review',
    'signatures': ['UAI.org/2017/conference'],
    'writers': ['UAI.org/2017/conference'],
    'invitees': ['~'],
    'noninvitees':note.content.author_emails.trim().split(","),
    'readers': ['everyone'],
    'process': openReviewProcess+'',
    'reply': {
      'forum': note.id, 
      'replyto': note.id,
      'writers': {'values-regex':'~.*|\\(anonymous\\)'},
      'signatures': {'values-regex':'~.*|\\(anonymous\\)'},
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

  var officialReviewProcess = function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result){
      var note_number = result.notes[0].number

      var reviewers = ['UAI.org/2017/conference/paper'+note_number+'/reviewers'];
      var areachairs = ['UAI.org/2017/conference/paper'+note_number+'/areachairs'];
      var authors = result.notes[0].content.author_emails.trim().split(",");

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to " + conference + ": \"" + note.content.title + "\"",
        "message": "Your submission to "+ conference +" has received an official review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + note.content.title + "\"",
        "message": "A submission to "+ conference+", for which you are an official area chair, has received an official review. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      var authorMailP = or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
      var areachairMailP = or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );

      return Promise.all([
        authorMailP,
        areachairMailP
      ])
    })
    .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0], token))
    .then(result => done())
    .catch(error => done(error));
    return true;
  };

  var officialReviewInvitation = {
    'id': 'UAI.org/2017/conference/-/paper'+note.number+'/official/review',
    'signatures': ['UAI.org/2017/conference'],
    'writers': ['UAI.org/2017/conference'],
    'invitees': [],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': officialReviewProcess+'',
    'duedate': 1481932799000,
    'reply': {
      'forum': note.id, 
      'replyto': note.id,
      'writers': {'values-regex':'UAI.org/2017/conference/paper'+note.number+'/AnonReviewer[0-9]+'},
      'signatures': {'values-regex':'UAI.org/2017/conference/paper'+note.number+'/AnonReviewer[0-9]+'},
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

  var questionProcess = function(){
    var or3client = lib.or3client;
    
    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    
    var list = note.invitation.replace(/_/g,' ').split('/')
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ')

    var getReviewerEmails = function(origNoteNumber){

      return or3client.or3request(or3client.grpUrl+'?id=UAI.org/2017/conference/paper'+origNoteNumber+'/reviewers',{},'GET',token)
      .then(result=>{
        var reviewers = result.groups[0].members;
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if(signatureIdx>=-1){
          reviewers.splice(signatureIdx,1);
        };
        if(note.readers.indexOf('everyone') == -1 && note.readers.indexOf('UAI.org/2017/conference/reviewers_and_ACS_and_organizers') == -1){
          reviewers = [];
        };
        var reviewer_mail = {
        "groups": reviewers,
        "subject": "Pre-review question posted to your assigned paper: \"" + note.content.title + "\"",
        "message": "A submission to "+ conference+", for which you are an official reviewer, has received a pre-review question. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.question+"\n\nTo view the pre-review question, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      })
    };

    origNote.then(function(result){
      var origNoteAuthors = result.notes[0].content.author_emails.trim().split(",");
      var note_number = result.notes[0].number

      var areachairs = ['UAI.org/2017/conference/paper'+note_number+'/areachairs'];

      var authors = (note.readers.indexOf('everyone') != -1) ? origNoteAuthors : [];
      var author_mail = {
        "groups": authors,
        "subject": "Pre-review question on your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a pre-review question from a reviewer.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.question+"\n\nTo view the pre-review question, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      
      if(note.readers.indexOf('everyone') == -1 && note.readers.indexOf('UAI.org/2017/conference/ACs_and_organizers') == -1 && note.readers.indexOf('UAI.org/2017/conference/reviewers_and_ACS_and_organizers') == -1){
        areachairs = []
      };
      var areachair_mail = {
        "groups": areachairs,
        "subject": "Pre-review question posted to your assigned paper: \"" + note.content.title + "\"",
        "message": "A submission to "+ conference+", for which you are an official area chair, has received a pre-review question. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.question+"\n\nTo view the pre-review question, click here: "+baseUrl+"/forum?id=" + note.forum
      };
    
      return or3client.addInvitationInvitee('UAI.org/2017/conference/-/paper'+note_number+'/official/review', note.signatures[0],token)
      .then(or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
      .then(Promise.all([ 
        getReviewerEmails(note_number), 
        or3client.or3request( or3client.mailUrl, author_mail, 'POST', token ),
        or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token )
      ]));
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };

  var reviewerQuestionInvite = {
    'id': 'UAI.org/2017/conference/-/paper'+note.number+'/pre-review/question',
    'duedate': 1481932799000,
    'signatures':['UAI.org/2017/conference'],
    'writers':['UAI.org/2017/conference'],
    'invitees': ['UAI.org/2017/conference/paper'+note.number+'/reviewers'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process':questionProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      'replyto': note.id,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'UAI.org/2017/conference/paper'+note.number+'/AnonReviewer[0-9]+',
        'description': 'How your identity will be displayed with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'UAI.org/2017/conference/paper'+note.number+'/AnonReviewer[0-9]+'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'values': ['everyone'], 
        'description': 'The users who will be allowed to read the above content.'
        },   // the reply must allow ANYONE to read this note (comment)
      'content': {
        'title': {
          'order': 1,
          'value-regex': '.{1,500}',
          'description': 'Brief summary of your question.'
        },
        'question': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your question'
        }
      }
    }
  };

  var commentProcess = function(){
    console.log('comment process initiated')
    var or3client = lib.or3client;
    
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ')

    var getAuthorEmails = function(origNote){
      console.log('get author emails initiated')
      var origNoteAuthors = origNote.content.author_emails.trim().split(",");
      var origNoteSignature = origNote.signatures[0];

      var author_mail = {
        "groups": origNoteAuthors,
        "subject": "Comment on your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
    };

    var getReviewerEmails = function(origNoteNumber){
      console.log('get reviewer emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=UAI.org/2017/conference/paper'+origNoteNumber+'/reviewers',{},'GET',token)
      .then(result=>{
        var reviewers = result.groups[0].members;
        console.log('reviewers before filter',reviewers);
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if(signatureIdx>-1){
          reviewers.splice(signatureIdx,1);
        };

        console.log('reviewers after filter',reviewers);
        var reviewer_mail = {
          "groups": reviewers,
          "subject": "Comment posted to your assigned paper: \"" + note.content.title + "\"",
          "message": "A submission to "+ conference+", for which you are an official reviewer, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      })
    };

    var getAreachairEmails = function(origNoteNumber){
      console.log('get AC emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=UAI.org/2017/conference/paper'+origNoteNumber+'/areachairs',{},'GET',token)
      .then(result=>{      
        var areachairs = result.groups[0].members;
        var signatureIdx = areachairs.indexOf(note.signatures[0]);
        console.log('areachairs before filter:',areachairs);
        if(signatureIdx>-1){
          areachairs.splice(signatureIdx,1);
        };
        console.log('areachairs after filter:',areachairs);
        var areachair_mail = {
          "groups": areachairs,
          "subject": "Comment posted to your assigned paper: \"" + note.content.title + "\"",
          "message": "A submission to "+ conference+", for which you are an official area chair, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );
      })
    };

    var getPCEmails = function(){
      console.log('get PC emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=UAI.org/2017/pcs',{},'GET',token)
      .then(result=>{      
        var pcs = result.groups[0].members;
        var signatureIdx = pcs.indexOf(note.signatures[0]);
        console.log('pcs before filter:',pcs);
        if(signatureIdx>-1){
          pcs.splice(signatureIdx,1);
        };
        console.log('pcs after filter:',pcs);
        var pc_mail = {
          "groups": pcs,
          "subject": "Private comment posted to a paper: \"" + note.content.title + "\"",
          "message": "A submission to "+ conference+" has received a private comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token );
      })
    };

    var getCommentEmails = function(replytoNoteSignatures){
      console.log('replytoNoteSignatures before filter:',replytoNoteSignatures);

      if(note.readers.indexOf('everyone') == -1){
        replytoNoteSignatures=[];
      };
      console.log('replytoNoteSignatures after filter:',replytoNoteSignatures);
      var comment_mail = {
        "groups": replytoNoteSignatures,
        "subject":"Your post has received a comment",
        "message": "One of your posts has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, comment_mail, 'POST', token );
    };

    console.log('functions defined')
    var origNoteP = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl+'?id='+note.replyto,{},'GET',token) : null;
    console.log('promises created')
    Promise.all([
      origNoteP,
      replytoNoteP
    ]).then(result => {
      console.log('promises resolving')
      var origNote = result[0].notes[0];
      var origNoteNumber = origNote.number;

      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteReaders = replytoNote ? replytoNote.readers : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : null;

      console.log('replytoNote',replytoNote);
      console.log('replytoNoteReaders',replytoNoteReaders);
      console.log('replytoNoteSignatures',replytoNoteSignatures);
      var promises = [];
      console.log('note',note)
      console.log('note.readers',note.readers)
      var visibleToEveryone = note.readers.indexOf('everyone')>-1 ? true : false;
      console.log('visibleToEveryone',visibleToEveryone);
      var visibleToReviewers = note.readers.indexOf('UAI.org/2017/conference/reviewers_and_ACS_and_organizers')>-1 ? true : false;
      var visibleToAreachairs = note.readers.indexOf('UAI.org/2017/conference/ACs_and_organizers')>-1 ? true : false;
      var visibleToPCs = note.readers.indexOf('UAI.org/2017/conference/organizers')>-1 ? true : false;

      if(visibleToEveryone){
        var authorMailP = getAuthorEmails(origNote);
        promises.push(authorMailP);
      };

      if(visibleToEveryone || visibleToReviewers){
        var reviewerMailP = getReviewerEmails(origNoteNumber);
        promises.push(reviewerMailP);
      };

      if(visibleToEveryone || visibleToReviewers || visibleToAreachairs){
        var areachairMailP = getAreachairEmails(origNoteNumber);
        promises.push(areachairMailP);
      };

      if(visibleToReviewers || visibleToAreachairs || visibleToPCs){
        var pcMailP = getPCEmails();
        promises.push(pcMailP);
      }

      var rootComment = note.forum == note.replyto;
      var anonComment = replytoNoteSignatures.indexOf('(anonymous)')>-1 ? true : false;
      var selfComment = replytoNoteSignatures.indexOf(note.signatures[0])>-1 ? true : false;

      if(!rootComment && !anonComment && !selfComment) { 
        var commentMailP = getCommentEmails(replytoNoteSignatures);
        promises.push(commentMailP);
      };

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
  
  var publicCommentInvite = {
    'id': 'UAI.org/2017/conference/-/paper'+note.number+'/public/comment',
    'signatures':['UAI.org/2017/conference'],
    'writers':['UAI.org/2017/conference'],
    'invitees': ['~'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process':commentProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'replyto': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.*|\\(anonymous\\)',
        'description': 'How your identity will be displayed with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'~.*|\\(anonymous\\)'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'value-dropdown': [
          'everyone',
          'UAI.org/2017/conference/organizers',
          'UAI.org/2017/conference/ACs_and_organizers',
          'UAI.org/2017/conference/reviewers_and_ACS_and_organizers'
        ], 
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

  var officialCommentInvite = {
    'id': 'UAI.org/2017/conference/-/paper'+note.number+'/official/comment',
    'signatures':['UAI.org/2017/conference'],
    'writers':['UAI.org/2017/conference'],
    'invitees': ['UAI.org/2017/conference/paper'+note.number+'/reviewers','UAI.org/2017/conference/paper'+note.number+'/areachairs'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process':commentProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'replyto': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'UAI.org/2017/conference/paper'+note.number+'/(reviewer|areachair)[0-9]+',
        'description': 'How your identity will be displayed with the above content.' 
        },    // this regex demands that the author reveal his/her ~ handle
      'writers': {'values-regex':'UAI.org/2017/conference/paper'+note.number+'/(reviewer|areachair)[0-9]+'},    // this regex demands that the author reveal his/her ~ handle
      'readers': { 
        'value-dropdown': [
          'everyone',
          'UAI.org/2017/conference/organizers',
          'UAI.org/2017/conference/ACs_and_organizers',
          'UAI.org/2017/conference/reviewers_and_ACS_and_organizers'
        ], 
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


  var acceptanceProcess = function(){
    var or3client = lib.or3client;
    or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token)
    .then(result => done())
    .catch(error => done(error));
    return true;
  };

  var acceptanceInvite = {
    'id': 'UAI.org/2017/conference/-/paper'+note.number+'/acceptance',
    'signatures': ['UAI.org/2017/conference'],
    'writers': ['UAI.org/2017/conference'],
    'invitees': ['UAI.org/2017/pcs'],
    'noninvitees': [],
    'readers': ['everyone'],
    'process': acceptanceProcess+'',
    'reply': {
      'forum': note.id,
      'replyto': note.id,
      'signatures': {
        'values-regex':'UAI.org/2017/pcs',
        'description':'Your displayed identity associated with the above content.'
        },
      'writers': {'values-regex':'UAI.org/2017/pcs'},
      'readers': { 
        'values': ['UAI.org/2017/pcs','UAI.org/2017/areachairs','UAI.org/2017/conference'],
        'description': 'The users who will be allowed to read the above content.'
        },
      'content': {
        'UAI2017': {
          'order': 1,
          'value-radio': [
            'Accepted',
            'Rejected',
            'Pending'
          ]
        }
      } 
    }
  };

  var referenceInvite = {
    id: 'UAI.org/2017/conference/-/Add/Revision',
    signatures: ['UAI.org/2017/conference'],
    writers: ['UAI.org/2017/conference'],
    invitees: note.signatures,
    noninvitees: [],
    readers: ['everyone'],
    process: 'function() { done() return true; }',
    reply: {
      forum: note.id,
      referent: note.id,
      signatures: invitation.reply.signatures,
      writers: invitation.reply.writers, 
      readers: invitation.reply.readers,
      content: invitation.reply.content
    }    
  }  


  var list = note.invitation.replace(/_/g,' ').split('/')
  list.splice(list.indexOf('-',1));
  var conference = list.join(' ');
  //Send an email to the author of the submitted note, confirming its receipt

  var mail = {
    "groups": note.content.author_emails.trim().split(","),
    "subject": "Confirmation of your submission to " + conference + ": \"" + note.content.title + "\".",
    "message": `Your submission to `+ conference +` has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
  };
  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token )
  
  // Create an empty group for this paper, e.g. "UAI.org/2017/conference/paper444"
  var paperGroup = {
    'id': 'UAI.org/2017/conference/paper'+note.number,
    'signatures': ['UAI.org/2017/conference'],
    'writers': ['UAI.org/2017/conference','UAI.org/2017/pcs'],
    'members': [],
    'readers': ['everyone'],
    'signatories': ['UAI.org/2017/conference', 'UAI.org/2017/conference/paper'+note.number]
  };

  var reviewerGroup = {
    'id': paperGroup.id+'/reviewers',
    'signatures':['UAI.org/2017/conference'],
    'writers':['UAI.org/2017/conference','UAI.org/2017/pcs'],
    'members':[],
    'readers':['everyone'],
    'signatories':['UAI.org/2017/conference',paperGroup.id+'/reviewers']
  };

  openReviewInvitation.noninvitees.push(reviewerGroup.id);
  publicCommentInvite.noninvitees.push(reviewerGroup.id);

  var reviewNonreadersGroup = {
    'id': paperGroup.id+'/review-nonreaders',
    'signatures':['UAI.org/2017/conference'],
    'writers':['UAI.org/2017/conference','UAI.org/2017/pcs'],
    'members':[],
    'readers':['everyone'],
    'signatories':['UAI.org/2017/conference',paperGroup.id+'/review-nonreaders']
  }

  var authorGroup = {
    'id':paperGroup.id+'/authors',
    'signatures':['UAI.org/2017/conference'],
    'writers':['UAI.org/2017/conference','UAI.org/2017/pcs'],
    'members': note.content.author_emails.trim().split(","),
    'readers':['everyone'],
    'signatories':['UAI.org/2017/conference',paperGroup.id+'/authors']
  };

  var areachairGroup = {
    'id':paperGroup.id+'/areachairs',
    'signatures':['UAI.org/2017/conference'],
    'writers':['UAI.org/2017/conference','UAI.org/2017/pcs'],
    'members':[],
    'readers':['everyone'],
    'signatories':['UAI.org/2017/conference',paperGroup.id+'/areachairs']
  };



  or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token)
  .then(result=>{
    group_promises = [
      or3client.or3request(or3client.grpUrl, reviewerGroup, 'POST', token),  
      or3client.or3request(or3client.grpUrl, reviewNonreadersGroup, 'POST', token),  
      or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
      or3client.or3request(or3client.grpUrl, areachairGroup, 'POST', token),
    ];

    return Promise.all(group_promises);    
  })
  .then(result=>{
    invitation_promises = [
      or3client.or3request(or3client.inviteUrl, metaReviewInvitation, 'POST', token),
      or3client.or3request(or3client.inviteUrl, openReviewInvitation, 'POST', token),
      or3client.or3request(or3client.inviteUrl, officialReviewInvitation, 'POST', token),
      or3client.or3request(or3client.inviteUrl, reviewerQuestionInvite, 'POST', token),
      or3client.or3request(or3client.inviteUrl, publicCommentInvite, 'POST', token),
      or3client.or3request(or3client.inviteUrl, officialCommentInvite, 'POST', token),
      or3client.or3request(or3client.inviteUrl, acceptanceInvite, 'POST', token),
      or3client.or3request(or3client.inviteUrl, referenceInvite, 'POST', token)
    ];

    return Promise.all(invitation_promises);
  })
  .then(result=>{
    done();
  })
  .catch(error=>done(error));

  return true;
};