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
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'Test Paper 1',
	'abstract': 'The abstract of test paper 1',
	'authors': 'Ari Kobren',
	'conflicts': 'umass.edu',
	'CMT_id': '',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

var sub2 = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1','~Ari_Kobren2'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'Test Paper 2',
	'abstract': 'The paper has two authors',
	'authors': 'Ari Kobren, Ari Kobren 2',
	'conflicts': 'umass.edu',
	'CMT_id': '',
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
make_post_req(noteUrl, sub2);
