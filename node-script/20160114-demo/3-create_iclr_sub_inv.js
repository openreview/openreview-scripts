#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
  'id': 'ari@host.com',
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
    'id': 'ICLR.cc/2016/-/workshop/submission2',
    // I need to put myself first in the following because it will be passed to process
    'authors': ['ICLR.cc/2016'],
    'writers': ['ICLR.cc/2016'],
    'readers': ['*'],
    'invitees': ['~'],
    'reply': {
	'forum': null,        // this will be set automatically
	'parent': null,       // the response to this invite will be a forum root
	'authors': '~.*',     // authors must reveal their ~ handle
	'writers': '~.*',
	'readers': '.*',
	'content': {
	    'title': '.{1,100}',
	    'abstract': '.{1,2000}',
	    'authors': '(.*,)+',
	    'conflicts': '(.*;)+',
	    'resubmit': 'Yes|No',
	    'cmtID': '.*',                            // if this is a resubmit, specify the CMT ID
	    'pdf': 'upload|http://arxiv.org/pdf/.+'   // either an actual pdf or an arxiv link
	}
    },
    'process': (function (token, invitation, note, count, lib) {
	console.log('HERE');
	var request = require('org/arangodb/request');
	var noteID = note.id;
	var forum = note.forum;
	// CREATE INVITATION TO COMMENT
	var create_comment_invite = function(noteID, forum, count) {
	    return {
		'id': 'ICLR.cc/2016/-/workshop/paper/' + count + '/comment',
		'authors': ['ICLR.cc/2016'],
		'writers': ['ICLR.cc/2016'],
		'invitees': ['~'],
		'readers': ['*'],
		//     super: ICLR.cc/2016/-/workshop/comment
		'reply': {
		    'forum': forum,  // links this note to the previously posted note (paper)
		    'parent': noteID,
		    'authors': '~.*',
		    'writers': '~.*',
		    'readers': '\\*',
		    'content': {
			'qualEval': '.{1,5000}',
			'quantEval': '1|2|3|4|5|6|7|8|9|10',
			'confidence': '1|2|3|4|5'
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
	// NN = a paper # (by finding the max of ICLR.cc/2016/-/workshop/paper/*/comment)
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

create_iclr_paper_submission_invite(inviteUrl, subInv);
