#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var mailUrl = 'http://localhost:8529/_db/_system/openreview/mail';
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var rootUsr = {
  'id': 'OpenReview.net',
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

function make_post_req(url, o) {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var or3obj = new or3post(url, o, loggedInHdr(token));
	console.log(or3obj);
	request(or3obj, callback);
    }
  });
}

// REVIEWER GROUP
var revGrp = {
    'id': 'ICLR.cc/2016/workshop/reviewers',
    'signatures': [rootUsr.id],
    'writers': ['ICLR.cc/2016'],
    'readers': ['ICLR.cc/2016'],
    'members': [],
    'signatories': ['ICLR.cc/2016']
};

function main(){
    var reviewerFile = process.argv[2];
    var parser = csvparse({delimiter: ','});

    // Use the writable stream api
    parser.on('readable', function(){
	while(record = parser.read()) {
	    revGrp.members.push(record[3]);
	};
    });

    // When finished with file create group
    parser.on('finish', function(){
	make_post_req(grpUrl, revGrp);
    });

    // Catch any error
    parser.on('error', function(err){
	console.log(err);
    });

    fs.readFile(reviewerFile, function(err, data) {
	parser.write(data);
	parser.end();
    });
}
main();
