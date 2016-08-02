#!/usr/bin/env node

var request = require('request');

// The open review local url
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
  'id': 'ari@host.com',
  'password': ''
};

function or3post(url, body, headers) {
  this.url = url;
  this.method = 'POST';
  this.port = 80;
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

function create_usr_no_pass(email) {
    return {
	'id': email,
	'needsPassword': true
    };
}

function post_req(url, o) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
	if (!error && response.statusCode == 200) {
            var token = body.token;
	    var or3obj = new or3post(url, o, loggedInHdr(token));
	    request(or3obj, callback);
	}
    });
}

post_req(grpUrl, create_usr_no_pass('123@g.com'));
post_req(grpUrl, create_usr_no_pass('123@g.com'));
