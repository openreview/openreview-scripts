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

// ICLR SUBMISSION
var sub = {
    'invitation': 'ICLR.cc/2016/-/workshop/submission',
    'forum': null,
    'parent': null,
    'authors': ['~Ari_Kobren'],
    'writers': ['~Ari_Kobren'],
    'readers': ['*'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'My Title',
	    'abstract': 'My Abstract',
	    'authors': 'Ari Kobren,',
	    'conflicts': 'umass.edu;',
	    'resubmit': 'Yes',
	    'cmtID': '98',
	    'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

function make_post_req(url, o) {
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

make_post_req(noteUrl, sub);
