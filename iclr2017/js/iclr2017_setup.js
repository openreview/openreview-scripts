var url = process.argv[2] || 'http://localhost:3000';

var or3client = require('../../../or3/client').mkClient(url);
var fs = require('fs');
var iclr_params = require('./iclr2017_params.js')

// The open review local url
var grpUrl = or3client.grpUrl;
var loginUrl = or3client.loginUrl;
var regUrl = or3client.regUrl;
var inviteUrl = or3client.inviteUrl;
var mailUrl = or3client.mailUrl;
var notesUrl = or3client.notesUrl;

//REMINDER: Any variables in the submissionProcess function must be accessible from 'lib'
var submissionProcess = function () {
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
    'process':messageProcess+'',
    'reply': { 
      'forum': note.forum,
      'readers': { 
        'values-regex': '~.*',        
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
  or3client.or3request(or3client.inviteUrl, publicCommentInvite, 'POST', token).catch(error=>console.log(error));

  return true;
};


or3client.getUserTokenP(iclr_params.rootUser).then(function(token){
  or3client.or3request(grpUrl, iclr_params.iclr, 'POST', token)

  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017conference, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017conferenceProgramChairs, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017conferenceAreaChairs, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.programChair1, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.areaChair1, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.areaChair2, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.areaChair1reviewers, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.areaChair2reviewers, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.reviewer1, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.reviewer2, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.reviewer3, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.reviewer4, 'POST', token))
  .then(result=> or3client.or3request(inviteUrl, or3client.createSubmissionInvitation({ 
        'id':iclr_params.iclr2017conference.id+'/-/submission', 
        'signatures':[iclr_params.iclr2017conference.id],
        'writers':[iclr_params.iclr2017conference.id], 
        'invitees':['~'],
        'process':submissionProcess+'',
        'reply':{
          'content': {
            'title': {
              'order': 3,
              'value-regex': '.{1,100}',
              'description': 'Title of paper.'
            },
            'abstract': {
              'order': 4,
              'value-regex': '[\\S\\s]{1,5000}',
              'description': 'Abstract of paper.'
            },
            'authors': {
              'order': 1,
              'value-regex': '[^,\\n]+(,[^,\\n]+)*',
              'description': 'Comma separated list of author names, as they appear in the paper.'
            },
            'author_emails': {
              'order': 2,
              'value-regex': '[^,\\n]+(,[^,\\n]+)*',
              'description': 'Comma separated list of author email addresses, in the same order as above.'
            },
            'conflicts': {
              'order': 100,
              //'value-regex': '[^,\\n]+(,[^,\\n]+)*',
              'value-regex': "^([a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))+(;[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))*$",
              'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).'
            },
            'pdf': {
              'order': 4,
              'value-regex': 'upload|http://arxiv.org/pdf/.+',   // either an actual pdf or an arxiv link
              'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv.'
            },          
            'keywords': {
              'order': 5,
              //'value-regex': '[^,\\n]+(,[^,\\n]+)*',
              'values-regex': '.*',
              'description': 'Comma separated list of keywords.'
            }
          }
        }
      }), 'POST', token))
  .then(result => or3client.addHostMember(iclr_params.iclr2017conference.id, token))
  .then(result => or3client.or3request(notesUrl, iclr_params.note1, 'POST',token))
  
})