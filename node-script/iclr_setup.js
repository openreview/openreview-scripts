#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var or3 = require('../../or3/client');
var iclr_params = require('./iclr_params.js')

// The open review local url
var grpUrl = or3.grpUrl;
var loginUrl = or3.loginUrl;
var regUrl = or3.regUrl;
var inviteUrl = or3.inviteUrl;
var mailUrl = or3.mailUrl;
var notesUrl = or3.notesUrl;

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
      'invitees': ['~']
    },
    { 'forum': note.forum,
      'process':or3client.commentProcess 
    }
  );
  or3client.or3request(or3client.inviteUrl, comment_invite, 'POST',token).catch(error=>console.log(error));

  //create a review invitation
  var review_invitation = or3client.createReviewInvitation(

    { 'id': 'ICLR.cc/2016/workshop/-/paper/' + count + '/unofficial_review',
      'signatures': ['ICLR.cc/2016/workshop'],
      'writers': ['ICLR.cc/2016/workshop'],
      'invitees': ['~'],
      'noninvitees': note.content.author_emails.trim().split(",")
    },
    { 'forum': note.id, 
      'parent': note.id,
      'writers': {'values-regex':'~.*|reviewer-.+'},
      'signatures': {'values-regex':'~.*|reviewer-.+'},
      'process': or3client.reviewProcess;
    }
  );
  or3client.or3request(or3client.inviteUrl, review_invitation, 'POST', token).catch(error=>console.log(error));
  
  return true;
};

or3.getUserTokenP(rootUser).then(function(token){
  or3.or3request(regUrl, u1, 'POST', token)
  .then(result=> or3.or3request(regUrl, u2, 'POST', token))
  .then(result=> or3.or3request(regUrl, u3, 'POST', token))
  .then(result=> or3.or3request(grpUrl, iclr, 'POST', token))
  .then(result=> or3.or3request(grpUrl, iclr16, 'POST', token))
  .then(result=> or3.or3request(grpUrl, workshop, 'POST', token))
  .then(result=> or3.or3request(grpUrl, conference, 'POST', token))
  .then(result=> or3.or3request(grpUrl, paper, 'POST', token))
  .then(result=> or3.addHostMember("ICLR.cc/2016/workshop", token))
  .then(result=> or3.or3request(inviteUrl, or3.createSubmissionInvitation({ 
    'id':workshop.id+'/-/submission', 
    'signatures':[workshop.id], 
    'writers':[workshop.id], 
    'invitees':['~'],
    'process':submissionProcess+"" 
  }), 'POST', token))
  .then(result => or3.addHostMember(workshop.id, token))
  .then(result => console.log(workshop.id+' added to homepage'))


})
