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

  p.when(p.all(papersP, invitationsP), function(all) {
    var papers = all[0];
    var invitations = all[1];

    var trips = _.map(invitations, function(inv) {
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
      return {tpmsId: tpmsId, noteId: inv.reply.forum, invitationId: inv.id};
    });


    var noteId2Trips = _.groupBy(trips, 'noteId');

    _.map(papers, function(paper) {

      var trips = noteId2Trips[paper.id];
      var hasCommentInv = _.some(trips, function(trip) {
        var regex = new RegExp("ICLR.cc/2016/workshop/-/paper/[0-9]+/comment");
        var matches = trip.invitationId.match(regex);
        return (matches && matches[0] == trip.invitationId);
      });

      if (!hasCommentInv) {

        console.log("paper missing comment inv: " + paper.id);
        var tpmsIds = _.map(trips, function(trip) {
          return parseInt(trip.tpmsId);
        }); 
        var tpmsId = _.min(tpmsIds);
        console.log("tpmsId: " + tpmsId);
        if (tpmsId) {


          var commentInvitationData = createCommentInvitationData(paper.id, tpmsId);
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
                console.log("created comment for " + paper.id);
                console.log("created comment invitation " + body.id);
              } else {
                console.log("problem: ");
              }
            }
          );

        }
      }

    });

  });











});
