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
  'password': '12345678'
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

// NOTE RESPONDING TO SIMPLE INVITATION
var subInv = {
    'invitation': 'arisconf/-/simple',
    //    'id':             // I think this should be specified automatically?
    'forum': null,      // should this be set automatically?
    'parent': null,     // should this be set to whatever is being commented on?
    'authors': ['~Ari_Kobren'],
    'writers': ['~Ari_Kobren'],
    'readers': ['*'],
    'content': {
	'title': 'A Paper that I wrote one time'
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
