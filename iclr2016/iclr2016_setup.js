#!/usr/bin/env node
var url = process.argv[2] || 'http://localhost:3000';

var or3client = require('../../or3/client').mkClient(url);
var fs = require('fs');
var iclr_params = require('./iclr2016_params.js')

// The open review local url
var grpUrl = or3client.grpUrl;
var loginUrl = or3client.loginUrl;
var regUrl = or3client.regUrl;
var inviteUrl = or3client.inviteUrl;
var mailUrl = or3client.mailUrl;
var notesUrl = or3client.notesUrl;

var u1 = iclr_params.pcs.u1;
var u2 = iclr_params.pcs.u2;
var u3 = iclr_params.pcs.u3;
var iclr = iclr_params.iclr;
var iclr16 = iclr_params.iclr16;
var workshop = iclr_params.workshop;
var conference = iclr_params.conference;
var paper = iclr_params.paper;

var rootUser = {
  'id': 'OpenReview.net',
  'password': '12345678'
}

var submissionProcess = function() {
  var or3client = lib.or3client;

  //create a comment invitation
  var comment_invite = or3client.createCommentInvitation(
    { 'id': 'ICLR.cc/2016/workshop/-/paper/'+count+'/comment',
      'signatures':['ICLR.cc/2016/workshop'],
      'writers':['ICLR.cc/2016/workshop'],
      'invitees': ['~'],
      'process':or3client.commentProcess+'',
      'reply': { 
        'forum': note.forum,
      }
    }
  );

  or3client.or3request(or3client.inviteUrl, comment_invite, 'POST',token).catch(error=>console.log(error));

  //create a review invitation
  var review_invitation = or3client.createReviewInvitation(
    { 'id': 'ICLR.cc/2016/workshop/-/paper/' + count + '/unofficial_review',
      'signatures': ['ICLR.cc/2016/workshop'],
      'writers': ['ICLR.cc/2016/workshop'],
      'invitees': ['~'],
      'noninvitees': note.content.author_emails.trim().split(","),
      'process': or3client.reviewProcess+'',
      'reply':{
        'forum': note.id, 
        'parent': note.id,
        'writers': {'values-regex':'~.*|reviewer-.+'},
        'signatures': {'values-regex':'~.*|reviewer-.+'},
      }
    }
  );
  or3client.or3request(or3client.inviteUrl, review_invitation, 'POST', token).catch(error=>console.log(error));
  
  return true;
};

or3client.getUserTokenP(rootUser).then(function(token){
  or3client.or3request(regUrl, u1, 'POST', token)
  .then(result=> or3client.or3request(regUrl, u2, 'POST', token))
  .then(result=> or3client.or3request(regUrl, u3, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr16, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, workshop, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, conference, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, paper, 'POST', token))
  .then(result=> or3client.addHostMember("ICLR.cc/2016/workshop", token))
  .then(result=> or3client.or3request(inviteUrl, or3client.createSubmissionInvitation(
    { 
      'id':workshop.id+'/-/submission', 
      'signatures':[workshop.id], 
      'writers':[workshop.id], 
      'invitees':['~'],
      'process':submissionProcess+"" 
    }
  ), 'POST', token))
  .then(result => or3client.addHostMember(workshop.id, token))
  .then(result => console.log(workshop.id+' added to homepage'))
})
