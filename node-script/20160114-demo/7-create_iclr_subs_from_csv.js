#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
//var xml2js = require('xml2js')
var csvparse = require('csv-parse')

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var noteUrl = 'http://localhost:8529/_db/_system/openreview/notes';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
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

// ICLR SUBMISSION
var sub = {
    'invitation': 'ICLR.cc/2016/-/workshop/submission',
    'forum': null,
    'parent': null,
    'authors': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1'],
    'readers': ['*'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'My Title',
	'abstract': 'My Abstract',
	'authors': 'Ari Kobren',
	'conflicts': 'umass.edu',
	'resubmit': 'Yes',
	'cmtID': '98',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

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

function process_record(record) {
	var sub = {
    'invitation': 'ICLR.cc/2016/-/workshop/submission',
    'forum': null,
    'parent': null,
    'authors': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1'],
    'readers': ['*'],
    'pdfTransfer': 'url',
    'content': {
	'title': record[1],
	'abstract': record[2],
	'authors': record[3],
	'conflicts': record[4],
	'resubmit': 'Yes',
	'cmtID': '98',
	'pdf': record[9]
    }
	}
	//console.log(sub);
	make_post_req(noteUrl, sub);
};
	

var submissionFilepath = "/Users/csgreenberg/workspace/data/iesl/openreview/iclr_submissions.txt"
var output = [];
// Create the parser
//var parser = csvparse({delimiter: ':'});
var parser = csvparse({delimiter: '\t'});
// Use the writable stream api
parser.on('readable', function(){
	while(record = parser.read()){
		//output.push(record);
		process_record(record);
	}
});
// Catch any error
parser.on('error', function(err){
	console.log(err.message);
});
// When we are done, test that the parsed output matched what expected
parser.on('finish', function(){
	console.log('finished')
	/*
	output.should.eql([
		[ 'root','x', '0','0','root','/root','/bin/bash' ],
		[ 'someone','x','1022','1022','a funny cat','/home/someone','/bin/bash' ]
	]);
*/
});
// Now that setup is done, write data to the stream
fs.readFile(submissionFilepath, function(err, data) {
	parser.write(data);
	/*
	parser.parseString(data, function (err, result) {
		console.log(result);
		console.log('Done');
	});
	*/
	parser.end();
});

//parser.write("root:x:0:0:root:/root:/bin/bash\n");
//parser.write("someone:x:1022:1022:a funny cat:/home/someone:/bin/bash\n");
// Close the readable stream
//parser.end();
		  
/*
var submissionFilepath = "/Users/csgreenberg/workspace/data/iesl/openreview/iclr_submissions.xml"
var parser = new xml2js.Parser();
fs.readFile(submissionFilepath, function(err, data) {
	parser.parseString(data, function (err, result) {
		console.log(result);
		console.log('Done');
	});
});
*/

/*
var parseString = xml2js.parseString;
parseString(txt, function (err, result) {
	console.log(result);
});
*/



//make_post_req(noteUrl, sub);
