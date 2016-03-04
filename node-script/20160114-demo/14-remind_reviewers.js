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
                  return unofficialInvitation ? unofficialInvitation.substring(30).slice(0, -18) : '';
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
                        + "Please remember that your ICLR 2016 workshop reviews are due next week, on Thursday, 10 March 2016, by 5 pm Eastern Standard Time.\n\n"
                        + "Please log in at "
                        + "http://beta.openreview.net/forum?id=" + note.forum + " "
                        + "to find your assignment.  If there are any problems, alert the program chairs as quickly as you can by e-mail to iclr2016.programchairs@gmail.com\n\n"
                        + "In your review's text comments, please provide:\n\n"
                        +  "- A brief summary of the paper's contributions, in the context of prior work.\n"
                        +  "- An assessment of novelty, clarity, significance, and quality.\n"
                        +  "- A list of pros and cons (reasons to accept/reject).\n\n"
                        + "When you submit a review, its text will be immediately publicly viewable.\n\n"
                        + "While most of the interactions in OpenReview.net are non-anonymous, the assigned reviewers of each paper can have their comments posted anonymously. Thus your identity as a reviewer for each of your assigned papers can remain hidden. You can also reply to the review of another reviewer for your assigned papers and choose to remain anonymous. The choice of publishing a comment anonymously is made before you submit your message (see your selection right above the comment text box).\n"
                        + "*Important* - remember that while you know the name of the other reviewers of your assigned papers, the other users of OpenReview (including the authors) don't! Thus, please do not reveal reviewers’ names in your comments.\n\n\n"
                        + "Thank you for your help in putting together the ICLR technical program!\n\n"
                        + "Hugo, Samy, and Brian - the ICLR 2016 program committee"
                      );

                      request(
                        {
                          'method': 'POST',
                          'url': urlPrefix + 'mail', 
                          'json': true,
                          'body': {
                            'groups' : [reviewerEmail], 
                            'subject': 'ICLR workshop track reviews due 10 March 2016',
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
  });

}));
