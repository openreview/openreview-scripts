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
  .then(result=> or3client.activateUser(iclr_params.hugo.first, iclr_params.hugo.last, iclr_params.hugo.id))

  /*
  .then(result=> or3client.or3request(regUrl, {id: iclr_params.oriol.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.activateUser(iclr_params.oriol.first, iclr_params.oriol.last, iclr_params.oriol.id))

  .then(result=> or3client.or3request(regUrl, {id: iclr_params.marcAurelio.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.activateUser(iclr_params.marcAurelio.first, iclr_params.marcAurelio.last, iclr_params.marcAurelio.id))
  
  .then(result=> or3client.or3request(regUrl, {id: iclr_params.tara.id, needsPassword: true}, 'POST', token))
  .then(result=> or3client.activateUser(iclr_params.tara.first, iclr_params.tara.last, iclr_params.tara.id))
  
  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017workshop, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017workshopProgramChairs, 'POST', token))
  .then(result=> or3client.or3request(grpUrl, iclr_params.iclr2017workshopAreaChairs, 'POST', token))
  .then(result=> or3client.addHostMember(iclr_params.iclr2017workshop.id, token))
  .then(result=> or3client.or3request(inviteUrl, or3client.createSubmissionInvitation(
    { 
      'id':iclr_params.iclr2017workshop.id+'/-/submission', 
      'signatures':[iclr_params.iclr2017workshop.id], 
      'writers':[iclr_params.iclr2017workshop.id], 
      'invitees':['~'],
      'reply':{
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
            //'value-regex': '[^,\\n]+(,[^,\\n]+)*',
            'value-regex': "^([a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))+(;[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))*$",
            'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).'
          },
          'pdf': {
            'order': 4,
            'value-regex': 'upload|http://arxiv.org/pdf/.+',   // either an actual pdf or an arxiv link
            'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv.'
          },          
          'keywords': {
            'order': 5,
            'value-regex': '[^,\\n]+(,[^,\\n]+)*',
            'description': 'Comma separated list of keywords.'
          },
        }
      }
    }
  ), 'POST', token))
  .then(result => or3client.addHostMember(iclr_params.iclr2017workshop.id, token))
  .then(result => console.log(iclr_params.iclr2017workshop.id+' added to homepage'))
  */
})