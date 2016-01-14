#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
  'id': 'ari@host.com',
  'password': '12345678'
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
  'User-Agent': 'test-create-script',
  };
}

// GROUPS TO CREATE
var iclr16 = {
    'id': 'ICLR.cc/2016',
    'authors': ['ICLR.cc'],
    'writers': ['ICLR.cc/2016'],
    'readers': ['*'],
    'members': ['u1@host.com','u2@host.com', 'u3@host.com'],
    'signatories': ['ICLR.cc/2016']
};

function make_post_req(url, o) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var or3postReq = new or3post(url, o, loggedInHdr(token));
	request(or3postReq, callback);
    }
  });
}

make_post_req(grpUrl,iclr16);
