function () {
  var or3client = lib.or3client;

  var metaReviewProcess = function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);

    var programchairs = ['auai.org/UAI/2017/Chairs'];

    origNote.then(function(result){
      var forum = result.notes[0]

      var pc_mail = {
        "groups": programchairs,
        "subject": "[UAI 2017] Meta-review by area chair posted: "+ "\"" + forum.content.title + "\".",
        "message": "A paper submission to UAI 2017 has received a meta-review by an area chair.\n\nTitle: "+note.content.title+"\n\nMeta-review: "+note.content.metareview+"\n\nTo view the meta-review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var promises = [
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
    'id': 'auai.org/UAI/2017/-/paper'+note.number+'/Meta/Review',
    'signatures': ['auai.org/UAI/2017'],
    'writers': ['auai.org/UAI/2017'],
    'invitees': ['auai.org/UAI/2017/paper'+note.number+'/Area_Chair'],
    'noninvitees':[],
    'readers': ['auai.org/UAI/2017','auai.org/UAI/2017/Senior_Program_Committee','auai.org/UAI/2017/Chairs'],
    'process': metaReviewProcess+'',
    'duedate': 1507180500000, //duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
    'reply': {
      'forum': note.id,
      'replyto': note.id,
      'writers': {'values-regex':'auai.org/UAI/2017/paper'+note.number+'/Area_Chair'},
      'signatures': {'values-regex':'auai.org/UAI/2017/paper'+note.number+'/Area_Chair'},
      'readers': {
        'values': ['auai.org/UAI/2017/Chairs'],
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

  var reviewProcess = function(){
    var or3client = lib.or3client;

    var origNote = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var list = note.invitation.replace(/_/g,' ').split('/');
    list.splice(list.indexOf('-',1));
    var conference = list.join(' ');

    origNote.then(function(result){
      var note_number = result.notes[0].number;
      var origNoteTitle = result.notes[0].content.title;
      var reviewers = ['auai.org/UAI/2017/paper'+note_number+'/Reviewers'];
      var areachairs = ['auai.org/UAI/2017/paper'+note_number+'/Area_Chair'];
      var authors = result.notes[0].content.authorids;

      var author_mail = {
        "groups": authors,
        "subject": "Review of your submission to UAI 2017: \"" + origNoteTitle + "\"",
        "message": "Your submission to UAI 2017 has received an official review.\n\nTitle: "+note.content.title+"\n\nReview: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
      };

      var areachair_mail = {
        "groups": areachairs,
        "subject": "Review posted to your assigned paper: \"" + origNoteTitle + "\"",
        "message": "A submission to UAI 2017, for which you are an official area chair, has received an official review. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.review+"\n\nTo view the review, click here: "+baseUrl+"/forum?id=" + note.forum
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


  var reviewInvitation = {
    'id': 'auai.org/UAI/2017/-/paper'+note.number+'/Review',
    'signatures': ['auai.org/UAI/2017'],
    'writers': ['auai.org/UAI/2017'],
    'invitees': ['auai.org/UAI/2017/paper'+note.number+'/Reviewers'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process': reviewProcess+'',
    'duedate': 1507180500000, //duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
    'reply': {
      'forum': note.id,
      'replyto': note.id,
      'writers': {'values-regex':'auai.org/UAI/2017/paper'+note.number+'/AnonReviewer[0-9]+'},
      'signatures': {'values-regex':'auai.org/UAI/2017/paper'+note.number+'/AnonReviewer[0-9]+'},
      'readers': {
        'values': ['auai.org/UAI/2017/Senior_Program_Committee'], //only Senior_Program_Committee initially; when a reviewer submits his/her review, they are added to the readers
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

  var commentProcess = function(){
    var or3client = lib.or3client;

    var getAuthorEmails = function(forumNote){
      console.log('get author emails initiated')
      var forumNoteAuthors = forumNote.content.authorids;
      var forumNoteSignature = forumNote.signatures[0];

      var author_mail = {
        "groups": forumNoteAuthors,
        "subject": "Comment on your submission to UAI 2017: \"" + note.content.title + "\".",
        "message": "Your submission to UAI 2017 has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
    };

    var getReviewerEmails = function(forumNoteNumber){
      console.log('get reviewer emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/paper'+forumNoteNumber+'/Reviewers',{},'GET',token)
      .then(result=>{
        var reviewers = result.groups[0].members;

        //if the comment writer is a reviewer, don't send an email to him/herself
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if(signatureIdx>-1){
          reviewers.splice(signatureIdx,1);
        };

        var reviewer_mail = {
          "groups": reviewers,
          "subject": "Comment posted to your assigned paper: \"" + note.content.title + "\"",
          "message": "A submission to UAI 2017, for which you are an official reviewer, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      })
    };

    var getAreachairEmails = function(forumNoteNumber){
      console.log('get AC emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/paper'+forumNoteNumber+'/Area_Chair',{},'GET',token)
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
          "message": "A submission to UAI 2017, for which you are an official area chair, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );
      })
    };

    var getPCEmails = function(){
      console.log('get Program_Committee emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/Chairs',{},'GET',token)
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
          "message": "A submission to UAI 2017 has received a private comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
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

    var forumNoteP = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl+'?id='+note.replyto,{},'GET',token) : null;

    Promise.all([
      forumNoteP,
      replytoNoteP
    ]).then(result => {
      var forumNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteReaders = replytoNote ? replytoNote.readers : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : null;

      var promises = [];

      var visibleToEveryone = note.readers.indexOf('everyone')>-1 ? true : false;
      var visibleToReviewers = note.readers.indexOf('auai.org/UAI/2017/Program_Committee')>-1 ? true : false;
      var visibleToAreachairs = note.readers.indexOf('auai.org/UAI/2017/Senior_Program_Committee')>-1 ? true : false;
      var visibleToPCs = note.readers.indexOf('auai.org/UAI/2017/Chairs')>-1 ? true : false;

      if(visibleToEveryone){
        var authorMailP = getAuthorEmails(forumNote);
        promises.push(authorMailP);
      };

      if(visibleToEveryone || visibleToReviewers){
        var reviewerMailP = getReviewerEmails(forumNote.number);
        promises.push(reviewerMailP);
      };

      if(visibleToEveryone || visibleToReviewers || visibleToAreachairs){
        var areachairMailP = getAreachairEmails(forumNote.number);
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


  var confidentialCommentInvite = {
    'id': 'auai.org/UAI/2017/-/paper'+note.number+'/Confidential/Comment',
    'signatures':['auai.org/UAI/2017'],
    'writers':['auai.org/UAI/2017'],
    'invitees': ['auai.org/UAI/2017/Program_Committee','auai.org/UAI/2017/Senior_Program_Committee'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process':commentProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'replyto': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.+',
        'description': 'How your identity will be displayed with the above content.'
        },
      'writers': {'values-regex':'~.+'},
      'readers': {
        'values-dropdown': [
          'auai.org/UAI/2017/Chairs',
          'auai.org/UAI/2017/Senior_Program_Committee',
          'auai.org/UAI/2017/Program_Committee'
        ],
        'description': 'The users who will be allowed to read the above content.'
        },
      'content': {
        'title': {
          'order': 1,
          'value-regex': '.{1,500}',
          'description': 'Brief summary of your comment.',
          'required':true
        },
        'comment': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your comment or reply.',
          'required':true
        }
      }
    }
  };

  var openCommentInvite = {
    'id': 'auai.org/UAI/2017/-/paper'+note.number+'/Open/Comment',
    'signatures':['auai.org/UAI/2017'],
    'writers':['auai.org/UAI/2017'],
    'invitees': ['auai.org/UAI/2017/Program_Committee','auai.org/UAI/2017/Senior_Program_Committee'],
    'noninvitees':[],
    'readers': ['everyone'],
    'process':commentProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      //'replyto': noteID,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.+',
        'description': 'How your identity will be displayed with the above content.'
        },
      'writers': {'values-regex':'~.+'},
      'readers': {
        'values': ['everyone'],
        'description': 'The users who will be allowed to read the above content.'
      },
      'content': {
        'title': {
          'order': 1,
          'value-regex': '.{1,500}',
          'description': 'Brief summary of your comment.',
          'required':true
        },
        'comment': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your comment or reply.',
          'required':true
        }
      }
    }
  };


  var bidProcess = function(){
    var or3client = lib.or3client;
    or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token)
    .then(result => done())
    .catch(error => done(error));
    return true;
  };

  var bidInvite = {
    'id': 'auai.org/UAI/2017/-/paper'+note.number+'/Reviewer_Bid',
    'signatures':['auai.org/UAI/2017'],
    'writers':['auai.org/UAI/2017'],
    'invitees': ['auai.org/UAI/2017/Program_Committee'],
    'noninvitees':['auai.org/UAI/2017/Senior_Program_Committee','auai.org/UAI/2017/Chairs'],
    'readers': ['everyone'],
    'process':bidProcess+'',
    'reply': {
      'forum': note.id,      // links this note (comment) to the previously posted note (paper)
      'replyto': note.id,    // not specified so we can allow comments on comments
      'signatures': {
        'values-regex':'~.+',
        'description': 'How your identity will be displayed with the above content.'
        },
      'writers': {'values-regex':'~.+'},
      'readers': {
        'values': ['auai.org/UAI/2017'],
        'description': 'The users who will be allowed to read the above content.'
      },
      'content': {
        'Preferences': {
            'order': 1,
            'value-radio': [
              'I want to review',
              'I can review',
              'I can probably review but am not an expert',
              'I cannot review'
            ],
            'required':true
        }
      }
    }
  };


  //Send an email to the author of the submitted note, confirming its receipt
  var mail = {
    "groups": note.content.authorids,
    "subject": "Confirmation of your submission to UAI 2017: \"" + note.content.title + "\".",
    "message": `Your submission to UAI 2017 has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
  };
  var mailP = or3client.or3request( or3client.mailUrl, mail, 'POST', token );

  // Create an empty group for this paper, e.g. "auai.org/UAI/2017/paper444"
  var paperGroup = {
    'id': 'auai.org/UAI/2017/paper'+note.number,
    'signatures': ['auai.org/UAI/2017'],
    'writers': ['auai.org/UAI/2017'],
    'members': [],
    'readers': ['everyone'],
    'signatories': ['auai.org/UAI/2017', 'auai.org/UAI/2017/paper'+note.number]
  };

  var reviewerGroup = {
    'id': paperGroup.id+'/Reviewers',
    'signatures':['auai.org/UAI/2017'],
    'writers':['auai.org/UAI/2017'],
    'members':[],
    'readers':['auai.org/UAI/2017/Chairs','auai.org/UAI/2017/Senior_Program_Committee',paperGroup.id+'/Reviewers'],
    'signatories':['auai.org/UAI/2017',paperGroup.id+'/Reviewers']
  };

  var authorGroup = {
    'id':paperGroup.id+'/Authors',
    'signatures':['auai.org/UAI/2017'],
    'writers':['auai.org/UAI/2017'],
    'members': note.content.authorids,
    'readers':['auai.org/UAI/2017/Chairs'],
    'signatories':['auai.org/UAI/2017',paperGroup.id+'/authors']
  };

  var areachairGroup = {
    'id':paperGroup.id+'/Area_Chair',
    'signatures':['auai.org/UAI/2017'],
    'writers':['auai.org/UAI/2017'],
    'members':[], //member to be added later by assignment script
    'readers':['auai.org/UAI/2017/Chairs','auai.org/UAI/2017/Senior_Program_Committee'],
    'signatories':['auai.org/UAI/2017',paperGroup.id+'/Area_Chair']
  };



  or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token)
  .then(result=>{
    group_promises = [
      or3client.or3request(or3client.grpUrl, reviewerGroup, 'POST', token),
      or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
      or3client.or3request(or3client.grpUrl, areachairGroup, 'POST', token),
    ];

    return Promise.all(group_promises);
  })
  .then(result=>{
    invitation_promises = [
      or3client.or3request(or3client.inviteUrl, metaReviewInvitation, 'POST', token),
      or3client.or3request(or3client.inviteUrl, reviewInvitation, 'POST', token),
      or3client.or3request(or3client.inviteUrl, confidentialCommentInvite, 'POST', token),
      or3client.or3request(or3client.inviteUrl, openCommentInvite, 'POST', token),
      or3client.or3request(or3client.inviteUrl, bidInvite, 'POST', token)
    ];

    return Promise.all(invitation_promises);
  })
  .then(result=>{
    done();
  })
  .catch(error=>done(error));

  return true;
};
