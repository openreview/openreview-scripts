#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var regUrl = 'http://localhost:80/register';
var grpUrl = 'http://localhost:80/groups';
var loginUrl = 'http://localhost:80/login';

var headers = { 'User-Agent': 'test-create-script' };

var rootUsr = {
    'id': 'OpenReview.net',
    'password': '12345678'
}

//PCs
var u1 = {
    'id': 'u1@host.com',
    'needsPassword': true
};

var u2 = {
    'id': 'u2@host.com',
    'needsPassword': true
};

var u3 = {
    'id': 'u3@host.com',
    'needsPassword': true
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
  'User-Agent': 'test-create-script',
  };
}

function make_post_req(url, o) {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var or3postReq = new or3post(url, o, loggedInHdr(token));
	request(or3postReq, callback);
    }
  });
}

make_post_req(regUrl, u1);
make_post_req(regUrl, u2);
make_post_req(regUrl, u3);
