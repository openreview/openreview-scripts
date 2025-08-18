var or3client = require('../../or3/or3client');
var fs = require('fs');
var _ = require('lodash');

var grpUrl = 'http://localhost:3000/groups';
var loginUrl = 'http://localhost:3000/login';
var regUrl = 'http://localhost:3000/register';
var inviteUrl = 'http://localhost:3000/invitations';
var mailUrl = 'http://localhost:3000/mail';
var notesUrl = 'http://localhost:3000/notes';

var headers = { 'User-Agent': 'test-create-script' }; //what are these?

var rootUser = {
  id:'OpenReview.net',
  password:''
}

or3client.getUserTokenP(rootUser).then(function(token){
  or3client.or3request(notesUrl+'?invitation=eccv.org/2016/workshop/-/submission', {}, 'GET', token)
  .then( function(result){
    console.log(result);
    return or3client.or3request(inviteUrl, or3client.createVerdictInvitation(result.notes[0].id, 'eccv.org/2016/workshop', ['~ECCV_Program_Chairs']), 'POST', token)
  })
  .then(result=>console.log("finished:",result))
});