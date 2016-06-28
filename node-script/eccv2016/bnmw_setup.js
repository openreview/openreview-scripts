/*
  This script sets the basic settings for the ECCV BNMW conference from scratch.
*/

var url = process.argv[2] || 'http://localhost:3000';

var or3client = require('../../../or3/client').mkClient(url);
var bnmw = require('./bnmw_params.js')
var fs = require('fs');
var _ = require('lodash');

var grpUrl = or3client.grpUrl;
var loginUrl = or3client.loginUrl;
var regUrl = or3client.regUrl;
var inviteUrl = or3client.inviteUrl;
var mailUrl = or3client.mailUrl;
var notesUrl = or3client.notesUrl;

var headers = bnmw.headers;
var rootUser = bnmw.rootUser;
var eccv = bnmw.eccv;
var workshop = bnmw.workshop;
var paper = bnmw.paper;
var noteBody = bnmw.noteBody;
var email1 = bnmw.email1;
var email2 = bnmw.email2;
var wrapper_group1 = bnmw.wrapper_group1;
var wrapper_group2 = bnmw.wrapper_group2;

//REMINDER: Any variables in the submissionProcess function must be accessible from 'lib'
var submissionProcess = function () {
  var or3client = lib.or3client;
  console.log(lib)
  var list = note.invitation.split('/')
  list.splice(list.indexOf('-',1));
  var conference = list.join('/')
  
  var comment_invite = or3client.createCommentInvitation(
    { 'id': 'ECCV2016.org/BNMW/paper/-/'+count+'/comment',
      'signatures':['ECCV2016.org/BNMW'],
      'writers':['ECCV2016.org/BNMW'],
      'invitees': ['~'],
      'process':or3client.commentProcess+'',
      'reply': { 
        'forum': note.forum
      }
    }

  );
  or3client.or3request(or3client.inviteUrl, comment_invite, 'POST',token).catch(error=>console.log(error));

  var open_review_invitation = or3client.createReviewInvitation(
    { 'id': 'ECCV2016.org/BNMW/paper/-/open/review/'+note.id,
      'signatures': ['ECCV2016.org/BNMW'],
      'writers': ['ECCV2016.org/BNMW'],
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

  return true;
};

or3client.getUserTokenP(rootUser).then(function(token){
  or3client.or3request( grpUrl, eccv, 'POST', token)
  .then(result => console.log(eccv.id+' group posted'))
  .then(result => or3client.or3request(grpUrl, workshop, 'POST', token))
  .then(result => console.log(workshop.id+' group posted'))
  .then(result => or3client.or3request(grpUrl, paper, 'POST', token))
  .then(result => console.log(paper.id+' group posted'))
  .then(result => or3client.or3request(inviteUrl, or3client.createSubmissionInvitation(
    { 'id':workshop.id+'/-/submission', 
      'signatures':[workshop.id], 
      'writers':[workshop.id], 
      'invitees':['~'], 
      'process':submissionProcess+""
    }
  ), 'POST', token))
  .then(result => console.log('submission invitation posted'))
  .then(result => or3client.or3request(grpUrl, wrapper_group1, 'POST', token))
  .then(result => console.log(wrapper_group1.id+' group posted'))
  .then(result => or3client.or3request(grpUrl, wrapper_group2, 'POST', token))
  .then(result => console.log(wrapper_group2.id+' group posted'))
  .then(hostGroup => or3client.addHostMember(workshop.id, token))
  .then(result => console.log(workshop.id+' added to homepage'))
  .then(result => console.log('SETUP COMPLETE'));
  
})
