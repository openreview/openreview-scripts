#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');
var _ = require('lodash');

var urlPrefix = 'http://localhost:8529/_db/_system/openreview/'; 

var reviewerFile = process.argv[3];
fs.createReadStream(reviewerFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {

  var email2name = _.fromPairs(_.map(csvDubArr, function(row) {
    var email = row[3].trim();
    var first = row[0].trim();
    var last = row[1].trim();
    return [email, first + " " + last];
  }));

	var createCommentInvitationData = function(rev_num, forum, tpmsId) { return {
		'id': 'ICLR.cc/2016/workshop/-/paper/' + tpmsId + '/comment',
		'signatures': ['ICLR.cc/2016/workshop'],    // the root is allowed to sign as anyone.
		'writers': ['ICLR.cc/2016/workshop'],
    'invitees': ['~', 'ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + rev_num],
		'readers': ['everyone'],

		//     super: ICLR.cc/2016/-/workshop/comment
		// TODO AK: eventually we want to create a superclass of comment but for now this is OK

		'reply': {
		    'forum': forum,      // links this note (comment) to the previously posted note (paper)
        'signatures': '((~.*)|ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + rev_num + '),',
        'writers': '((~.*)|ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + rev_num + '),',
		    'readers': 'everyone,',   // the reply must allow ANYONE to read this note (comment)
		    'content': {
			'title': {
			    'order': 1,
			    'value-regex': '.{1,500}',
			    'description': 'Brief summary of your comment.'
			},
			'comment': {
			    'order': 2,
			    'value-regex': '[\\S\\s]{1,5000}',
			    'description': 'Your comment or reply.'
			}
		    }
		},
		'process': (function (token, invitation, note, count, lib) {
		    //figure out the signatures of the original note
		    var or3origNote = {
			'url': 'http://localhost:8529/_db/_system/openreview/notes?id=' + note.forum,
			'method': 'GET',
			'json': true,
			'port': 8529,
			'headers': {
			    'Authorization': 'Bearer ' + token
			}
		    };

		    var origNote = request(or3origNote);
		    console.log("ORIG NOTE SIGNATURES");
		    console.log(origNote.body.notes[0].content.author_emails.trim().split(","));

		    var mail = {
			"groups": origNote.body.notes[0].content.author_emails.trim().split(","),
			"subject": "New comment on your ICLR submission \"" + note.content.title  + "\".",
			"message": "Your submission to ICLR 2016 workshops has received a new comment.\n\nTo view the comment, click here: http://beta.openreview.net/forum?id=" + note.forum
		    };

		    var or3commentMail = {
			'url': 'http://localhost:8529/_db/_system/openreview/mail',
			'method': 'POST',
			'port': 8529,
			'json': true,
			'body': mail,
			'headers': {
			    'Authorization': 'Bearer ' + token
			}
		    };

		    var sendMail = function (o) {
			var resp = request(o);
			console.log("MAIL");
			console.log(resp);
		    };
		    sendMail(or3commentMail);
		    return true;
		}) + ""
  };};
  var duedate = new Date('Thu Mar 10 2016 17:15:00 GMT-0500 (EST)').getTime();
  var createInvitationData = function(rev_num, note, tpmsId) { return {
    'id': 'ICLR.cc/2016/workshop/-/paper/' + tpmsId + '/review/' + rev_num,
    'signatures': ['ICLR.cc/2016/workshop'],  // super user can sign as anyone
    'writers': ['ICLR.cc/2016/workshop'],
    'readers': ['everyone', 'ICLR.cc/2016/workshop', 'ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + rev_num],
    'invitees': ['ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + rev_num],
    'duedate': duedate,
    'reply': {
        'forum': note.forum,
        'parent': note.id,
        'signatures': '((~.*)|ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + rev_num + '),',  // author reveals their ~ handle or remains anonymous
        // This reviewer has not been assigned yet
        'writers': '((~.*)|ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + rev_num + '),',  // author reveals their ~ handle or remains anonymous
        'readers': 'everyone,',     // review must be world readable
        'content': {
      'title': {
          'order': 1,
          'value-regex': '.{0,500}',
          'description': 'Brief summary of your review.'
      },
      'review': {
          'order': 2,
          'value-regex': '[\\S\\s]{1,5000}',
          'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.'
      },
      'rating': {
          'order': 3,
          'value-regex': '10: Top 5% of accepted papers, seminal paper|9: Top 15% of accepted papers, strong accept|8: Top 50% of accepted papers, clear accept|7: Good paper, accept|6: Marginally above acceptance threshold|5: Marginally below acceptance threshold|4: Ok but not good enough - rejection|3: Clear rejection|2: Strong rejection|1: Trivial or wrong'
      },
      'confidence': {
          'order': 4,
          'value-regex': '5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature|4: The reviewer is confident but not absolutely certain that the evaluation is correct|3: The reviewer is fairly confident that the evaluation is correct|2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper|1: The reviewer\'s evaluation is an educated guess'
      }
        }
    },
    'process': (function (token, invitation, note, tpmsId, lib) {
        //figure out the signatures of the original note
        var or3origNote = {
      'url': 'http://localhost:8529/_db/_system/openreview/notes?id=' + note.forum,
      'method': 'GET',
      'json': true,
      'headers': {
          'Authorization': 'Bearer ' + token
      }
        };

        var origNote = request(or3origNote);
        console.log("ORIG NOTE SIGNATURES");
        console.log(origNote.body.notes[0].content.author_emails.trim().split(","));

        var mail = {
      "groups": origNote.body.notes[0].content.author_emails.trim().split(","),
      "subject": "Review of your ICLR submission \"" + note.content.title + "\".",
      "message": "Your submission to ICLR 2016 workshops has received a new review.\n\nTo view the review, click here: http://beta.openreview.net/forum?id=" + note.forum
        };

        var or3commentMail = {
      'url': 'http://localhost:8529/_db/_system/openreview/mail',
      'method': 'POST',
      'port': 8529,
      'json': true,
      'body': mail,
      'headers': {
          'Authorization': 'Bearer ' + token
      }
        };

        var sendMail = function (o) {
      var resp = request(o);
      console.log("MAIL");
      console.log(resp);
        };
        sendMail(or3commentMail);

        // Now submit a new version of the review invitation that has no invitees
        // This effectively makes it impossible to submit another review
        var fulfilled_review_invite = invitation;
        fulfilled_review_invite.invitees = [];
        fulfilled_review_invite.process = (function (token, invitation, note, tpmsId, lib) {
      console.log("THIS REVIEW HAS ALREADY BEEN SUBMITTED");
      return true;
        }) + "";

        var or3fulfilled_rev = {
      'url': 'http://localhost:8529/_db/_system/openreview/invitations',
      'method': 'POST',
      'port': 8529,
      'json': true,
      'body': fulfilled_review_invite,
      'headers': {
          'Authorization': 'Bearer ' + token
      }
        };
        var resp = request(or3fulfilled_rev);
        console.log("CREATING FULFILLED REVIEW");
        console.log(fulfilled_review_invite);
        console.log(resp);
        return true;
    }) + ""
  };};

  var assignReviewer = function(reviewerEmail, count, note, tpmsId, token) {

    var invitationData = createInvitationData(count, note, tpmsId);
    request(
      {
        'method': 'POST',
        'url': urlPrefix + 'invitations', 
        'json': true,
        'body': invitationData,
        'headers': {
          'Authorization': 'Bearer ' + token 
        }
      },
      function (error, response, body) {
        console.log("creating invitation");
        if (!error && response.statusCode == 200) {
          console.log("created invitation: " + body.id);

          var rev_grp = {
              'id': 'ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer',
              'signatures': ['ICLR.cc/2016/workshop'],
              'writers': ['ICLR.cc/2016/workshop'],
              'readers': ['everyone'],
              'members': ['ICLR.cc/2016/workshop'],
              'signatories': []
          };

          request(
            {
              'method': 'POST',
              'url': urlPrefix + 'groups', 
              'json': true,
              'body': rev_grp,
              'headers': {
                'Authorization': 'Bearer ' + token 
              }
            },
            function (error, response, body) {
              console.log("creating reviewer parent group");
              if (!error && response.statusCode == 200) {
                console.log("created reviewer parent group: " + body.id);


                var reviewerData = {
                  'id': 'ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + count,
                  'signatures': ['ICLR.cc/2016'],
                  'writers': ['ICLR.cc/2016'],
                  'members': [reviewerEmail],
                  'readers': ['ICLR.cc/2016', 'ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/' + count],
                  'signatories': [reviewerEmail]
                };
                request(
                  {
                    'method': 'POST',
                    'url': urlPrefix + 'groups', 
                    'json': true,
                    'body': reviewerData,
                    'headers': {
                      'Authorization': 'Bearer ' + token 
                    }
                  },
                  function (error, response, body) {

                    console.log("creating reviewers");
                    if (!error && response.statusCode == 200) {
                      console.log("created reviewer: " + body.id);


                      var name = email2name[reviewerEmail] || 'Reviewer';
                      var message = (
                        "Dear " + name + ",\n\n"
                        + "Thanks for agreeing to review Workshop Track submissions for ICLR 2016.\n\n"
                        + "Your assignment is now available on OpenReview.net.  Please log in at\n\n"
                        + "http://beta.openreview.net/forum?id=" + note.forum + "\n\n"
                        + "to find your assignment.  Please check it now to ensure that you do not have a conflict of interest and that you feel qualified to review the paper.  If there are any problems, alert the program chairs as quickly as you can by e-mail to iclr2016.programchairs@gmail.com\n\n"
                        + "*Important* - your reviews are due on Thursday, March 10, by 5 pm Eastern Standard Time.\n\n"
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
                            'subject': 'ICLR 2016 Workshop Track reviewer assignment',
                            'message': message 
                          },
                          'headers': {
                            'Authorization': 'Bearer ' + token 
                          }
                        },
                        function (error, response, body) {

                          console.log("creating reviewers");
                          if (!error && response.statusCode == 200) {
                            console.log("created reviewer: " + body.id);
                            console.log(body);
                          }
                        }
                      );

                    } else {
                      console.log("error adding reviewer: " + JSON.stringify(reviewerData));
                    }
                  }
                );



              }
            }
          );















        } else {
          console.log("error creating invitation: " + JSON.stringify(invitationData));
        }
      }
    );

    var commentInvitationData = createCommentInvitationData(count, note.forum, tpmsId);
    request(
      {
        'method': 'POST',
        'url': urlPrefix + 'invitations', 
        'json': true,
        'body': commentInvitationData,
        'headers': {
          'Authorization': 'Bearer ' + token 
        }
      },
      function (error, response, body) {
        console.log("creating comment invitation");
        if (!error && response.statusCode == 200) {
          console.log("created comment invitation: " + body.id);
        }
      }
    );



  };  



  console.log("about to login");
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
      console.log("logging in: " + response.statusCode);
      if (!error && response.statusCode == 200) {
        console.log("logged in");

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

              console.log('MAP: ' + JSON.stringify(note2replyInvitationMap))

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
                  console.log("getting notes");
                  if (!error && response.statusCode == 200) {
                    console.log("got notes");
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
                      return _.map(counts, function(count) {
                        return {tpmsId: count, note: note};
                      });
                    }));
                    var tpmsPaperId2note = _.fromPairs(_.filter(_.map(tpmsIdNotePairs, function(pair) {
                      return [pair.tpmsId, pair.note];
                    })));

                    var assignmentFile = process.argv[2];
                    fs.createReadStream(assignmentFile).pipe(csvparse({delimiter: ','}, function(err, csvDubArr) {

                      var notesWithReviewers = _.map(_.groupBy(csvDubArr, function(row) { 
                        return row[0];
                      }), function(rows, tpmsId) {
                        var note = tpmsPaperId2note[tpmsId + ""];
                        var reviewerEmails = _.map(rows, function(row) {
                          return row[1].trim();
                        });

                        if (note) {


                          _.forEach(reviewerEmails, function(reviewerEmail, index) {
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


                                  console.log("\n***** ");
                                  console.log("tpmsId: " + tpmsId);
                                  console.log("noteId: " + (note ? note.id : null));
                                  console.log("reviewerEmail: " + reviewerEmail);
                                  console.log("invs " + invIds.toString());

                                  var hasReviewInvitation = _.some(invIds, function(id) {
                                    return id.indexOf('/review/') > -1;
                                  });

                                  var hasPublishedReview = _.some(notes, function(note) {
                                    return (
                                      note.invitation.indexOf('paper/' + tpmsId + '/review/') > -1
                                    ) && (_.indexOf(note.tauthors, reviewerEmail) > -1);
                                  });

                                  console.log("hasReviewInvitation: " + hasReviewInvitation);
                                  console.log("hasPublishedReview: " + hasPublishedReview);
                                  if (!hasReviewInvitation && !hasPublishedReview) {
                                    console.log("assigning reviewer: " + reviewerEmail);
                                    console.log("assigning tpmsId: " + tpmsId);
                                    console.log("assigning noteId: " + (note ? note.id : 'missing'));
                                    assignReviewer(reviewerEmail, index + 10, note, tpmsId, token);
                                  }

                                } else {
                                  console.log("get invitations error where reviewerEmail = " + reviewerEmail);
                                  console.log("get invitations error where note id = " + (note ? note.id : ''));
                                }
                              }
                            );


                          });
                        } else {
                          console.log("note missing: " + tpmsId);
                        };
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

