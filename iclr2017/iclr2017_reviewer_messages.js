#!/usr/bin/env node
var url = process.argv[2] || 'http://localhost:3000';

var or3client = require('../../or3/client').mkClient(url);
var fs = require('fs');
var iclr_params = require('./iclr2017_params.js')

var grpUrl = or3client.grpUrl;
var loginUrl = or3client.loginUrl;
var regUrl = or3client.regUrl;
var inviteUrl = or3client.inviteUrl;
var mailUrl = or3client.mailUrl;
var notesUrl = or3client.notesUrl;

var rootUser = {
  'id': 'OpenReview.net',
  'password': '12345678'
};

var messageProcess = function(){

  return true;
};


or3client.getUserTokenP(rootUser).then(function(token){

  var invite = or3client.createCommentInvitation({
    'id': 'iclr.cc/2017/workshop/-/reviewer/message',
    'signatures':['iclr.cc/2017/workshop'],
    'writers':['iclr.cc/2017/workshop'],
    'invitees': ['iclr.cc/2017/workshop/areachairs/1'],
    'readers': ['iclr.cc/2017/workshop/areachairs'],
    'process':messageProcess+'',
    'reply': { 
      'forum': 'p8DR1mRqQinQVOGWf878',
      'content': {
        'Subject': {
          'order': 1,
          'value-regex': '.{1,500}',
          'description': 'Subject line of your message.'
        },
        'Message': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Your message.'
        },
        'readers': {
          'order': 3,
          'values-regex': '~.*',
          'description':'Who will receive this message.'
        } 
      }
    }
  });
  or3client.or3request(inviteUrl, invite, 'POST', token)

})