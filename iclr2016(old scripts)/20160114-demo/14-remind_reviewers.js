#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');
var _ = require('lodash');



var reviewerFile = process.argv[3];
fs.createReadStream(reviewerFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {

  var email2name = _.fromPairs(_.map(csvDubArr, function(row) {
    var email = row[3].trim();
    var first = row[0].trim();
    var last = row[1].trim();
    return [email, first + " " + last];
  }));

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



        //GET invitations 
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
            console.log("getting invitations");
            if (!error && response.statusCode == 200) {
              console.log("got invitations");
              var invitations = body.invitations;


              var note2replyInvitationMap = _.reduce(invitations, function(acc, inv) {
                var forumInvs = acc[inv.reply.forum] || [];
                var parentInvs = acc[inv.reply.parent] || [];

                return _.assign(acc, _.fromPairs([
                  [inv.reply.forum, _.flatten([forumInvs, inv.id])],
                  [inv.reply.parent, _.flatten([parentInvs, inv.id])]
                ]));
                  
              }, {});

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

                      var replyInvitations = note2replyInvitationMap[note.id]

                      var commentInvitations = _.filter(replyInvitations, function(invId) {
                        var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/comment");
                        var matches = invId.match(regex);
                        return matches && matches[0] == invId;
                      });
                      var unofficialInvitations = _.filter(replyInvitations, function(invId) {
                        var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/unofficial_review");
                        var matches = invId.match(regex);
                        return matches && matches[0] == invId;
                      });
                      var commentCounts = _.map(commentInvitations, function(commentInvitation) {
                        return commentInvitation ? commentInvitation.substring(30).slice(0, -8) : '';
                      }); 
                      var unofficialCounts = _.map(unofficialInvitations, function(unofficialInvitation) {
                        return unofficialInvitation ? unofficialInvitation.substring(30).slice(0, -18) : '';
                      }); 

                      var counts = _.flatten([commentCounts, unofficialCounts]);

                      console.log("note: " + note.id);
                      console.log("counts: " + counts.toString());

                      return _.map(counts, function(count) {
                        console.log("note: " + note.id);
                        return {tpmsId: count, note: note};
                      });
                      
                    }));

                    var tpmsId2note = _.fromPairs(_.filter(_.map(tpmsIdNotePairs, function(pair) {
                      return [pair.tpmsId, pair.note];
                    })));

                    var assignmentFile = process.argv[2];
                    fs.createReadStream(assignmentFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {



                      _.forEach(csvDubArr, function(row) {
                        var tpmsId = row[0].trim();
                        var reviewerEmail = row[1].trim();
                        var note = tpmsId2note[tpmsId + ''];

                        var reviewerName = email2name[reviewerEmail] || "Reviewer"; 

                        var hasPublishedReview = _.some(notes, function(note) {
                          return (
                            note.invitation.indexOf('paper/' + tpmsId + '/review/') > -1
                          ) && (_.indexOf(note.tauthors, reviewerEmail) > -1);
                        });


                        if (!hasPublishedReview) {
                          console.log("\n");
                          console.log("not yet published: " + tpmsId + " / " + (note ? note.id : 'note missing'));
                          console.log("reviewer name: " + reviewerName);

                          if (note) {
                            var message = (
                              "Dear " + reviewerName + ",\n\n"

                              + "Your review of ICLR 2016 workshop submissions was due last Thursday, March 10, but we have not yet received it.\n"
                              + "Please complete your review and submit it as soon as possible to provide the authors with time to respond to your review before decisions are made.\n\n"

                              + "Please log in at "
                              + "http://beta.openreview.net/forum?id=" + note.forum + " "
                              + "to find your assignment.  If there are any problems, alert the program chairs as quickly as you can by e-mail to iclr2016.programchairs@gmail.com\n\n"

                              + "Thank you for your prompt attention to this,\n"
                              + "Hugo, Samy, and Brian -- ICLR 2016 program chairs\n"

                            );

                            request(
                              {
                                'method': 'POST',
                                'url': urlPrefix + 'mail', 
                                'json': true,
                                'body': {
                                  'groups' : [reviewerEmail], 
                                  'subject': 'Please complete your ICLR 2016 workshop reviews ASAP',
                                  'message': message 
                                },
                                'headers': {
                                  'Authorization': 'Bearer ' + token 
                                }
                              },
                              function (error, response, body) {

                                if (!error && response.statusCode == 200) {
                                  console.log("mail success: " + reviewerEmail + " / " + tpmsId + " / " + (note ? note.id : 'note missing'));
                                } else {
                                  console.log("mail error: " + reviewerEmail + " / " + tpmsId + " / " + (note ? note.id : 'note missing'));
                                  console.log(JSON.stringify(error));
                                  console.log(JSON.stringify(response));
                                  console.log(JSON.stringify(body));
                                }

                              }
                            );
                          }
                        } else {
                          console.log("\n");
                          console.log("review done: " + tpmsId + " / " + (note ? note.id : 'note missing'));
                        }


                      });

                    }));

                  }
                }
              );

            }
          }
        );

      }
  });

}));
