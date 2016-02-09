#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
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

var mailSubject = "Subject";
var mailMessage = "Dear $RecipientName$,\n\nThanks for agreeing to review Workshop Track submissions for ICLR 2016. We are happy to report that we will be managing the Workshop Track review process through OpenReview.net:\n\nhttp://beta.openreview.net/group?id=ICLR.cc/2016/workshop\n\nThe time table for the workshop track will be as follows:\n\n   18 February 2016 - Submission deadline\n   26 February 2016 - Review assignments are completed\n   10 March 2016 - Review submission deadline\n   28 March 2016 - Decisions sent to authors\n\nOur plan is to keep the reviewing load very low, to 1 or 2 extended abstracts (2-3 pages each). No author response period will be explicitly held beyond the open commenting feature that is supported by the reviewing platform.  However, as for the Conference Track, interaction with the authors is strongly encouraged.\n\nThank you for your help in putting together the ICLR technical program!\n\nHugo, Samy, and Brian - the ICLR 2016 program committee";

var revMail = {
    "groups": ["ICLR.cc/2016/workshop/reviewers"],
    "subject": mailSubject,
    "message": mailMessage
};

function make_post_req(url, o) {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var or3obj = new or3post(url, o, loggedInHdr(token));
	console.log(or3obj);
	request(or3obj, callback);
    }
  });
}

make_post_req(mailUrl, revMail);
