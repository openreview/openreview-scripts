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

var noteId2ResultP = function() {

  var df = p.defer();
  var resultFile = process.argv[2];
  fs.createReadStream(resultFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {
    var noteIdResultPairs = _.map(csvDubArr, function(row) {
      var noteId = row[3] && row[3].substring('beta.openreview.net/forum?id='.length);
      return {noteId: noteId, accepted: row[0] == "Accept"};
    });

    var noteId2Result = _.fromPairs(_.map(_.groupBy(noteIdResultPairs, 'noteId'), function(pairs, noteId) {
      var allAccept = _.every(pairs, function(p) {
        return p.accepted;
      });

      var someAccept = _.every(pairs, function(p) {
        return p.accepted;
      });

      return [noteId, allAccept ? "Accept" : (someAccept ? "Both" : "Reject")];

    }));

    df.resolve(noteId2Result);
  }));
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
          console.log("accept sent: ");
          console.log("email, name, title: " + email + ", " + name + ", " + title);
          console.log("\n");
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
          console.log("reject sent: ");
          console.log("email, name, title: " + email + ", " + name + ", " + title);
          console.log("\n");
        }
      }
    );
  };

  p.when(p.all(noteId2ResultP, papersP), function(all) {
    var noteId2Result = all[0];
    var papers = _.filter(_.sortBy(all[1], function(p) {
      return p.content.CMT_id;
    }), function(p) {
      return noteId2Result[p.id];
    });


    var table = _.map(papers, function(paper) {
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


      console.log("nameEmailPairs: " + JSON.stringify(nameEmailPairs));

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
        console.log("Wrong Result: " + result + " - " + paper.id);
      }

    });

    stringify(table, function(err, str) {
      console.log(str);
    });

  });


});
