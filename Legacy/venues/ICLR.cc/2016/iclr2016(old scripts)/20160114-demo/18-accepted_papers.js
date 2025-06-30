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

  p.when(p.all(noteId2ResultP, papersP), function(all) {
    var noteId2Result = all[0];
    var papers = _.filter(_.sortBy(all[1], function(p) {
      return p.content.CMT_id
    }), function(p) {
      return noteId2Result[p.id] && noteId2Result[p.id] != "Reject"
    });

    var table = _.map(papers, function(paper) {
      var title = paper.content.title;
      var authors = paper.content.authors;
      var author_emails = paper.content.author_emails;
      var url = "beta.openreview.net/forum?id=" + paper.id;
      var cmtId = paper.content.CMT_id
      var result = noteId2Result[paper.id];
      return [title, authors, author_emails, url, result, cmtId];
    });

    stringify(table, function(err, str) {
      console.log(str);
    });

  });



});
