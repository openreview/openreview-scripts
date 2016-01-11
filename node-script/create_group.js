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
    console.log("SUCCESS")
    console.log(body)
  } else {
  console.log("BODY");
  console.log(body);
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

// GROUP TO CREATE
var group = {
  'id': 'arisgroup3',
  'authors': ['ari@host.com'],
  'writers': ['akobren@host.com','ari@host.com'],
  'readers': ['akobren@host.com','ari@host.com'],
  'members': ['akobren@host.com','ari@host.com'],
  'signatories': ['ari@host.com']
};

// REVIEWER
var reviewer = {
  'id': 'iclr/paper/123/reviewer/1',
  'authors': ['ari@host.com'],
  'writers': ['ari@host.com'],
  'members': ['akobren@host.com'],
  'signatories': ['iclr/paper/123/reviewer/1'],
  'readers': ['ari@host.com', 'akobren@host.com'],
  'nonreaders': ['ICLR.cc/2016/akobren@host.com/conflicts']
};

// REVIEWER
var reviewer = {
  'id': 'iclr/paper/123/reviewer/1',
  'authors': ['ari@host.com'],
  'writers': ['ari@host.com'],
  'members': ['ari@host.com'],
  'signatories': ['ari@host.com'],
  'readers': ['ari@host.com'],
  'nonreaders': ['ICLR.cc/2016/akobren@host.com/conflicts']
};


// FAKE CONFERENCE
var ariConf = {
  'id': 'arisconf',
  'authors': ['ari@host.com'],
  'writers': ['ari@host.com'],
  'members': ['ari@host.com'],
  'signatories': ['arisconf/pc'],
  'readers': ['*'],
};

// FAKE CONFERENCE
var ariConfPart = {
  'id': 'arisconf/participants',
  'authors': ['arisconf'],
  'writers': ['arisconf'],
  'members': ['*'],
  'readers': ['*']
};

function create_group(g) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var createGrp = new or3post(grpUrl, g, loggedInHdr(token));
	console.log("CREATING GROUP:");
	console.log(createGrp);
	request(createGrp, callback);
    }
  });
}

create_group(ariConfPart)
