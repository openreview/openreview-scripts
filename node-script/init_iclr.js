#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csv = require('csv');

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
  'User-Agent': 'test-create-script'
  };
}

function iclrPc(usr) {
    return {
	'id': 'ICLR.cc/2016',
	'authors': [usr],
	'writers': [usr],
	'members': [usr],
	'signatories': ['ICLR.cc/2016'],
	'readers': ['ICLR.cc/2016']
    };
}


//////////////////////////////
// THIS NEEDS TO BE FINISHED//
//////////////////////////////
function createGrpForUser(email, org, first, last) {
    return {
	'id': email
    };
}

function createIclrSubInv() {
    return  {
	'id': 'ICLR.cc/2016/-/conf/submission',
	'authors': ['ICLR.cc/2016'],
	'writers': ['ICLR.cc/2016'],
	'readers': ['*'],
	'invitees': ['~'],
//    cdate: 1/1/2016        // are these working yet?
//    duedate: 2/3/2016
//    ddate: 2/3/2016

    ///////////////////////////////
    // THIS NEEDS TO BE FINISHED //
    //////////////////////////////
	'process': function (noteID) {
	    var subNum = 1;
	    var forum = noteID;
	    var comment_invite = create_comment_invite(forum, subNum);
	    post_req(inviteUrl, comment_invite);
	    // NN = a paper # (by finding the max of ICLR.cc/2016/-/workshop/paper/*/comment)
	    //   reply email receipt to reply.authors
	    //   create ICLR.cc/2016/workshop/paper/123/reviewers // to be filled in later
	    //   add note.authors to ICLR.cc/2016/workshop/authors
	    //   # allow anyone to comment
	    //   create comment invitation:
  	    //send email to paper’s authors’ and reviewers’ email addresses
  	    return true;
	},
	'reply': {
	    'forum': null,        // this will be set automatically
	    'parent': null,       // the response to this invite will be a forum root
	    'authors': '~.*',     // authors must reveal their ~ handle
	    'writers': '~.*',
	    'readers': '.*',
	    'content': {
		'title': '.{1,100}'
//	    'abstract': '.{1,2000}',
//	    'authors': '.*',
//	    'pdf': 'upload|http://arxiv.org/pdf/.*'   // either an actual pdf or an arxiv link
	    }
	}
    };
};

//////////////////////////////
// THIS NEEDS TO BE CHECKED //
//////////////////////////////
function create_comment_invite(forumID, subNum) {
    var comment_invite = {
	'id': 'ICLR.cc/2016/-/workshop/paper/' + subNum + '/comment',
	'forum': forumID,
	'parent': null,
	'author': ['ICLR.cc/2016'],
	'readers': ['*'],
	//     super: ICLR.cc/2016/-/workshop/comment
	'reply': {
	    'forum': forumID,
	    'authors': ['~.*'],
	    'writers': ['~.*'],
	    'readers': ['*'],
	    'content': {
		'title': '.{1,100}',
		'comment': '.{1,5000}'
	    }
	}
    };
    return comment_invite;
};

function assignReviewer(papNum, revNum, rev) {
    return {
	'id': 'ICLR.cc/2016/paper/' + papNum + '/reviewer/' + revNum,
	'authors': ['ICLR.cc/2016'],
	'writers': ['ICLR.cc/2016'],
	'members': [rev],
	'signatories': ['ICLR.cc/2016/-/conf/paper/' + papNum + '/reviewer/' + revNum],
	'readers': ['ICLR.cc/2016']
	//this.nonreaders = ICLR.cc/2016/belanger/conflicts
    };
}

function parseLine(line) {
    return {
	'subNum': line[0],
	'subName': line[1],
	'lastUpdate': line[2],
	'firstName': line[3],
	'lastName': line[4],
	'email': line[5],
	'org': line[6],
	'rank': line[7],
	'rankComment': line[8],
	'qualEval': line[9],
	'quantEval': line[10],
	'quantEvalNum': line[11],
	'confidence': line[12],
	'confidenceNum': line[13],
	'commentsToAC': line[14]
    };
}

function post_req(url, o) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
	if (!error && response.statusCode == 200) {
            var token = body.token;
	    var or3obj = new or3post(url, o, loggedInHdr(token));
	    request(or3obj, callback);
	}
    });
}

//post_req(grpUrl, iclrPc('ari@host.com'));

var iclrData = fs.readFile('/Users/akobren/data/or3/iclr-workshop/reviewsForAndrew.csv', 'utf8', function (err, data) {
    if (err) throw err;
    csv.parse(data, function(err, data) {
	if (err) throw err;

	var prevSubNum = 0;
	var revNum;
	for (var i = 1; i<10; i++) {
	    var submission = parseLine(data[i]);
	    var subNum = submission.subNum;
	    if (prevSubNum == subNum) {
		revNum++;
	    } else {
		revNum = 1;
	    }
	    var email = submission.email;
	    var assignment = assignReviewer(subNum, revNum, email);
	    console.log(assignment);
	}
	return data;
    });
});
