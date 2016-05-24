#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var or3lib = require('../../../or3/or3lib');


// The open review local url
var grpUrl = 'http://localhost:3000/groups';
var loginUrl = 'http://localhost:3000/login';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var rootUsr = {
  'id': 'OpenReview.net',
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
  'User-Agent': 'test-create-script',
  };
}

// GROUPS TO CREATE
var workshop = {
    'id': 'ICLR.cc/2016/workshop',
    'signatures': [rootUsr.id],
    'writers': ['ICLR.cc/2016'],
    'readers': ['everyone'],
    'members': ['ICLR.cc/2016'],
    'signatories': ['ICLR.cc/2016'],
    'web': fs.readFileSync('web-field-workshop.html', "utf8")
};

var conference = {
    'id': 'ICLR.cc/2016/conference',
    'signatures': [rootUsr.id],
    'writers': ['ICLR.cc/2016'],
    'readers': ['everyone'],
    'members': ['ICLR.cc/2016'],
    'signatories': ['ICLR.cc/2016']
};

var paper = {
    'id': 'ICLR.cc/2016/workshop/paper',
    'signatures': [rootUsr.id],
    'writers': [workshop.id],
    'readers': ['everyone'],
    'members': [workshop.id],
    'signatories': []
};

function create_groups() {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
          var token = body.token;
	  var or3workshopGrp = new or3post(grpUrl, workshop, loggedInHdr(token));
	  request(or3workshopGrp, function(error, response, body) {
	      var or3paperGrp = new or3post(grpUrl, paper, loggedInHdr(token));
	      request(or3paperGrp, function(error, response, body) {
		  var or3conferenceGrp = new or3post(grpUrl, conference, loggedInHdr(token));
		  request(or3conferenceGrp, callback);
	      });
	  });
      }
    });
}

create_groups();

//add workshop to host group:
or3lib.getRootTokenP().then(token => or3lib.addHostMember("ICLR.cc/2016/workshop", token))


