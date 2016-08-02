#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csv = require('csv');

// The open review local url
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var noteUrl = 'http://localhost:8529/_db/_system/openreview/notes';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
  'id': 'ari@host.com',
  'password': ''
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
	// I need to put myself first in the following because it will be passed to process
	'authors': ['ari@host.com', 'ICLR.cc/2016'],
	'writers': ['ICLR.cc/2016'],
	'readers': ['*'],
	'invitees': ['~'],
	//    cdate: 1/1/2016        // are these working yet?
	//    duedate: 2/3/2016
	//    ddate: 2/3/2016
	'reply': {
	    'forum': null,        // this will be set automatically
	    'parent': null,       // the response to this invite will be a forum root
	    'authors': '~.*',     // authors must reveal their ~ handle
	    'writers': '~.*',
	    'readers': '.*',
	    'content': {
		// ONLY HAVE THE TITLE FOR THE ICLR DATA RIGHT NOW
		'title': '.{1,100}'
//  	        'abstract': '.{1,2000}',
//	        'authors': '.*',
//	        'pdf': 'upload|http://arxiv.org/pdf/.*'   // either an actual pdf or an arxiv link
	    }
	},
	///////////////////////////////
	// THIS NEEDS TO BE FINISHED //
	//////////////////////////////
	'process': (function (firstAuthorToken, invite, note) {
	    var request = require('org/arangodb/request');
	    var noteID = note.id;

	    //////////////////////////////////
	    // ONLY FOR ICLR DATA FROM HUGO //
	    //////////////////////////////////
	    var subNum = note.submission_num;

	    // CREATE INVITATION TO COMMENT
	    var create_comment_invite = function(noteid, subNum) {
		return {
		    'id': 'ICLR.cc/2016/-/conf/paper/' + subNum + '/comment',
		    'forum': noteid,   // this links this invitation to the note (paper)
		    'parent': null,
		    'authors': ['ICLR.cc/2016'],
		    'writers': ['ICLR.cc/2016'],
		    'invitees': ['*'],
		    'readers': ['*'],
		    // UNIMPLEMETED
		    //     super: ICLR.cc/2016/-/workshop/comment
		    'reply': {
			'forum': noteid,  //  links this note to the previously posted note (paper)
			// 'parent': SHOULD THIS BE FILLED IN?
			'authors': '~.*',
			'writers': '~.*',
			'readers': '.*',
			'content': {
			    // THESE FIELDS ARE FOR HUGO'S DATA
			    'qualEval': '.{0,5000}',
			    'quantEval': '.{0,5000}',
			    'quantEvalNum': '.{0,5000}',
			    'confidence': '.{0,5000}',
			    'confidenceNum': '.{0,5000}',
			    'commentsToAC': '.{0,5000}'
//			    'title': '.{1,100}',
//			    'comment': '.{1,5000}'
			}
		    }
		};
	    };

	    var comment_invite = create_comment_invite(noteID, subNum);
	    var or3comment_invite = {
		'url': 'http://localhost:8529/_db/_system/openreview/invitations',
		'method': 'POST',
		'port': 8529,
		'json': true,
		'body': comment_invite,
		'headers': {
		    'Authorization': 'Bearer ' + firstAuthorToken
		}
	    };
	    var resp = request(or3comment_invite);
	    console.log("RESPONSE");
	    console.log(resp);
	    //   reply email receipt to reply.authors
	    //   create ICLR.cc/2016/workshop/paper/123/reviewers // to be filled in later
	    //   add note.authors to ICLR.cc/2016/workshop/authors
  	    return true;
	}) + ""
    };
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

function create_usr_no_pass(email) {
    return {
	'id': email,
	'needsPassword': true
    };
}

function create_iclr_sub_from_data(subNum, title) {
    return {
	'invitation': 'ICLR.cc/2016/-/conf/submission',
	'forum': null,        // this will be set automatically
	'parent': null,       // this will be the root of the forum
	'submission_num': subNum, // WE ONLY HAVE THIS IN THE DATA FROM HUGO
	'authors': ['~Ari_Kobren'],
	'writers': ['~Ari_Kobren'],
	'readers': ['*'],
	'content': {
	    'title': title
//	    'abstract': 'this is my abstract',
//	    'authors': 'Ari Kobren',
//	    'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'   // either an actual pdf or an arxiv link
	}
    };
}

function create_iclr_comment(inviteID, forumID, review) {
    return {
	'invitation': inviteID,
//	'forum': forumID,            // Am I supposed to have to set this field?
	'parent': null,              // Does this need to be the forum ID?
	'authors': ['~Ari_Kobren'],  // Hard Coded for Testing
	'writers': ['~Ari_Kobren'],  // Hard Coded for Testing
	'readers': ['*'],
	'content': {
	    'qualEval': review.qualEval,
	    'quantEval': review.quantEval,
	    'quantEvalNum': review.quantEvalNum,
	    'confidence': review.confidence,
	    'confidenceNum': review.confidenceNum,
	    'commentsToAC': review.commentsToAC
	}
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

///////////////////////////////////////////
// CREATE INITIAL ICLR SUBMISSION INVITE //
///////////////////////////////////////////
var init_invite = createIclrSubInv();
console.log("*******CREATE INIT SUBMISSION INVITE*******");
console.log(init_invite);
post_req(inviteUrl, init_invite);

var iclrData = fs.readFile('/Users/akobren/data/or3/iclr-workshop/reviewsForAndrew.csv', 'utf8', function (err, data) {
    if (err) throw err;
    csv.parse(data, function(err, data) {
	if (err) throw err;
	var prevSubNum = 0;
	var revNum;
	for (var i = 1; i<2; i++) {
	    var submission = parseLine(data[i]);
	    var subNum = submission.subNum;
	    if (prevSubNum == subNum) {
		revNum++;
	    } else {
		//////////////////////////////
		// CREATE SUBMISSION (NOTE) //
		//////////////////////////////
		prevSubNum = subNum;
		var iclr_sub = create_iclr_sub_from_data(subNum, submission.subName);
		console.log("*******CREATE PAPER NOTE*******");
		console.log(iclr_sub);
		post_req(noteUrl, iclr_sub);
		revNum = 1;
	    }
	    var email = submission.email;
	    ////////////////////////////////////////
	    // CREATE GROUP FOR USER IF NOT EXISTS//
	    ////////////////////////////////////////
	    var usr = create_usr_no_pass(email);
	    console.log("*******CREATE USER*******");
	    console.log(usr);
	    post_req(grpUrl, usr);

	    //////////////////////////////
	    // ASSIGN REVIEWER TO PAPER //
	    //////////////////////////////
	    var assn = assignReviewer(subNum, revNum, email);
	    console.log("*******ASSIGN REVIEWER*******");
	    console.log(assn);
	    post_req(grpUrl, assn);

	    //////////////////////////////
	    // SUBMIT REVIEWER COMMENT ///
	    //////////////////////////////
	    var forum_id = 'DUMMY';
	    var invite_id = 'ICLR.cc/2016/-/conf/paper/' + prevSubNum + '/comment';
	    var comment = create_iclr_comment(invite_id, forum_id, submission);
	    console.log('***********COMMENT*************');
	    console.log(comment);
	    post_req(noteUrl, comment);
	}
	return data;
    });
});
