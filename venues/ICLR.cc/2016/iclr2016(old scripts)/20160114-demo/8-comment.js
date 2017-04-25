#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var notesUrl = 'http://localhost:8529/_db/_system/openreview/notes';
var mailUrl = 'http://localhost:8529/_db/_system/openreview/mail';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var rootUsr = {
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

var comment = {
    'invitation': 'ICLR.cc/2016/workshop/-/paper/1/comment',
    'forum': null,
    'parent': null,
    //		    'parent': noteID,    // not specified so we can allow comments on comments
    'signatures': ['~Ari_Kobren1'],    // this regex demands that the author reveal his/her ~ handle
    'writers': ['~Ari_Kobren1'],    // this regex demands that the author reveal his/her ~ handle
    'readers': ['everyone'],   // the reply must allow ANYONE to read this note (comment)
    'content': {
	'title': 'This is a test comment',
	'comment': 'What a great paper'
    }
};

function create_comment(url, o) {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var comment = new or3post(url, o, loggedInHdr(token));
	console.log(comment);
	request(comment, callback);
    }
  });
}

create_comment(notesUrl, comment);
