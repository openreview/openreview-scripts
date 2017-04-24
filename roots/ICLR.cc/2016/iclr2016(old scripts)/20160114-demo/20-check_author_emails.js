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
        'id': 'OpenReview.net', 'password': ''
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

  var groupsP = function() {
    var df = p.defer();
    request(
      {
        method: 'GET',
        url: urlPrefix + 'groups?regex=.+@.+', 
        json: true,
        headers: {
            'Authorization': 'Bearer ' + token
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          df.resolve(body.groups);
        } else {
          df.resolve([]);
        }
      }
    );
    return df.promise;
  }();

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

  p.when(p.all(groupsP, papersP), function(all) {
    var groups = all[0];
    var id2Group = _.fromPairs(_.map(groups, function(group) {
      return [group.id, group];
    }));

    var papers = _.filter(all[1], function(p) {
      return !p.content.CMT_id.trim();
    });



    _.forEach(papers, function(paper) {
      var tauthor = paper.tauthors[0];
      var emailList = _.map(paper.content.author_emails.split(","), function(e) {
        return e.trim();
      });
      var allEmailed = emailList.length > 0 && _.every(emailList, function(email) {
        return id2Group[email] && id2Group[email].emailable;
      });
      if (allEmailed) {
      } else {
        var success = _.filter(emailList, function(email) {
          return id2Group[email] && id2Group[email].emailable;
        });
        var failure = _.filter(emailList, function(email) {
          return !(id2Group[email] && id2Group[email].emailable);
        });
        console.log("Some authors not emailed - ");
        console.log("paper: " + paper.id); 
        console.log("user: " + tauthor);
        console.log("email success: " + JSON.stringify(success));
        console.log("email failure: " + JSON.stringify(failure));
        console.log("---");
      }
    });

    console.log("**********");
    console.log("**********");
    console.log("**********");

    _.forEach(papers, function(paper) {
      var tauthor = paper.tauthors[0];
      var emailList = _.map(paper.content.author_emails.split(","), function(e) {
        return e.trim();
      });
      var someEmailed = emailList.length > 0 && _.some(emailList, function(email) {
        return id2Group[email] && id2Group[email].emailable;
      });
      if (someEmailed) {
      } else {
        var success = _.filter(emailList, function(email) {
          return id2Group[email] && id2Group[email].emailable;
        });
        var failure = _.filter(emailList, function(email) {
          return !(id2Group[email] && id2Group[email].emailable);
        });
        console.log("not one author emailed - ");
        console.log("paper: " + paper.id); 
        console.log("user: " + tauthor);
        console.log("email success: " + JSON.stringify(success));
        console.log("email failure: " + JSON.stringify(failure));
        console.log("---");
      }
    });
  });

});
