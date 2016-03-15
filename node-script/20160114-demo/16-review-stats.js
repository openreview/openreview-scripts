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

var assignmentsP = function() {
  var df = p.defer();
  var assignmentFile = process.argv[2];
  fs.createReadStream(assignmentFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {
    var assignments = _.map(csvDubArr, function(row) {
      return {tpmsId: row[0], email: row[1]};
    });
    df.resolve(assignments);
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
        }
      }
    );
    return df.promise;
  }();

  var replyNotesP = function() {
    var df = p.defer();
    request(
      {
        method: 'GET',
        url: urlPrefix + 'notes', 
        json: true,
        headers: {
            'Authorization': 'Bearer ' + token
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          df.resolve(_.filter(body.notes, function(n) {
            return n.forum != n.id;
          }));
        }
      }
    );
    return df.promise;
  }();

  var invitationsP = function() {
    var df = p.defer();
    request(
      {
        method: 'GET',
        url: urlPrefix + 'invitations', 
        json: true,
        headers: {
            'Authorization': 'Bearer ' + token
        }
      },
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
          df.resolve(body.invitations);
        }
      }
    );
    return df.promise;
  }();


  p.when(p.all(assignmentsP, papersP, replyNotesP, invitationsP), function(all) {
    var assignments = all[0];
    var papers = all[1];
    var notes = all[2];
    var invitations = all[3];

    var tpmsId2Assignments = _.groupBy(assignments, 'tpmsId');
    var tpmsIdNoteIdPairs = _.map(invitations, function(inv) {
      var tpmsId = function() {
        var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/unofficial_review");
        var matches = inv.id.match(regex);
        if (matches && matches[0] == inv.id) {
          return inv.id.substring(30).slice(0, -18);
        } else {
          var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/comment");
          var matches = inv.id.match(regex);
          if (matches && matches[0] == inv.id) {
            return inv.id.substring(30).slice(0, -8);
          }
        }
      }();
      return {tpmsId: tpmsId, noteId: inv.reply.forum};
    });

    var parentId2ChildList = _.groupBy(notes, 'parent');

    var noteId2List = _.groupBy(tpmsIdNoteIdPairs, 'noteId');

    var rows = _.flatten(_.map(papers, function(paper) {

      var tpmsIdList = _.map(noteId2List[paper.id], function(pair) {
        return pair.tpmsId;
      });
      var tpmsId = _.find(tpmsIdList, function(tpmsId) {
        return tpmsId2Assignments[tpmsId];
      }) || tpmsIdList[0];
      var paperId = paper.id;
      var cmtId = paper.content.CMT_id;
      var assignments = tpmsId2Assignments[tpmsId];

      if (assignments && assignments.length > 0) {
        return _.map(assignments, function(assignment) {
          var reviewer = assignment.email;
          var replyNotes = parentId2ChildList[paperId];

          var review = _.find(replyNotes, function(reply) {
            var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/" + tpmsId + "/review/.+");
            var matches = reply.invitation.match(regex);
            return  matches && (matches[0] == reply.invitation) && _.some(reply.tauthors, function(tauthor) {
             return tauthor == reviewer;
            });
          }); 

          var title = review ? review.content.title : '';
          var rating = review ? review.content.rating.substring(0, 2) : '';
          var confidence = review ? review.content.confidence.substring(0, 1) : '';
          var signature = review ? review.signatures[0] : '';

          return {
            cmtId: cmtId,
            tpmsId: tpmsId, 
            url: "beta.openreview.net/forum?id=" + paper.id,
            reviewer: reviewer,
            rating: rating,
            confidence: confidence,
            signature: signature,
            title: title
          };
        });
      } else {
        return [{
          cmtId: cmtId,
          tpmsId: tpmsId, 
          url: "beta.openreview.net/forum?id=" + paper.id,
          reviewer: '',
          rating: '',
          confidence: '',
          signature:'',
          title: ''
        }];
      }

    }));

    var header = {
      cmtId: "CMT ID",
      tpmsId: "TPMS ID", 
      url: "Paper URL",
      reviewer: "Reviewer email",
      rating: "Rating",
      confidence: "Confidence",
      signature: "Signature", 
      title: "Review title"
    };

    var rowsWithHeader = _.flatten([header, _.orderBy(rows, ['cmtId', 'tpmsId'], ['asc', 'asc'])]);
    var dubArr = _.map(rowsWithHeader, function(row) {
      return [row.cmtId, row.tpmsId, row.url, row.reviewer, row.rating, row.confidence, row.signature, row.title];
    });
    stringify(dubArr, function(err, str) {
      console.log(str);
    });

  });


});
