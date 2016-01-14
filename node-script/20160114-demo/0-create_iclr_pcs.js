#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';

var headers = { 'User-Agent': 'test-create-script' };

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

var headers = {};
request(new or3post(grpUrl, u1, headers), callback);
request(new or3post(grpUrl, u2, headers), callback);
request(new or3post(grpUrl, u3, headers), callback);
