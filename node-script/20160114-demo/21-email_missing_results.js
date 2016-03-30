#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');
var stringify = require('csv-stringify');
var _ = require('lodash');
var p = require('node-promise');

var urlPrefix = 'http://localhost:8529/_db/_system/openreview/'; 

var tokenP = function() {
  var df = p.defer();
  request(
    {
      method: 'POST',
      url: urlPrefix + 'login', 
      json: true, 
      body: {
        'id': 'OpenReview.net', 'password': '12345678'
      }
    },
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token; 
        df.resolve(token);
      }
    }
  );
  return df.promise;
}();

p.when(tokenP, function(token) {

  var papersP = function() {
    var df = p.defer();
    request(
      {
        method: 'GET',
        url: urlPrefix + 'notes?invitation=ICLR.cc/2016/workshop/-/submission', 
        json: true,
        headers: {
            'Authorization': 'Bearer ' + token
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          df.resolve(body.notes);
        } else {
          df.resolve([]);
        }
      }
    );
    return df.promise;
  }();

  var sendAccept = function(email, name, title) {
    console.log("sendAccept: " + email + ", " + name + ", " + title);
    var subject = "ICLR 2016 workshop track decision - Accepted";
    var message = ( 
      "Dear " + name + ",\n\n"  
      + "We are pleased to inform you that your ICLR 2016 workshop track submission\n"
      + "*" + title + "*\n"
      + "has been accepted to the workshop track as a poster presentation.\n\n"
      + "Please make your travel arrangements ASAP. Hotel rates and ICLR early registration are only in effect until April 1, 2016. You can register and reserve your hotel room from the conference website: http://www.iclr.cc/doku.php?id=start\n\n"
      + "At least one author for each paper must be registered for ICLR 2016 by April 10th.\n\n"
      + "We will post guidelines for the poster presentations to the conference web site, so be on the lookout for those.\n\n"
      + "We look forward to seeing you in San Juan!\n\n"
      + "Hugo, Samy, and Brian -- the ICLR 2016 program committee"
    );
    request(
      {
        'method': 'POST',
        'url': urlPrefix + 'mail', 
        'json': true,
        'body': {
          'groups' : [email], 
          'subject': subject,
          'message': message 
        },
        'headers': {
          'Authorization': 'Bearer ' + token 
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          console.log("accept sent : " + JSON.stringify(body));
          console.log("paper: " + title);
          console.log("");
        }
      }
    );
  };

  var sendReject = function(email, name, title) {
    console.log("sendReject: " + email + ", " + name + ", " + title);
    var subject = "ICLR 2016 workshop track decision - Rejected";
    var message = ( 
      "Dear " + name + ",\n\n"
      + "We are writing to inform you that your ICLR 2016 workshop track submission\n"
      + "*" + title + "*\n"
      + "was not accepted.\n\n"
      + "Thank you for your interest in the conference, and we hope you'll nevertheless consider joining us in Puerto Rico.\n\n"
      + "Brian, Hugo, Samy -- the ICLR 2016 program committee"
    );
    request(
      {
        'method': 'POST',
        'url': urlPrefix + 'mail', 
        'json': true,
        'body': {
          'groups' : [email], 
          'subject': subject,
          'message': message 
        },
        'headers': {
          'Authorization': 'Bearer ' + token 
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          console.log("reject sent: " + JSON.stringify(body));
          console.log("paper: " + title);
          console.log("");
        }
      }
    );
  };

  var noteId2Result = {
    "XL9vKJ98DCXB8D1RUGV0": "Accept", 
    "91EowxONgIkRlNvXUVog": "Accept",
    "ZY9x1mJ3zS5Pk8ELfEjD": "Accept",
    "ANYzpXg3LcNrwlgXCq9G": "Accept",
    "xnrAg7jmLF1m7RyVi3vG": "Accept",
    "xnrA4qzmPu1m7RyVi38Z": "Accept",
    "oVgo1jRRDsrlgPMRsBzY": "Reject",
    "VAVqG11WmSx0Wk76TAzp": "Accept",
    "3QxgDBPQxIp7y9wltPq9": "Reject",
    "Qn8lE8x17fkB2l8pUYPk": "Accept",
    "BNYAA7gNBi7PwR1riXzR": "Accept",
    "XL92M93mzhXB8D1RUWBz": "Accept",
    "L7VOzGWB5hRNGwArs4BJ": "Accept",
    "jZ9WrEWPmsnlBG2XfGLl": "Accept"
  };

  p.when(p.all(papersP), function(all) {
    var papers = _.filter(_.sortBy(all[0], function(p) {
      return !p.content.CMT_id;
    }), function(p) {
      return noteId2Result[p.id];
    });


    _.forEach(papers, function(paper) {
      var title = paper.content.title;
      var authorList = _.map(paper.content.authors.split(","), function(s) {
        return s.trim();
      });
      var authorEmailList = _.map(paper.content.author_emails.split(","), function(s) {
        return s.trim();
      });
      var nameEmailPairs = function() {
        if (authorEmailList.length > 0) {
          return _.map(_.zip(authorList, authorEmailList), function(p) {
            return {name: p[0], email: p[1]};
          });
        } else {
          console.log("No Emails: " + paper.id);
          return [[]];
        }
      }();


      var result = noteId2Result[paper.id];

      if (result == "Accept") {
        _.forEach(nameEmailPairs, function(p) { if (p.email && p.name) {
          sendAccept(p.email, p.name, title);
        }});
      } else if (result == "Reject") {
        _.forEach(nameEmailPairs, function(p) { if (p.email && p.name) {
          sendReject(p.email, p.name, title);
        }});
      } else {
        //console.log("Wrong Result: " + result + " - " + paper.id);
      }

    });

  });


});
