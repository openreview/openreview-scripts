function(){
    var or3client = lib.or3client;

    var getAuthorEmails = function(forumNote){

      var forumNoteAuthors = forumNote.content.authorids;

      var author_mail = {
        "groups": forumNoteAuthors,
        "subject": "Comment on your submission to UAI 2017: \"" + forumNote.content.title + "\".",
        "message": "Your submission to UAI 2017 has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
    };

    var getReviewerEmails = function(forumNote, commentType){

      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/Paper'+forumNote.number+'/Reviewers', {}, 'GET', token)
      .then(result=>{
        var reviewers = result.groups[0].members;

        //if the comment writer is a reviewer, don't send an email to him/herself
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if (signatureIdx>-1) {
          reviewers.splice(signatureIdx,1);
        };

        var reviewer_mail = {
          "groups": reviewers,
          "subject": commentType + " Comment posted to your assigned paper: \"" + forumNote.content.title + "\"",
          "message": "A submission to UAI 2017, for which you are a reviewer, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      });
    };

    var getAreachairEmails = function(forumNote, commentType){

      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/Paper'+forumNote.number+'/Area_Chair', {}, 'GET', token)
      .then(result=>{
        var areachairs = result.groups[0].members;
        var signatureIdx = areachairs.indexOf(note.signatures[0]);
        if (signatureIdx > -1){
          areachairs.splice(signatureIdx,1);
        };
        var areachair_mail = {
          "groups": areachairs,
          "subject": commentType + " Comment posted to your assigned paper: \"" + forumNote.content.title + "\"",
          "message": "A submission to UAI 2017, for which you are the area chair, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );
      });
    };

    var getPCEmails = function(forumNote, commentType, coChairsGroup){

      return or3client.or3request(or3client.grpUrl+'?id=' + coChairsGroup, {}, 'GET', token)
      .then(result=>{
        var pcs = result.groups[0].members;
        var signatureIdx = pcs.indexOf(note.signatures[0]);
        if (signatureIdx>-1) {
          pcs.splice(signatureIdx,1);
        };
        var pc_mail = {
          "groups": pcs,
          "subject": commentType + " Comment posted to a paper: \"" + forumNote.content.title + "\"",
          "message": "A submission to UAI 2017 has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token );
      });
    };

    var getCommentEmails = function(replytoNoteSignatures, forumNote){

      if(note.readers.indexOf('everyone') == -1){
        replytoNoteSignatures=[];
      };

      var comment_mail = {
        "groups": replytoNoteSignatures,
        "subject": "Your post has received a comment, paper: \"" + forumNote.content.title + "\"",
        "message": "One of your posts has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, comment_mail, 'POST', token);
    };

    var forumNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);

    forumNoteP.then(result => {

      var forumNote = result.notes[0];
      var uaiGroup = 'auai.org/UAI/2017';
      var authorsGroup = uaiGroup + '/Paper' + forumNote.number + '/Authors';
      var pcGroup = uaiGroup + '/Program_Committee';
      var spcGroup = uaiGroup + '/Senior_Program_Committee';
      var coChairsGroup = uaiGroup + '/Program_Co-Chairs';

      var regex = /auai\.org\/UAI\/2017\/-\/Paper[1-9]+\/(.*)\/Comment/;
      var commentType = "";

      var match = regex.exec(note.invitation);
      if (match) {
        commentType = match[1];
      }

      var promises = [];

      var visibleToAuthors = note.readers.includes(authorsGroup);
      var visibleToReviewers = note.readers.includes(pcGroup);
      var visibleToAreachairs = note.readers.includes(spcGroup);
      var visibleToPCs = note.readers.includes(coChairsGroup);

      if (visibleToAuthors) {
        console.log('Send notification to authors...');
        var authorMailP = getAuthorEmails(forumNote);
        promises.push(authorMailP);
      };

      if (visibleToReviewers) {
        console.log('Send notification to reviewers...');
        var reviewerMailP = getReviewerEmails(forumNote, commentType);
        promises.push(reviewerMailP);
      };

      if (visibleToAreachairs) {
        console.log('Send notification to area chairs...');
        var areachairMailP = getAreachairEmails(forumNote, commentType);
        promises.push(areachairMailP);
      };

      if (visibleToPCs) {
        console.log('Send notification to program co chairs...');
        var pcMailP = getPCEmails(forumNote, commentType, coChairsGroup);
        promises.push(pcMailP);
      }

      return Promise.all(promises);
    })
    .then(result => {

      if (note.forum != note.replyto) {
        var emails = [];
        for (var i = 0; i < result.length; i ++) {
          var groups = result[i].groups;
          for (var j = 0; j < groups.length; j++) {
            emails.push(groups[j]);
          }
        }

        or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token)
        .then(result => {
          var replytoNote = result.notes[0];
          console.log('replytoNote author');
          console.log(replytoNote.tauthor);
          console.log('emails');
          console.log(emails);
          if(!emails.includes(replytoNote.tauthor)) {
            getCommentEmails(replytoNote.signatures, forumNote)
            .then(result => done());
          } else {
            done();
          }
        })

      } else {
        done();
      }
    })
    .catch(error => done(error));

    return true;
  };
