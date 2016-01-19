#!/usr/bin/env node

var assert = require('assert');
// we use this request library instead of node's because
// some or3 code will be forced to use this library for now
//var request = require('org/arangodb/request');
// This is the alternative node.js request library
var http = require('http');
var querystring = require('querystring');

// The open review local url
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';

var headers = { 'User-Agent': 'or3-tests' };

//USERS
var u1 = {
    'id': 'u1@host.com',
    'password': '12345678'
};

// the body is a json object that will be sent
// via post to the or3 server. The rest of the
// object that is returned is boilerplate for or3.
// For now the headers are unimportant.
function or3Post(url, body, headers) {
    return {
	'url': url,
	'method': 'POST',
	'port': 8529,
	'json': true,
	'body': body,
	'headers': headers
    };
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
function makeLoginReq(userpass) {
    var loginReq = new or3Post(loginUrl, userpass, headers);
    var resp = request(loginReq);
    console.log(resp);
    console.log(resp.body);
    console.log(resp.json);
    console.log(resp.statusCode);
    return resp;
}

describe('User Login', function() {
    describe('Activated User', function() {
	it('should be able to log in', function () {
	    var postData = querystring.stringify({
		'msg' : 'Hello World!'
	    });

	    var loginReq = or3Post(loginUrl, u1, {});
	    var req = http.request(loginReq, (res) => {
		console.log(`STATUS: ${res.statusCode}`);
		console.log(`HEADERS: ${JSON.stringify(res.headers)}`);
		res.setEncoding('utf8');
		res.on('data', (chunk) => {
		    console.log(`BODY: ${chunk}`);
		});
		res.on('end', () => {
		    console.log('No more data in response.');
		});
	    });

	    req.on('error', (e) => {
		console.log(`problem with request: ${e.message}`);
	    });

	    // write data to request body
	    req.write(postData);
	    console.log(postData);
	    console.log(loginReq);
	    console.log(req);
	    req.end();
	});
    });
});
