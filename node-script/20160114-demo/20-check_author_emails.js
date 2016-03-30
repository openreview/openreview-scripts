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
          df.resolve(body.notes);
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
    var specialId2Group = _.fromPairs(_.map(groups, function(group) {
      return [group.specialId, group];
    }));
    var papers = _.filter(all[1], function(p) {
      return !p.content.CMT_id.trim();
    });

    _.forEach(papers, function(paper) {
      var tauthor = paper.tauthors[0];
      var emailList = _.map(paper.content.author_emails.split(","), function(e) {
        return e.trim();
      });
      if (_.includes(emailList, tauthor)) {
      } else {
        //the author is not listed:
        console.log("\n"); 
        console.log("Error");
        console.log("user: " + tauthor); 
        console.log("author_emails: " + paper.content.author_emails); 
      }
    });
  });

});
