function(){
    var or3client = lib.or3client;

    var getAuthorEmails = function(forumNote){
      console.log('get author emails initiated')
      var forumNoteAuthors = forumNote.content.authorids;
      var forumNoteSignature = forumNote.signatures[0];

      var author_mail = {
        "groups": forumNoteAuthors,
        "subject": "Comment on your submission to UAI 2017: \"" + forumNote.content.title + "\".",
        "message": "Your submission to UAI 2017 has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
    };

    var getReviewerEmails = function(forumNote){
      console.log('get reviewer emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/Paper'+forumNote.number+'/Reviewers',{},'GET',token)
      .then(result=>{
        var reviewers = result.groups[0].members;

        //if the comment writer is a reviewer, don't send an email to him/herself
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if(signatureIdx>-1){
          reviewers.splice(signatureIdx,1);
        };

        var reviewer_mail = {
          "groups": reviewers,
          "subject": "Comment posted to your assigned paper: \"" + forumNote.content.title + "\"",
          "message": "A submission to UAI 2017, for which you are a Program Committee member, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      })
    };

    var getAreachairEmails = function(forumNote){
      console.log('get AC emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/Paper'+forumNote.number+'/Area_Chair',{},'GET',token)
      .then(result=>{
        var areachairs = result.groups[0].members;
        var signatureIdx = areachairs.indexOf(note.signatures[0]);
        console.log('areachairs before filter:',areachairs);
        if(signatureIdx>-1){
          areachairs.splice(signatureIdx,1);
        };
        console.log('areachairs after filter:',areachairs);
        var areachair_mail = {
          "groups": areachairs,
          "subject": "Comment posted to your assigned paper: \"" + forumNote.content.title + "\"",
          "message": "A submission to UAI 2017, for which you are a Senior Program Committee member, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, areachair_mail, 'POST', token );
      })
    };

    var getPCEmails = function(forumNote){
      console.log('get Program_Committee emails initiated')
      return or3client.or3request(or3client.grpUrl+'?id=auai.org/UAI/2017/Program_Co-Chairs',{},'GET',token)
      .then(result=>{
        var pcs = result.groups[0].members;
        var signatureIdx = pcs.indexOf(note.signatures[0]);
        console.log('pcs before filter:',pcs);
        if(signatureIdx>-1){
          pcs.splice(signatureIdx,1);
        };
        console.log('pcs after filter:',pcs);
        var pc_mail = {
          "groups": pcs,
          "subject": "Comment posted to a paper: \"" + forumNote.content.title + "\"",
          "message": "A submission to UAI 2017 has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token );
      })
    };

    var getCommentEmails = function(replytoNoteSignatures, forumNote){
      console.log('replytoNoteSignatures before filter:',replytoNoteSignatures);

      if(note.readers.indexOf('everyone') == -1){
        replytoNoteSignatures=[];
      };
      console.log('replytoNoteSignatures after filter:',replytoNoteSignatures);
      var comment_mail = {
        "groups": replytoNoteSignatures,
        "subject": "Your post has received a comment, paper: \"" + forumNote.content.title + "\"",
        "message": "One of your posts has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, comment_mail, 'POST', token );
    };

    var forumNoteP = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl+'?id='+note.replyto,{},'GET',token) : null;

    Promise.all([
      forumNoteP,
      replytoNoteP
    ]).then(result => {
      var forumNote = result[0].notes[0];
      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteReaders = replytoNote ? replytoNote.readers : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : null;

      var promises = [];

      var visibleToEveryone = note.readers.indexOf('everyone')>-1 ? true : false;
      var visibleToReviewers = note.readers.indexOf('auai.org/UAI/2017/Program_Committee')>-1 ? true : false;
      var visibleToAreachairs = note.readers.indexOf('auai.org/UAI/2017/Senior_Program_Committee')>-1 ? true : false;
      var visibleToPCs = note.readers.indexOf('auai.org/UAI/2017/Program_Co-Chairs')>-1 ? true : false;

      if(visibleToEveryone){
        var authorMailP = getAuthorEmails(forumNote);
        promises.push(authorMailP);
      };

      if(visibleToEveryone || visibleToReviewers){
        var reviewerMailP = getReviewerEmails(forumNote);
        promises.push(reviewerMailP);
      };

      if(visibleToEveryone || visibleToReviewers || visibleToAreachairs){
        var areachairMailP = getAreachairEmails(forumNote);
        promises.push(areachairMailP);
      };

      if(visibleToReviewers || visibleToAreachairs || visibleToPCs){
        var pcMailP = getPCEmails(forumNote);
        promises.push(pcMailP);
      }

      var rootComment = note.forum == note.replyto;
      var anonComment = replytoNoteSignatures.indexOf('(anonymous)')>-1 ? true : false;
      var selfComment = replytoNoteSignatures.indexOf(note.signatures[0])>-1 ? true : false;

      if(!rootComment && !anonComment && !selfComment) {
        var commentMailP = getCommentEmails(replytoNoteSignatures, forumNote);
        promises.push(commentMailP);
      };

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
