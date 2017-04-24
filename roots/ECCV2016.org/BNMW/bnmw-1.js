var port = process.argv[2] || 3000;

var or3client = require('../../or3/client').mkClient(port);
var bnmw = require('./bnmw_params');
var fs = require('fs');
var _ = require('lodash');

var grpUrl = or3client.grpUrl;
var loginUrl = or3client.loginUrl;
var regUrl = or3client.regUrl;
var inviteUrl = or3client.inviteUrl;
var mailUrl = or3client.mailUrl;
var notesUrl = or3client.notesUrl;

var headers = bnmw.headers; //what are these?

or3client.getUserTokenP(bnmw.rootUser).then(function(token){
  or3client.or3request( notesUrl+'?invitation=ECCV2016.org/BNMW/-/submission',{},'GET', token)
  .then(function(result){    
    console.log('result:',result.notes)
    var official_reviewers = ['reviewer-1', 'reviewer-2'];
    var notes = result.notes;
    
    for(var i = 0; i<notes.length; i++){
      //for each note, it's open review invitation, then set that invitation's noninvitees to be the official reviewers.
      //this is so that open reviews can't be signed as 'reviewer-1', etc.
      var note = notes[i];
      console.log('updating note '+note.id+", "+i)
      or3client.or3request( inviteUrl+'?id=ECCV2016.org/BNMW/paper/-/open/review/'+note.id,{}, 'GET', token )
      .then(result => or3client.or3request(inviteUrl, _.assign(result.invitations[0], {noninvitees:official_reviewers}), 'POST', token))
      .then(result=>console.log('result is:',result))

      //create official reviews for each note, assigning the official reviewers as their invitees
      var official_review_invitation = or3client.createReviewInvitation(
        { 'id': 'ECCV2016.org/BNMW/paper/-/official/review/'+note.id,
          'signatures': ['ECCV2016.org/BNMW'],
          'writers': ['ECCV2016.org/BNMW'],
          'invitees': official_reviewers,
          'process':or3client.reviewProcess,
          'reply':{
            'forum': note.id, 
            'replyto': note.id,
            'writers': {'values-regex':'~.*|reviewer-.+'},
            'signatures': {'values-regex':'~.*|reviewer-.+'},
          } 
        }
        );

      _.assign(official_review_invitation, {duedate: 9462978020546});
      or3client.or3request(inviteUrl, official_review_invitation, 'POST', token);
    }; 
    
  })
  
})