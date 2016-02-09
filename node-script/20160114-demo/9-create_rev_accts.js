#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var noteUrl = 'http://localhost:8529/_db/_system/openreview/notes';
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var rootUsr = {
  'id': 'OpenReview.net',
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

function make_post_req(url, o) {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var commentInvite = new or3post(url, o, loggedInHdr(token));
	console.log(commentInvite);
	request(commentInvite, callback);
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

//FirstName,LastName,Organization,ContactEMail,TPMSEMail
function parseLine(line) {
    return { 'id': line[3],
	     'needsPassword': true
	   };
}

function main(){
    var reviewerFile = process.argv[2];
    var parser = csvparse({delimiter: ','});
    // Use the writable stream api
    parser.on('readable', function(){
	while(record = parser.read()){
	    var usrGrp = parseLine(record);
	    revGrp.members.push(usrGrp.id);
	    make_post_req(grpUrl, usrGrp);
	}
    });
    // Catch any error
    parser.on('error', function(err){
	console.log(err);
    });
    // When finished with file create group and send mail
    parser.on('finish', function(){
	make_post_req(grpUrl, revGrp);
    });

    fs.readFile(reviewerFile, function(err, data) {
	parser.write(data);
	parser.end();
    });
}


main();
