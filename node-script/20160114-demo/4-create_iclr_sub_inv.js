#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';

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

// ICLR SUBMISSION INVITE
var subInv = {
    'id': 'ICLR.cc/2016/-/workshop/submission',
    'authors': [rootUsr.id],
    'writers': ['ICLR.cc/2016'],
    'readers': ['*'],
    'invitees': ['~'],
    'reply': {
	'forum': null,        // this will be set automatically
	'parent': null,       // the response to this invite will be a forum root
	'authors': '~.*',     // authors must reveal their ~ handle
	'writers': '~.*',     // the writers must also reveal their ~ handle
	'readers': '\\*,',
	'content': {
	    'title': '.{1,100}',
	    'abstract': '.{1,2000}',
	    'authors': '(.*,)+',
	    'conflicts': '(.*;)+',
	    'resubmit': 'Yes|No',
//	    'cmtID': '.*',                            // if this is a resubmit, specify the CMT ID
	    'pdf': 'upload|http://arxiv.org/pdf/.+'   // either an actual pdf or an arxiv link
	}
    },
    'process': (function (token, invitation, note, count, lib) {
	var request = require('org/arangodb/request');             // this is messy; on the server I can only use arango's request library
	// TODO AK: should we move away from using the node.js request library in favor of arango only?

	var noteID = note.id;
	var forum = note.forum;
	// CREATE INVITATION TO COMMENT
	var create_comment_invite = function(noteID, forum, count) {
	    return {
		'id': 'ICLR.cc/2016/-/workshop/paper/' + count + '/comment',
		'authors': [rootUsr.id],
		'writers': ['ICLR.cc/2016'],
		'invitees': ['~'],              // this indicates the ~ group
		'readers': ['*'],               // this indicates the * group

		//     super: ICLR.cc/2016/-/workshop/comment
		// TODO AK: eventually we want to create a superclass of comment but for now this is OK

		'reply': {
		    'forum': forum,      // links this note (comment) to the previously posted note (paper)
//		    'parent': noteID,    // not specified so we can allow comments on comments
		    'authors': '~.*',    // this regex demands that the author reveal his/her ~ handle
		    'writers': '~.*',    // this regex demands that the author reveal his/her ~ handle
		    'readers': '\\*,',   // the reply must allow ANYONE (i.e., the * group) to read this note (comment)
		    'content': {
			'title': '.{0,500}',
			'comment': '.{1,5000}'
//			'quantEval': '0|1|2|3|4|5|6|7|8|9',
//			'confidence': '1|2|3|4|5'
		    },
		    'process': (function (token, invitation, note, count, lib) {
			// SEND EMAIL TO AUTHORS THAT THEIR PAPER RECIEVED A COMMENT
			return true;
		    }) + ""
		}
	    };
	};

	var comment_invite = create_comment_invite(noteID, forum, count);
	var or3comment_invite = {
	    'url': 'http://localhost:8529/_db/_system/openreview/invitations',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': comment_invite,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	console.log("OR3 COMMENT INVITE");
	console.log(or3comment_invite);

	var resp = request(or3comment_invite);
	console.log("RESPONSE");
	console.log(resp);
	console.log(resp.statusCode);

	// CREATE REVIEWER GROUPS
	var paper_grp = {
	    'id': 'ICLR.cc/2016/workshop/paper/' + count,
	    'authors': [rootUsr.id],
	    'writers': ['ICLR.cc/2016'],
	    'readers': ['*'],
	    'members': ['ICLR.cc/2016'],
	    'signatories': []
	};

	var rev_grp = {
	    'id': 'ICLR.cc/2016/workshop/paper/' + count + '/reviewer',
	    'authors': [rootUsr.id],
	    'writers': ['ICLR.cc/2016'],
	    'readers': ['*'],
	    'members': ['ICLR.cc/2016'],
	    'signatories': []
	};

	var or3paper_grp = {
	    'url': 'http://localhost:8529/_db/_system/openreview/groups',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': paper_grp,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	var or3rev_grp = {
	    'url': 'http://localhost:8529/_db/_system/openreview/groups',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': rev_grp,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	var request_with_callback = function (o, callback) {
	    resp = request(o);
	    console.log('GROUP');
	    console.log(resp);
	    callback();
	};

	request_with_callback(or3paper_grp, function () {
	    resp = request(or3rev_grp);
	    console.log('SECOND GROUP');
	    console.log(resp);
	});

	var rev_inv_1 = {
	    'id': 'ICLR.cc/2016/-/workshop/paper/' + count + '/reviewer/1',
	    'authors': [rootUsr],
	    'writers': ['ICLR.cc/2016'],
	    'readers': ['ICLR.cc/2016', 'ICLR.cc/2016/workshop/paper/' + count + '/reviewer/1'],
	    'invitees': ['ICLR.cc/2016/workshop/paper/' + count + '/reviewer/1'],
	    'reply': {
		'forum': noteID,
		'parent': noteID,
		'authors': '~.*|ICLR.cc/2016/workshop/paper/' + count + '/reviewer/1',  // author reveals their ~ handle or remains anonymous
		// This reviewer has not been assigned yet
		'writers': '~.*',
		'readers': '\\*,',     // review must be world readable
		'content': {
		    'qualEval': '.{1,5000}',
		    'quantEval': '0|1|2|3|4|5|6|7|8|9',
		    'confidence': '1|2|3|4|5'
		}
	    }
	};

	var or3rev_inv_1 = {
	    'url': 'http://localhost:8529/_db/_system/openreview/invitations',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': rev_inv_1,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	resp = request(or3rev_inv_1);
	console.log("RESPONSE");
	console.log(resp);

	//   reply email receipt to reply.authors
	//   create ICLR.cc/2016/workshop/paper/123/reviewers // to be filled in later
	//   add note.authors to ICLR.cc/2016/workshop/authors
	//   # allow anyone to comment
	//   create comment invitation:
  	//send email to paper’s authors’ and reviewers’ email addresses
  	return true;
    }) + ""
};

function create_iclr_paper_submission_invite(url, o) {
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

create_iclr_paper_submission_invite(inviteUrl, subInv);
