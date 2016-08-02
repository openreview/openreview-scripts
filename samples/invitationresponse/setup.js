var or3lib = require('../../../or3/client').mkClient(3000);
var fs = require('fs');
var _ = require('lodash');

var rootUser = {
  id:'OpenReview.net',
  password:''
}

// ECCV ROOT GROUP
var eccv = {
  'id': 'eccv.org',
  'signatures': [rootUser.id],
  'writers': ['eccv.org', rootUser.id],
  'members': [rootUser.id],
  'readers': ['everyone'],
  'signatories': ['eccv.org']
};

var eccv16 = {
  'id': 'eccv.org/2016',
  'signatures': [rootUser.id],
  'writers': ['eccv.org', 'eccv.org/2016'],
  'readers': ['everyone'],
  'members': ['pc@host.com'],
  'signatories': ['eccv.org/2016']
};

//Program Chair
var pc = {
  'id': 'pc@host.com',
  'needsPassword': true
};

var papersubmitter = {
  'id': 'papersubmitter@gmail.com',
  'needsPassword': true
}

// GROUPS TO CREATE
var workshop = {
  'id': 'eccv.org/2016/workshop',
  'signatures': [rootUser.id],
  'writers': ['eccv.org/2016', 'eccv.org/2016/workshop'],
  'readers': ['everyone'],
  'members': ['eccv.org/2016'],
  'signatories': ['eccv.org/2016', 'eccv.org/2016/workshop'],
  'web': fs.readFileSync('web-field-workshop.html', "utf8")
};

var paper = {
  'id': 'eccv.org/2016/workshop/paper',
  'signatures': [rootUser.id],
  'writers': [workshop.id],
  'readers': ['everyone'],
  'members': [workshop.id],
  'signatories': [],
};

var noteBody = {
  'content': {
    'CMT_id':'',
    'abstract':'We aim to detect all instances of a category in an image and, for each instance, mark the pixels that belong to it. We call this task Simultaneous Detection and Segmentation (SDS). Unlike classical bounding box detection, SDS requires a segmentation and not just a box. Unlike classical semantic segmentation, we require individual object instances. We build on recent work that uses convolutional neural networks to classify category-independent region proposals (R-CNN [16]), introducing a novel architecture tailored for SDS. We then use category-specific, top- down figure-ground predictions to refine our bottom-up proposals. We show a 7 point boost (16% relative) over our baselines on SDS, a 5 point boost (10% relative) over state-of-the-art on semantic segmentation, and state-of-the-art performance in object detection. Finally, we provide diagnostic tools that unpack performance and provide directions for future work.',
    'author_emails':"author@gmail.com",
    'authors':'Bharath Hariharan, Pablo Arbeláez, Ross Girshick, Jitendra Malik',
    'conflicts':'cs.berkeley.edu',
    'pdf':'http://arxiv.org/pdf/1407.1808v1.pdf',
    'title':'Simultaneous Detection and Segmentation'
  },
  'forum': null,
  'invitation': 'eccv.org/2016/workshop/-/submission',
  'parent': null,
  'pdfTransfer':"url",
  'readers':["everyone"],
  'signatures':["~super_user1"],
  'writers':["~super_user1"]
};

//DEMO HACK
var email1 = 'melisabok@gmail.com';
var email2 = 'mbok@cs.umass.edu';

var reviewer_account1 = {
  'id': email1,
  'needsPassword': true
}

var reviewer_account2 = {
  'id': email2,
  'needsPassword': true
}

var wrapper_group1 = {
  'id': 'reviewer-1',
  'signatures': [rootUser.id],
  'writers': [email1],
  'readers': ['everyone'], //if this is an anonymizing wrapper group, it probably shouldn't have "everyone" as readers
  'members': [email1],
  'signatories': [email1]
};

var wrapper_group2 = {
  'id': 'reviewer-2',
  'signatures': [rootUser.id],
  'writers': [email2],
  'readers': ['everyone'], //if this is an anonymizing wrapper group, it probably shouldn't have "everyone" as readers
  'members': [email2],
  'signatories': [email2]
};

var reviewers_group = {
  'id': workshop.id + '/reviewers',
  'signatures': [workshop.id],
  'writers': [workshop.id],
  'readers': [workshop.id], 
  'members': [],
  'signatories': [workshop.id]
};

var reviewers_declined_group = {
  'id': workshop.id + '/reviewers-declined',
  'signatures': [workshop.id],
  'writers': [workshop.id, workshop.id + '/reviewers-declined'],
  'readers': [workshop.id, workshop.id + '/reviewers-declined'], 
  'members': [],
  'signatories': [workshop.id]
};

var officialreview_invite;

var responseInvitationProcess = function() {

  var or3client = lib.or3client.mkClient(3000);;
  var hashKey = or3client.createHash(note.content.email, invitation.id);

  if(hashKey == note.content.key) {
    if (note.content.response == 'Yes') {
      console.log("Invitation replied Yes");
      or3client.addInvitationInvitee(invitation.signatures[0] + '/-/paper/review/' + note.content.noteId, note.content.email, token)
      .then(result => or3client.addGroupMember(invitation.signatures[0] + '/reviewers', note.content.email, token))
      .then(result => or3client.removeGroupMember(invitation.signatures[0] + '/reviewers-declined', note.content.email, token))
      .then(function(result) {
        var message = "The user " + note.content.email + " has accepted the invitation to do the review process."
        return or3client.or3request(or3client.mailUrl, { groups: [invitation.signatures[0]], subject: "OpenReview invitation accepted" , message: message}, 'POST', token);
      })
      .catch(error => console.log(error));
    } else if (note.content.response == 'No'){
      console.log("Invitation replied No");
      or3client.removeInvitationInvitee(invitation.signatures[0] + '/-/paper/review/' + note.content.noteId, note.content.email, token)
      .then(result => or3client.addGroupMember(invitation.signatures[0] + '/reviewers-declined', note.content.email, token))
      .then(result => or3client.removeGroupMember(invitation.signatures[0] + '/reviewers', note.content.email, token))
      .then(function(result) {
        var message = "The user " + note.content.email + " has rejected the invitation to do the review process."
        return or3client.or3request(or3client.mailUrl, { groups: [invitation.signatures[0]], subject: "OpenReview invitation rejected" , message: message}, 'POST', token);
      })  
      .catch(error => console.log(error));
    }
    return true;
  } else {
    console.log('Invalid key', note.content.key);
    return false;
  }
}


//Super User must be activated first
or3lib.getUserTokenP(rootUser).then(function(token){
  or3lib.or3request( or3lib.grpUrl, eccv, 'POST', token)
  .then(result => or3lib.or3request( or3lib.grpUrl, eccv16, 'POST', token))
  .then(result => or3lib.or3request( or3lib.regUrl, pc, 'POST', token))
  .then(result => or3lib.or3request( or3lib.regUrl, papersubmitter, 'POST', token))
  .then(result => console.log('groups created'))
  .then(result => or3lib.or3request(or3lib.grpUrl, workshop, 'POST', token))
  .then(result => or3lib.or3request(or3lib.grpUrl, paper, 'POST', token))
  .then(result => console.log('workshop and paper created'))
  .then(result => or3lib.or3request(or3lib.inviteUrl, or3lib.createSubmissionInvitation(
    { 
      'id': workshop.id+'/-/submission', 
      'signatures': [workshop.id], 
      'writers': [workshop.id], 
      'invitees': ['~'], 
      'process': or3lib.submissionProcess
    }
  ), 'POST', token))
  .then(result => console.log('paper submission invitation created'))
  .then(result => or3lib.or3request(or3lib.notesUrl, noteBody, 'POST', token))
  .then(result => console.log('sample note posted'))
  .then(result => or3lib.or3request(or3lib.regUrl, reviewer_account1, 'POST', token))
  .then(result => or3lib.or3request(or3lib.grpUrl, wrapper_group1, 'POST', token))
  .then(result => or3lib.or3request(or3lib.regUrl, reviewer_account2, 'POST', token))
  .then(result => or3lib.or3request(or3lib.grpUrl, wrapper_group2, 'POST', token))
  .then(result => or3lib.or3request(or3lib.grpUrl, reviewers_group, 'POST', token))
  .then(result => or3lib.or3request(or3lib.grpUrl, reviewers_declined_group, 'POST', token))
  .then(result => or3lib.or3request(or3lib.grpUrl + '?id=' + workshop.id + '/reviewers-declined', {}, 'GET', token))
  .then(result => console.log(result.groups[0].signatures))
  .then(result => or3lib.or3request(or3lib.notesUrl, {}, 'GET', token))
  .then(function(result){
    //Create invitation with no invitees
    //var review_invitation = or3lib.createReviewInvitation(workshop.id + '/-/paper/review/' + result.notes[0].id, result.notes[0].id, workshop.id, [], undefined, 99999999999);
    var review_invitation = or3lib.createReviewInvitation(
      { 
        'id': workshop.id + '/-/paper/review/' + result.notes[0].id,
        'duedate': 9999999999999,
        'signatures': [workshop.id],
        'writers': [workshop.id],
        'invitees': [],
        'process':or3lib.reviewProcess,
        'reply':{
          'forum': result.notes[0].id, 
          'parent': result.notes[0].id,
          'writers': {'values-regex':'~.*|reviewer-.+'},
          'signatures': {'values-regex':'~.*|reviewer-.+'},
          'readers': { 
            'values': ['everyone'], 
            description: 'The users who will be allowed to read the above content.'
            },
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
              'value-dropdown': [
                '10: Top 5% of accepted papers, seminal paper', 
                '9: Top 15% of accepted papers, strong accept', 
                '8: Top 50% of accepted papers, clear accept', 
                '7: Good paper, accept',
                '6: Marginally above acceptance threshold',
                '5: Marginally below acceptance threshold',
                '4: Ok but not good enough - rejection',
                '3: Clear rejection',
                '2: Strong rejection',
                '1: Trivial or wrong'
              ]
            },
            'confidence': {
              'order': 4,
              'value-radio': [
                '5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature', 
                '4: The reviewer is confident but not absolutely certain that the evaluation is correct', 
                '3: The reviewer is fairly confident that the evaluation is correct',
                '2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper',
                '1: The reviewer\'s evaluation is an educated guess'
              ]
            }
          }
        } 
      }
    );
    return or3lib.or3request(or3lib.inviteUrl, review_invitation, 'POST', token);
  })
  .then(result => console.log(result))
  .then(result => or3lib.or3request(or3lib.notesUrl, {}, 'GET', token))
  .then(function(result){
    var invitation_response = or3lib.createReviewInvitation({
      'id': workshop.id + '/-/paper/review/invitation/' + result.notes[0].id,
      'signatures': [workshop.id],
      'writers': [workshop.id],
      'readers': ['everyone'],
      'invitees': ['everyone'],
      'reply' : { 
        readers: { 'values': ['everyone'] }, 
        signatures: { 'values-regex': '\\(anonymous\\)' }, 
        writers: { 'values-regex': '\\(anonymous\\)' }, 
        content: {
          'noteId': {
            'order': 0,
            'value': result.notes[0].id,
            'description': 'Note id of the invitation'
          },
          'email': {
            'order': 1,
            'value-regex': '\\S+@\\S+\\.\\S+',
            'description': 'Email address.'
          },
          'key': {
            'order': 2,
            'value-regex': '.{0,100}',
            'description': 'Email key hash'
          },
          'response': {
            'order': 3,
            'value-radio': ['Yes', 'No'],
            'description': 'Invitation response'
          },
        }
      },
      'process': responseInvitationProcess+'',
      'web': fs.readFileSync('web-field-invitation.html', "utf8")
    });
    return or3lib.or3request(or3lib.inviteUrl, invitation_response, 'POST', token);
  })
  .then(function(result) {
    _.forEach([wrapper_group1, wrapper_group2], function(group) {
      var hashKey = or3lib.createHash(group.members[0], result.id);
      var url = "http://localhost:3000/invitation?id=" + result.id + "&email=" + group.members[0] + "&key=" + hashKey + "&response=";
      var message = "You have been invited to review the paper " + noteBody.content.title + ".\n\n" +
       "Please click on the link below to accept the invitation: \n\n" +
        url + "Yes\n\n" +
       "If you won't be able to do it please click on the following link: \n\n" + 
        url + "No\n\n" + 
       "Thanks. ";
      return or3lib.or3request(or3lib.mailUrl, { groups: [group.id], subject: "OpenReview invitation response" , message: message}, 'POST', token);
    })    
  })
  .then(result => console.log('reviewers assigned'))
  .then(hostGroup => or3lib.addHostMember("eccv.org/2016/workshop", token))
  //.then(hostGroup => or3lib.addHostMember("ICLR.cc/2016/workshop", token))
  .then(result => console.log('SETUP COMPLETE'))
  .catch(error => console.log('error', error));
  
})
