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
    'id': 'ICLR.cc/2016/-/workshop2/submission',
    //    'authors': 'ICLR.cc/2016',
    'authors': ['ari@host.com'],
    'writers': ['ICLR.cc/2016'],
    'readers': ['*'],
    'invitees': ['~'],
//    cdate: 1/1/2016        // are these working yet?
//    duedate: 2/3/2016
//    ddate: 2/3/2016
    'process': function (noteID) {
	var subNum = 1;
	var forum = noteID;
	var comment_invite = create_comment_invite(forum, subNum);
	console.log('FORUM:' + forum);
	console.log('COMMENT_INVITE')
	console.log(comment_invite);
	create_submission_invite(inviteUrl, comment_invite);
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
	    'title': '.{1,100}',
	    'abstract': '.{1,2000}',
	    'authors': '.*',
	    'pdf': 'upload|http://arxiv.org/pdf/.*'   // either an actual pdf or an arxiv link
	}
    }
};

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

// ICLR COMMENT PROTOTYPE - CURRENTLY UNUSED
function iclr_comment() {
    this.id = 'ICLR.cc/2016/-/workshop/comment';
    this.authors = ['ICLR.cc/2016'];
    this.writers = ['ICLR.cc/2016'];
    this.readers = ['*'];
    //cdate:
    //rdate:
    this.reply = {
	//parent: null
	'authors': ['~.*'],
	'writers': ['~.*'],
	'readers': ['*'],
	'content': {
	    'title': '.{1,100}',
	    'comment': '.{1,5000}'
	}
    };
    this.process = function (noteID) {
	//send email to paper’s authors’ and reviewers’ email addresses
	return true;
    };
}

function create_submission_invite(url, o) {
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

create_submission_invite(inviteUrl, subInv);
