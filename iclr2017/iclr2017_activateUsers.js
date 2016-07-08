var url = process.argv[2] || 'http://localhost:3000';

var or3client = require('../../or3/client').mkClient(url);
var fs = require('fs');
var iclr_params = require('./iclr2017_params.js')

// The open review local url
var grpUrl = or3client.grpUrl;
var loginUrl = or3client.loginUrl;
var regUrl = or3client.regUrl;
var inviteUrl = or3client.inviteUrl;
var mailUrl = or3client.mailUrl;
var notesUrl = or3client.notesUrl;

or3client.getUserTokenP(iclr_params.rootUser).then(function(token){
  or3client.or3request(grpUrl, iclr_params.iclr, 'POST', token)
  
  .then(result=> or3client.or3request(regUrl, {id: iclr_params.hugo.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.or3request(regUrl, {id: iclr_params.oriol.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.or3request(regUrl, {id: iclr_params.michael.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.or3request(regUrl, {id: iclr_params.melisa.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.or3request(regUrl, {id: iclr_params.tara.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.activateUser(iclr_params.hugo.first, iclr_params.hugo.last, iclr_params.hugo.id))
  .then(result=> or3client.activateUser(iclr_params.oriol.first, iclr_params.oriol.last, iclr_params.oriol.id))
  .then(result=> or3client.activateUser(iclr_params.michael.first, iclr_params.michael.last, iclr_params.michael.id))
  .then(result=> or3client.activateUser(iclr_params.melisa.first, iclr_params.melisa.last, iclr_params.melisa.id))
  .then(result=> or3client.activateUser(iclr_params.tara.first, iclr_params.tara.last, iclr_params.tara.id))
})