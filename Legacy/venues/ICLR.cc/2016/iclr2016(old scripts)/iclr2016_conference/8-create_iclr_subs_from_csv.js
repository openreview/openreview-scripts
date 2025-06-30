#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse')

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var noteUrl = 'http://localhost:8529/_db/_system/openreview/notes';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
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

function make_post_req(url, o) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var commentInvite = new or3post(url, o, loggedInHdr(token));
	console.log(commentInvite);
	request(commentInvite, callback);
    }
  });
}

//make_post_req(noteUrl, sub);


function process_record(record) {	
var sub = {
    'invitation': 'ICLR.cc/2016/conference/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
		//'title': 'Test Paper 1',
		'title': record[1],
		'abstract': record[2],
		'authors': record[3],
		'conflicts': record[4],
		'CMT_id': '',
		'pdf': record[9]
    }
};

	//console.log(sub);
	make_post_req(noteUrl, sub);
};
	
function main(){
	// get tsv filepath with iclr submissions from stdin
	//var submissionFilepath = "/Users/csgreenberg/workspace/data/iesl/openreview/iclr_submissions.txt"
	var submissionFilepath = process.argv[2];
	// Create the parser
	var parser = csvparse({delimiter: '\t'});
	// Use the writable stream api
	parser.on('readable', function(){
		while(record = parser.read()){
			process_record(record);
		}
	});
	// Catch any error
	parser.on('error', function(err){
		console.log(err.message);
	});
	
	fs.readFile(submissionFilepath, function(err, data) {
		parser.write(data);
		parser.end();
	});
}

main()
