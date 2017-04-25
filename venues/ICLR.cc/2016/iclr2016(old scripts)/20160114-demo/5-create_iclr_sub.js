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
  'id': 'a@host.com',
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

// ICLR SUBMISSION
var sub = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'SHOULD SUCCEED 1',
	'abstract': 'The abstract of test paper 1',
	'authors': 'Ari Kobren',
	'author_emails': 'ari@host.com',
	'conflicts': 'umass.edu',
	'CMT_id': '',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

var sub2 = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1','~Ari_Kobren2'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'SHOULD SUCCEED 2',
	'abstract': 'The paper has two authors',
	'authors': 'Ari Kobren, Ari Kobren 2',
	'author_emails': 'ari@host.com,a@host.com',
	'conflicts': 'umass.edu;google.com',
	'CMT_id': '',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

var sub3 = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1','~Ari_Kobren2'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'SHOULD FAIL 1',
	'abstract': 'The paper has two authors',
	'authors': 'Ari Kobren, Ari Kobren 2',
	'author_emails': 'ari@host.com,a@host.com',
	'conflicts': ',',
	'CMT_id': '',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

var sub4 = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1','~Ari_Kobren2'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'SHOULD FAIL 2',
	'abstract': 'The paper has two authors',
	'authors': 'Ari Kobren, Ari Kobren 2',
	'author_emails': 'ari@host.com,a@host.com',
	'conflicts': 'aksjdkflja',
	'CMT_id': '',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

var sub5 = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1','~Ari_Kobren2'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'SHOULD FAIL 3',
	'abstract': 'The paper has two authors',
	'authors': 'Ari Kobren, Ari Kobren 2',
	'author_emails': 'ari@host.com,a@host.com',
	'conflicts': 'kasjdflkas;askjdflkajs.edu',
	'CMT_id': '',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

var sub6 = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1','~Ari_Kobren2'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'SHOULD SUCCEED 3',
	'abstract': 'The paper has two authors',
	'authors': 'Ari Kobren, Ari Kobren 2',
	'author_emails': 'ari@host.com,a@host.com',
	'conflicts': 'iitk.ac.in;toronto.edu;cs.toronto.edu;utoronto.ca;cornell.edu;cs.cornell.edu;umontreal.ca',
	'CMT_id': '',
	'pdf': 'http://arxiv.org/pdf/1506.03425v1.pdf'
    }
};

var sub7 = {
    'invitation': 'ICLR.cc/2016/workshop/-/submission',
    'forum': null,
    'parent': null,
    'signatures': ['~Ari_Kobren1'],
    'writers': ['~Ari_Kobren1','~Ari_Kobren2'],
    'readers': ['everyone'],
    'pdfTransfer': 'url',
    'content': {
	'title': 'SHOULD SUCCEED 4',
	'abstract': 'The paper has two authors',
	'authors': 'Ari Kobren, Ari Kobren 2',
	'author_emails': 'ari@host.com,a@host.com',
	'conflicts': 'microsoft.com;huawei.com;ict.ac.cn',
	'CMT_id': '',
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

make_post_req(noteUrl, sub);
make_post_req(noteUrl, sub2);
make_post_req(noteUrl, sub3);
make_post_req(noteUrl, sub4);
make_post_req(noteUrl, sub5);
make_post_req(noteUrl, sub6);
make_post_req(noteUrl, sub7);
