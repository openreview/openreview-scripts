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
          headers: {
            'Authorization': 'Bearer ' + token 
          }
        },
        function (error, response, body) {
          if (!error && response.statusCode == 200) {
            var notes = body.notes;
            var tpmsIdNotePairs = _.flatten(_.map(_.filter(notes, function(n) {
              return n.id == n.forum;
            }), function(note) {

              //if (note.id == note.forum) {
              //  console.log("\n");
              //  console.log("*****NOTE******");
              //  console.log("noteId: " + note.id);
              //  console.log("replyInvitations: " + JSON.stringify(note.replyInvitations));

              //  var hasComment = _.some(note.replyInvitations, function(id) {
              //    return id.indexOf('/comment') > -1;
              //  });
              //  console.log("note missing comment: " + !hasComment);

              //  var hasUnofficial = _.some(note.replyInvitations, function(id) {
              //    return id.indexOf('/unofficial_review') > -1;
              //  });

              //  console.log("note missing unofficial: " + !hasUnofficial);
              //  console.log("has unofficial but missing commment: " + (hasUnofficial && !hasComment));
              //  console.log("has comment but missing unofficial: " + (!hasUnofficial && hasComment));
              //  console.log("has neither: " + (!hasUnofficial && !hasComment));

              //}

              var commentInvitations = _.filter(note.replyInvitations, function(invId) {
                var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/comment");
                var matches = invId.match(regex);
                return matches && matches[0] == invId;
              });
              var unofficialInvitations = _.filter(note.replyInvitations, function(invId) {
                var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/unofficial_review");
                var matches = invId.match(regex);
                return matches && matches[0] == invId;
              });
              var commentCounts = _.map(commentInvitations, function(commentInvitation) {
                return commentInvitation ? commentInvitation.substring(30).slice(0, -8) : '';
              }); 
              var unofficialCounts = _.map(unofficialInvitations, function(unofficialInvitation) {
                return unofficialInvitation ? unofficialInvitation.substring(30).slice(0, -8) : '';
              }); 

              var counts = _.flatten([commentCounts, unofficialCounts]);
              return _.map(counts, function(count) {
                return {tpmsId: count, note: note};
              });
              
            }));

            var tpmsId2note = _.fromPairs(_.filter(_.map(tpmsIdNotePairs, function(pair) {
              return [pair.tpmsId, pair.note];
            })));

            var assignmentFile = process.argv[2];
            fs.createReadStream(assignmentFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {


              var missingReviewPairs = [];
              var missingCommentPairs = []

              _.forEach(csvDubArr, function(row) {
                var tpmsId = row[0].trim();
                var reviewerEmail = row[1].trim();
                var note = tpmsId2note[tpmsId + ''];

                request(
                  {
                    method: 'GET',
                    url: urlPrefix + 'invitations?invitee=' + reviewerEmail,
                    json: true,
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

                      var hasReviewInvitation = _.some(invIds, function(id) {
                        return id.indexOf('/review/') > -1;
                      });

                      var hasPublishedReview = _.some(notes, function(note) {
                        return (
                          note.invitation.indexOf('paper/' + tpmsId + '/review/') > -1
                        ) && (_.indexOf(note.tauthors, reviewerEmail) > -1);
                      });

                      if (!hasReviewInvitation && !hasPublishedReview) {

                        console.log("\n");
                        console.log("******ASSIGNMENT*****");
                        console.log("tpmsId: " + tpmsId);
                        console.log("noteId: " + (note ? note.id : 'missing'));
                        console.log("reviewerEmail: " + reviewerEmail);
                        console.log('reviewer invitations: ' + JSON.stringify(invIds));
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
