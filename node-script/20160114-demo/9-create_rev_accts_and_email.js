#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var noteUrl = 'http://localhost:8529/_db/_system/openreview/notes';
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var mailUrl = 'http://localhost:8529/_db/_system/openreview/mail';

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

function loggedInHdr(token) {
  return {
  'Authorization': 'Bearer ' + token,
  'User-Agent': 'test-create-script'
  };
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

var mailSubject = "Welcome to ICLR 2016 Workshop Track reviewers";
function mailMessage(first, last) {
    return "Dear " + first + " " + last + ",\n\nThanks for agreeing to review Workshop Track submissions for ICLR 2016. We are happy to report that we will be managing the Workshop Track review process through OpenReview.net:\n\nhttp://beta.openreview.net/group?id=ICLR.cc/2016/workshop\n\nThe time table for the workshop track will be as follows:\n\n   18 February 2016 - Submission deadline\n   26 February 2016 - Review assignments are completed\n   10 March 2016 - Review submission deadline\n   28 March 2016 - Decisions sent to authors\n\nOur plan is to keep the reviewing load very low, to 1 or 2 extended abstracts (2-3 pages each). No author response period will be explicitly held beyond the open commenting feature that is supported by the reviewing platform.  However, as for the Conference Track, interaction with the authors is strongly encouraged.\n\nThank you for your help in putting together the ICLR technical program!\n\nHugo, Samy, and Brian - the ICLR 2016 program committee";
};


function revMail(first, last, revEmail) {
	return {
	    "groups": [revEmail],
	    "subject": mailSubject,
	    "message": mailMessage(first, last)
	};
};

//FirstName,LastName,Organization,ContactEMail,TPMSEMail
function revFromRecord(record) {
    return { 'first': record[0],
	     'last': record[1],
	     'email': record[3]
	   };
};

function createGrpAndEmail(token, reader, cb) {
    var record = reader.read();
    if (record) {
	var rev = revFromRecord(record);
	var usrGrp = new or3post(grpUrl, { 'id': rev.email, 'needsPassword': true }, loggedInHdr(token));
	var email = new or3post(mailUrl, revMail(rev.first, rev.last, rev.email), loggedInHdr(token));
	request(usrGrp, function() {
	    console.log("I'm Mailing " + rev.email);
	    console.log(email);
	    request(email, cb);
	});
    }
};

function emailAll(url, reader) {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
	if (!error && response.statusCode == 200) {
            var token = body.token;
	    var emailNextCallback = function(error, response, body){
		console.log("holler back");
		createGrpAndEmail(token, reader, emailNextCallback);
	    };
	    createGrpAndEmail(token, reader, emailNextCallback);
	}
    });
}

function main(){
    var reviewerFile = process.argv[2];
    var parser = csvparse({delimiter: ','});

    // Use the writable stream api
    parser.on('readable', function(){
	emailAll(mailUrl, parser);
    });

    // When finished with file create group and send mail
//    parser.on('finish', function(){
//	make_post_req(grpUrl, revGrp);
//    });

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
