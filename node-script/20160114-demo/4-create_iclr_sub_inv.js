#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';
var inviteUrl = 'http://localhost:8529/_db/_system/openreview/invitations';
var mailUrl = 'http://localhost:8529/_db/_system/openreview/mail';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var rootUsr = {
  'id': 'OpenReview.net',
  'password': '12345678'
};

function or3post(url, body, headers) {
  this.url = url;
  this.method = 'POST';
  this.port = 8529;
  this.json = true;
  this.body = body;
  this.headers = headers;
}

function callback(error, response, body) {
  if (!error && response.statusCode == 200) {
      console.log("SUCCESS");
      console.log(body);
  } else {
  console.log("ERROR: " + error);
  console.log("RESPONSE: " + response.statusCode);
  }
}

function loggedInHdr(token) {
  return {
  'Authorization': 'Bearer ' + token,
  'User-Agent': 'test-create-script'
  };
}

// ICLR SUBMISSION INVITE
var subInv = {
    'id': 'ICLR.cc/2016/workshop/-/submission',
    'signatures': ['ICLR.cc/2016/workshop'],                     // I can only sign as this author because I'm creating this invitation with the root user
    'writers': ['ICLR.cc/2016/workshop'],
    'readers': ['everyone'],
    'invitees': ['~'],
    'reply': {
	'forum': null,        // this will be set automatically
	'parent': null,       // the response to this invite will be a forum root
	'signatures': '~.*',     // signatures must reveal their ~ handle
	'writers': '~.*',     // the writers must also reveal their ~ handle
	'readers': 'everyone,',
	'content': {
	    'title': {
		'order': 3,
		'value-regex': '.{1,100}',
		'description': 'Title of paper.'
	    },
	    'abstract': {
		'order': 4,
		'value-regex': '[\\S\\s]{1,5000}',
		'description': 'Abstract of paper.'
	    },
	    'authors': {
		'order': 1,
		'value-regex': '[^,\\n]+(,[^,\\n]+)*',
		'description': 'Comma separated list of author names, as they appear in the paper.'
	    },
	    'author_emails': {
		'order': 2,
		'value-regex': '[^,\\n]+(,[^,\\n]+)*',
		'description': 'Comma separated list of author email addresses, in the same order as above.'
	    },
	    'conflicts': {
		'order': 100,
//		'value-regex': '[^,\\n]+(,[^,\\n]+)*',
		'value-regex': "^([a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))+(;[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))*$",
		'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).'
	    },
	    'CMT_id': {
		'order': 5,
		'value-regex': '.*',                            // if this is a resubmit, specify the CMT ID
		'description': 'If the paper is a resubmission from the ICLR 2016 Conference Track, enter its CMT ID; otherwise, leave blank.'
	    },
	    'pdf': {
		'order': 4,
		'value-regex': 'upload|http://arxiv.org/pdf/.+',   // either an actual pdf or an arxiv link
		'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv.'
	    }
	}
    },
    'process': (function (token, invitation, note, count, lib) {
	var request = require('org/arangodb/request');             // this is messy; on the server I can only use arango's request library
	// TODO AK: should we move away from using the node.js request library in favor of arango only?

	var noteID = note.id;
	var forum = note.forum;

	var create_quick_comment_invite = function(noteID, forum, count) {
	    return {
		'id': 'ICLR.cc/2016/workshop/-/paper/' + count + '/comment',
		'signatures': ['ICLR.cc/2016/workshop'],    // the root is allowed to sign as anyone.
		'writers': ['ICLR.cc/2016/workshop'],
		'invitees': ['~'],              // this indicates the ~ group
		'readers': ['everyone'],

		//     super: ICLR.cc/2016/-/workshop/comment
		// TODO AK: eventually we want to create a superclass of comment but for now this is OK

		'reply': {
		    'forum': forum,      // links this note (comment) to the previously posted note (paper)
//		    'parent': noteID,    // not specified so we can allow comments on comments
		    'signatures': '~.*',    // this regex demands that the author reveal his/her ~ handle
		    'writers': '~.*',    // this regex demands that the author reveal his/her ~ handle
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
	    };
	};

	var quick_comment_invite = create_quick_comment_invite(noteID, forum, count);
	var or3comment_invite = {
	    'url': 'http://localhost:8529/_db/_system/openreview/invitations',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': quick_comment_invite,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	console.log("OR3 COMMENT INVITE");
	console.log(or3comment_invite);

	var resp = request(or3comment_invite);
	console.log("RESPONSE");
	console.log(resp);
	console.log(resp.statusCode);



	// CREATE INVITATION FOR UNOFFICIAL REVIEW
	var create_unofficialreview_invite = function(noteID, forum, count) {
	    return {
		'id': 'ICLR.cc/2016/workshop/-/paper/' + count + '/unofficial_review',
		'signatures': ['ICLR.cc/2016/workshop'],    // can the root sign as anyone? Maybe this should change??
		'writers': ['ICLR.cc/2016/workshop'],
		'invitees': ['~'],              // this indicates the ~ group
		'noninvitees': note.content.author_emails.trim().split(","), // should this be note.writers?
		'readers': ['everyone'],
		//     super: ICLR.cc/2016/-/workshop/comment
		// TODO AK: eventually we want to create a superclass of comment but for now this is OK

		'reply': {
		    'forum': forum,      // links this note (comment) to the previously posted note (paper)
		    'parent': noteID,    // specified as the root
		    'signatures': '~.*',    // this regex demands that the author reveal his/her ~ handle
		    'writers': '~.*',    // this regex demands that the author reveal his/her ~ handle
		    'readers': 'everyone,',   // the reply must allow ANYONE
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
	    };
	};

	var unofficialreview_invite = create_unofficialreview_invite(noteID, forum, count);

	var or3unofficialreview_invite = {
	    'url': 'http://localhost:8529/_db/_system/openreview/invitations',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': unofficialreview_invite,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	resp = request(or3unofficialreview_invite);
	console.log("RESPONSE");
	console.log(resp);
	console.log(resp.statusCode);

	// CREATE REVIEWER GROUPS
	var paper_grp = {
	    'id': 'ICLR.cc/2016/workshop/paper/' + count,
	    'signatures': ['ICLR.cc/2016/workshop'],
	    'writers': ['ICLR.cc/2016/workshop'],
	    'readers': ['everyone'],
	    'members': ['ICLR.cc/2016/workshop'],
	    'signatories': []
	};

	var rev_grp = {
	    'id': 'ICLR.cc/2016/workshop/paper/' + count + '/reviewer',
	    'signatures': ['ICLR.cc/2016/workshop'],
	    'writers': ['ICLR.cc/2016/workshop'],
	    'readers': ['everyone'],
	    'members': ['ICLR.cc/2016/workshop'],
	    'signatories': []
	};

	var or3paper_grp = {
	    'url': 'http://localhost:8529/_db/_system/openreview/groups',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': paper_grp,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	var or3rev_grp = {
	    'url': 'http://localhost:8529/_db/_system/openreview/groups',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': rev_grp,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	var request_with_callback = function (o, callback) {
	    var resp = request(o);
	    console.log('GROUP');
	    console.log(resp);
	    callback();
	};

	request_with_callback(or3paper_grp, function () {
	    var resp = request(or3rev_grp);
	    console.log('SECOND GROUP');
	    console.log(resp);
	});

	var create_reviewer_invite = function(rev_num) {
	    return {
		'id': 'ICLR.cc/2016/workshop/-/paper/' + count + '/reviewer/' + rev_num,
		'signatures': ['ICLR.cc/2016/workshop'],  // super user can sign as anyone
		'writers': ['ICLR.cc/2016/workshop'],
		'readers': ['ICLR.cc/2016/workshop', 'ICLR.cc/2016/workshop/paper/' + count + '/reviewer/' + rev_num],
		'invitees': ['ICLR.cc/2016/workshop/paper/' + count + '/reviewer/' + rev_num],
		'reply': {
		    'forum': noteID,
		    'parent': noteID,
		    'signatures': '((~.*)|ICLR.cc/2016/workshop/paper/' + count + '/reviewer/' + rev_num + '),',  // author reveals their ~ handle or remains anonymous
		    // This reviewer has not been assigned yet
		    'writers': '((~.*)|ICLR.cc/2016/workshop/paper/' + count + '/reviewer/' + rev_num + '),',  // author reveals their ~ handle or remains anonymous
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
		    fulfilled_review_invite.process = (function (token, invitation, note, count, lib) {
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
	    };
	};
	var rev_inv_1 = create_reviewer_invite(1);
	var rev_inv_2 = create_reviewer_invite(2);

	var or3rev_inv_1 = {
	    'url': 'http://localhost:8529/_db/_system/openreview/invitations',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': rev_inv_1,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	resp = request(or3rev_inv_1);
	console.log("RESPONSE");
	console.log(resp);

	var or3rev_inv_2 = {
	    'url': 'http://localhost:8529/_db/_system/openreview/invitations',
	    'method': 'POST',
	    'port': 8529,
	    'json': true,
	    'body': rev_inv_2,
	    'headers': {
		'Authorization': 'Bearer ' + token
	    }
	};

	resp = request(or3rev_inv_2);
	console.log("RESPONSE");
	console.log(resp);

	//   reply email receipt to reply.signatures
	//   create ICLR.cc/2016/workshop/paper/123/reviewers // to be filled in later
	//   add note.signatures to ICLR.cc/2016/workshop/signatures
	//   # allow anyone to comment
	//   create comment invitation:
  	//send email to paper’s signatures’ and reviewers’ email addresses
  	return true;
    }) + ""
};

function create_iclr_paper_submission_invite(url, o) {
    var loginReq = new or3post(loginUrl, rootUsr, headers);
    request(loginReq, function(error, response, body) {
      if (!error && response.statusCode == 200) {
        var token = body.token;
	var commentInvite = new or3post(url, o, loggedInHdr(token));
	console.log(commentInvite);
	request(commentInvite, callback);
    }
  });
}

create_iclr_paper_submission_invite(inviteUrl, subInv);
