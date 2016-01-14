#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var noteUrl = 'http://localhost:8529/_db/_system/openreview/notes';

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

// ICLR SUBMISSION
var sub = {
    'invitation': 'ICLR.cc/2016/-/workshop/submission',
    'forum': null,
    'parent': null,
    'authors': ['~Ari_Kobren'],
    'writers': ['~Ari_Kobren'],
    'readers': ['*'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'My Title',
	    'abstract': 'My Abstract',
	    'authors': 'Ari Kobren,',
	    'conflicts': 'umass.edu;',
	    'resubmit': 'Yes',
	    'cmtID': '98',
	    'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

// ICLR REVIEWER INVITATION
var review_inv = function (rev, subNum, revNum, paperID) {
    return {
	'id': 'ICLR.cc/2016/-/workshop/paper/' + subNum + '/reviewer/' + revNum,
	'authors': ['ICLR.cc/2016'],
	'writers': ['ICLR.cc/2016'],
	'readers': ['ICLR.cc/2016', rev],
	'invitees': [rev],
	'reply': {
	    'forum': paperID,
	    'parent': paperID,
	    'authors': '~.*|ICLR.cc/2016/paper/' + subNum + '/reviewer/' + revNum,
	    'writers': '~.*',
	    'readers': '\\*',     // must be world readable
	    'content': {
		'qualEval': '.{1,5000}',
		'quantEval': '1|2|3|4|5|6|7|8|9|10',
		'confidence': '1|2|3|4|5'
	    }
	}
    };
};

function submit_and_assign_reviewer(sub, rev, subNum, revNum) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
          var token = body.token;
	  var or3submission = new or3post(noteUrl, sub, loggedInHdr(token));
	  request(or3submission, function(error, response, body) {
	      if (!error && response.statusCode == 200) {
		  var paperID = body.id;
		  var rev_inv = review_inv(rev, subNum, revNum, paperID);
		  var or3assignment = new or3post(inviteUrl, rev_inv, loggedInHdr(token));
		  request(or3assignment, callback);
	      }
	  });
      }
    });
}

submit_and_assign_reviewer(sub, 'u2@host.com', 1, 1);
