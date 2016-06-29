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
var iclrSub = {
    'invitation': 'ICLR.cc/2016/-/workshop11/submission',
    'forum': null,        // this will be set automatically
    'parent': null,       // this will be the root of the forum
    'authors': ['~Ari_Kobren'],
    'writers': ['~Ari_Kobren'],
    'readers': ['*'],
    'content': {
	'title': 'workshop10 submission',
	'abstract': 'this is my abstract',
	'authors': 'Ari Kobren',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'   // either an actual pdf or an arxiv link
    }
};

function make_post_req(url, o) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var post = new or3post(url, o, loggedInHdr(token));
	console.log(post);
	request(post, callback);
    }
  });
}

make_post_req(noteUrl, iclrSub);
