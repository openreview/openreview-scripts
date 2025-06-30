function(){
    /*
    This process function is triggered by a note being submitted to
    invitation id = MIDL.amsterdam/2018/Conference/-/Paper<number>/Recommend_Reviewer

    This process function should:
    1) Retrieve information about the submitted paper.
    2) Add the email address as a member to group id = MIDL.amsterdam/2018/Conference/Paper<number>/Reviewers/Invited
    3) Send a recruitment email to the email address, with a link that triggers a recruitment note to be posted
    4) Send an email to the recommender, with instructions on how to check the status of the response
    */
    console.log('process function initiated');
    var SHORT_PHRASE = 'MIDL 2018 Conference';
    var CONFERENCE_ID = 'MIDL.amsterdam/2018/Conference';
    var or3client = lib.or3client;
    var hashKey = or3client.createHash(note.content.email, "2810398440804348173");
    var recruiterName = note.signatures[0].replace('~','').replace('_',' ').replace(/[0-9]/,'');
    console.log('recruiterName: ' + recruiterName)


    // 1) Retrieve information about the submitted paper.
    or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
    .then(function(result){
      paper = result.notes[0];
      console.log('paper info acquired: ' + paper.id);

      // 2) Add the email address as a member to group id = MIDL.amsterdam/2018/Conference/Paper<number>/Reviewers/Invited
      var reviewersInvitedGroupId = 'MIDL.amsterdam/2018/Conference/Paper' + paper.number + '/Reviewers/Invited';
      return or3client.addGroupMember(reviewersInvitedGroupId, note.content.email, token)
    })
    .then(function(result){
      // 3) Send a recruitment email to the email address, with a link that triggers a recruitment note to be posted
      var recruitmentMessage = 'Dear ' + note.content.first + ',\n\n\
You have been nominated by ' + recruiterName + ' to serve as a reviewer for the conference Medical Imaging with Deep Learning (MIDL) 2018.\n\n\
Specifically, you have been recommended to review the following paper:\n\
\n\
Link: https://openreview.net/forum?id='+ paper.id + '\n\
Title: \"' + paper.content.title + '\"\n\
Abstract: \"' + paper.content.abstract + '\"\n\
\n\
Do you accept the the invitation to review this paper?\n\
\n\
To ACCEPT, on click the following link:\n\
https://openreview.net/invitation?id=MIDL.amsterdam/2018/Conference/-/Paper'+ paper.number +'/Reviewer_Invitation&email=' + note.content.email + '&key=' + hashKey + '&response=Yes\n\
\n\
To DECLINE, click on the following link:\n\
https://openreview.net/invitation?id=MIDL.amsterdam/2018/Conference/-/Paper'+ paper.number +'/Reviewer_Invitation&email=' + note.content.email + '&key=' + hashKey + '&response=No\n\
\n\
If you accept, you and ' + recruiterName + ' will be contacted shortly with confirmation of your assignment.\n\
\n\
You can change your decision later by clicking on either of the links above (they can clicked more than once).\n\
\n\
If you have any questions about the above, please contact info@openreview.net\n\
\n\
Thank you,\n\
The OpenReview Team';

      console.log('message to send: ' + recruitmentMessage);

      var recruitmentMessageBody = {
        groups: [note.content.email],
        subject: '[MIDL 2018] You have been nominated to serve as a reviewer',
        message: recruitmentMessage

      };
      return or3client.or3request(or3client.mailUrl, recruitmentMessageBody, 'POST', token);
    })
    .then(function(result){
      // 4) Send a confirmation email to the recommender
      console.log('message1 sent');
      var confirmationMessage = 'Dear ' + recruiterName + ',\n\n\
You have successfully nominated ' + note.content.first + ' to serve as a reviewer for the following paper:\n\
\n\
Link: https://openreview.net/forum?id=' + paper.id + '\n\
Title: ' + paper.content.title + '\n\
\n\
Thank you,\n\
The OpenReview Team';

      var confirmationMessageBody = {
        groups: note.signatures,
        subject: '[MIDL 2018] Reviewer recruitment message successfully sent',
        message: confirmationMessage
      };
      return or3client.or3request(or3client.mailUrl, confirmationMessageBody, 'POST', token);
    })
    .then(result => done())
    .catch(error => done(error));
    return true;
  };




