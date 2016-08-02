#!/usr/bin/env node

var fs = require('fs');
var request = require('request');
var csvparse = require('csv-parse');
var _ = require('lodash');

var urlPrefix = 'http://localhost:8529/_db/_system/openreview/'; 


console.log("about to login");
//Login
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
    console.log("logging in: " + response.statusCode);
    if (!error && response.statusCode == 200) {
      console.log("logged in");

      var token = body.token; 

      var createCommentInvitationData = function(forum, tpmsId) { return {
        'id': 'ICLR.cc/2016/workshop/-/paper/' + tpmsId + '/comment',
        'signatures': ['ICLR.cc/2016/workshop'],    // the root is allowed to sign as anyone.
        'writers': ['ICLR.cc/2016/workshop'],
        'invitees': ['~', 'ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer'],
        'readers': ['everyone'],

        //     super: ICLR.cc/2016/-/workshop/comment
        // TODO AK: eventually we want to create a superclass of comment but for now this is OK

        'reply': {
            'forum': forum,      // links this note (comment) to the previously posted note (paper)
            'signatures': '((~.*)|ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/.*),',
            'writers': '((~.*)|ICLR.cc/2016/workshop/paper/' + tpmsId + '/reviewer/.*),',
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


      var forumId = process.argv[2];
      var commentNumber = process.argv[3];
      var commentInvitationData = createCommentInvitationData(forumId, commentNumber);
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
          } else {
            console.log("problem: ");
          }
        }
      );
    }
  }
);
