#!/usr/bin/env node

var assert = require('assert');
// we use this request library instead of node's because
// some or3 code will be forced to use this library for now
//var request = require('org/arangodb/request');
// This is the alternative node.js request library
var request = require('request');


// The open review local url
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';

var headers = { 'User-Agent': 'or3-tests' };

//USERS
var root = {
    'id': 'OpenReview.net',
    'password': ''
};

var u1 = {
    'id': 'u1@host.com',
    'password': ''
};

// the body is a json object that will be sent
// via post to the or3 server. The rest of the
// object that is returned is boilerplate for or3.
// For now the headers are unimportant.
function or3Post(url, body, headers) {
  this.url = url;
  this.method = 'POST';
  this.port = 8529;
  this.json = true;
  this.body = body;
  this.headers = headers;
}

// a function that returns an objection that contains
// the token of a logged in user. This is meant to go
// in the header of an http request (to make that request
// as if the requester were logged in with the
// corresponding credentials.
function loggedInHdr(token) {
  return {
  'Authorization': 'Bearer ' + token
  };
}

// first make a login request with the input  username an password;
// store the corresponding login token and use it to make a request
// to the input url with the input object
function makeOR3Post(userpass, url, o) {
    var loginReq = new or3Post(loginUrl, userpass, headers);
    return request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
          var token = body.token;
	  var or3postReq = new or3post(url, o, loggedInHdr(token));
	  request(or3postReq, callback);
      } else {
	  assert.equal(true, false);
      }
    });
}

function callback(error, response, body) {
  if (!error && response.statusCode == 200) {
      assert.equal(true, true);
  } else {
      assert.equal(true, false);
  }
}

// SINGLE, COMPATIBLE authors AND writers
var iclr = {
    'id': 'ICLR.cc',
    'authors': ['u1@host.com'],
    'writers': ['u1@host.com'],
    'members': ['u1@host.com'],
    'readers': ['u1@host.com'],
    'signatories': ['u1@host.com']
};


describe('Group Creation', function() {
    describe('Create top-level group as root', function() {
	it('should return the id of the created group', function () {
	    assert.equal(false, true);
	});
    });

    describe('Create group with single, compatible  author and writer', function() {
	it('should SUCCEED; and return the id of the create group', function() {
	    makeOR3Post(u1, grpUrl, or3Post(u1, grpUrl, iclr));
	});
    });
});
