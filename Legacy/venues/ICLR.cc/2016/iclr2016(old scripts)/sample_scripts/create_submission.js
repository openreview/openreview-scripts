#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var noteUrl = 'http://localhost:8529/_db/_system/openreview/notes';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
  'id': 'ari@host.com',
  'password': ''
};

function or3post(url, body, headers) {
  this.url = url;
  this.method = 'POST';
  this.port = 8529;
  this.json = true;
  this.body = body;
  this.headers = headers;
}

function callback(error, response, body) {
  if (!error && response.statusCode == 200) {
      console.log("SUCCESS");
      console.log(response);
      console.log(body);
  } else {
  console.log("ERROR: " + error);
  console.log("RESPONSE: " + response.statusCode);
  }
}

function loggedInHdr(token) {
  return {
  'Authorization': 'Bearer ' + token,
  'User-Agent': 'test-create-script'
  };
}

// INVITATION TO SUBMIT PAPER
var subInv = {
    'invitation': 'arisconf/-/submission',
    'forum': null,      // should this be set automatically?
    'parent': null,     // should this be set to whatever is being commented on?
    'authors': ['~Ari_Kobren'],
    'writers': ['~Ari_Kobren'],
    'readers': ['*'],
    'content': {
	'title': 'Submitting a paper with abstract',
	'abstract': 'The abstract of some paper who knows',
	'authors': ['Ari Kobren'],
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    },
    'process': function(noteID) {
  	return true;  	       //send email to paper’s authors’ and reviewers’ email addresses
    }
};

function create_submission_invite(url, o) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var commentInvite = new or3post(url, o, loggedInHdr(token));
	console.log(commentInvite);
	request(commentInvite, callback);
    }
  });
}

create_submission_invite(noteUrl, subInv);
