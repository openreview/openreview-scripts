#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');
var _ = require('lodash');

var urlPrefix = 'http://localhost:8529/_db/_system/openreview/'; 

//Login
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
      //GET notes
      request(
        {
          method: 'GET',
          url: urlPrefix + 'notes', 
          json: true,
          body: {},
          headers: {
            'Authorization': 'Bearer ' + token 
          }
        },
        function (error, response, body) {
          if (!error && response.statusCode == 200) {
            var notes = _.filter(body.notes, function(n) {
              return n.id == n.forum;
            });

            var dubArr = _.map(notes, function(note) {

              if (note.id == note.forum) {
                console.log("\n");
                console.log("*****NOTE******");
                console.log("noteId: " + note.id);
                console.log("replyInvitations: " + JSON.stringify(note.replyInvitations));
              }


              var commentInvitation = _.find(note.replyInvitations, function(invId) {
                var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/comment");
                var matches = invId.match(regex);
                return matches && matches[0] == invId;
              });
              var count = commentInvitation ? commentInvitation.substring(30).slice(0, -8) : '';
              return [count, note];
            });
            var tpmsId2note = _.fromPairs(dubArr);

            var assignmentFile = process.argv[2];
            fs.createReadStream(assignmentFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {


              var missingReviewPairs = [];
              var missingCommentPairs = []

              _.forEach(csvDubArr, function(row) {
                var tpmsId = row[0].trim();
                var reviewerEmail = row[1].trim();
                var note = tpmsId2note[tpmsId] || null;

                request(
                  {
                    method: 'GET',
                    url: urlPrefix + 'invitations', 
                    json: true,
                    body: {'invitee': reviewerEmail},
                    headers: {
                      'Authorization': 'Bearer ' + token 
                    }
                  },
                  function (error, response, body) {

                    if (!error && response.statusCode == 200) {
                      var reviewerInvitations = body.invitations; 
                      var invIds = _.map(_.filter(reviewerInvitations, function(inv) {
                        return note && ((inv.reply.parent == note.id) || (inv.reply.forum == note.id));
                      }), function(inv) {
                        return inv.id;
                      }); 

                      console.log("\n");
                      console.log("******ASSIGNMENT*****");
                      console.log("tpmsId: " + tpmsId);
                      console.log("noteId: " + (note ? note.id : 'missing'));
                      console.log("reviewerEmail: " + reviewerEmail);
                      console.log('reviewer invitations: ' + JSON.stringify(invIds));

                      var missingReviewInvitation = !_.some(invIds, function(id) {
                        return id.indexOf('/review/') > -1;
                      });
                      console.log("missing review invitation: " + missingReviewInvitation);
                      if (missingReviewInvitation) {
                        missingReviewPairs.push({reviewer: reviewerEmail, tpmsId: tpmsId, noteId: note ? note.id : null});
                      }

                      var missingCommentInvitation = !_.some(invIds, function(id) {
                        return id.indexOf('/comment') > -1;
                      });
                      console.log("missing comment invitation: " + missingCommentInvitation);
                      if (missingCommentInvitation) {
                        missingCommentPairs.push({reviewer: reviewerEmail, tpmsId: tpmsId, noteId: note ? note.id : null});
                      }

                    }
                  }
                );

              });

            }));

          }
        }
      );
    }
});
