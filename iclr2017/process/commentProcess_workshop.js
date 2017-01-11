function(){
    var or3client = lib.or3client;

    var getAuthorEmails = function(origNote){
      console.log('get author emails initiated');
      var origNoteAuthors = origNote.content.authorids;
      var origNoteSignature = origNote.signatures[0];

      var author_mail = {
        "groups": origNoteAuthors,
        "subject": "Comment on your submission to ICLR 2017: \"" + origNote.content.title + "\".",
        "message": "Your submission to ICLR 2017 Workshop has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
    };

    var getReviewerEmails = function(origNote){
      console.log('get reviewer emails initiated');
      return or3client.or3request(or3client.grpUrl+'?id=ICLR.cc/2017/workshop/paper'+origNote.number+'/reviewers',{},'GET',token)
      .then(result=>{
        var reviewers = result.groups[0].members;
        console.log('reviewers before filter',reviewers);
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if(signatureIdx>-1){
          reviewers.splice(signatureIdx,1);
        };

        console.log('reviewers after filter',reviewers);
        var reviewer_mail = {
          "groups": reviewers,
          "subject": "Comment posted to your assigned paper: \"" + origNote.content.title + "\"",
          "message": "A submission to ICLR 2017 Workshop, for which you are an official reviewer, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      })
    };

    var getPCEmails = function(origNote){
      console.log('get PC emails initiated');
      return or3client.or3request(or3client.grpUrl+'?id=ICLR.cc/2017/pcs',{},'GET',token)
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
          "subject": "Private comment posted to a paper: \"" + origNote.content.title + "\"",
          "message": "A submission to ICLR 2017 Workshop has received a private comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token );
      })
    };

    var getCommentEmails = function(replytoNoteSignatures, origNote){
      console.log('replytoNoteSignatures before filter:',replytoNoteSignatures);

      if(note.readers.indexOf('everyone') == -1){
        replytoNoteSignatures=[];
      };
      console.log('replytoNoteSignatures after filter:',replytoNoteSignatures);
      var comment_mail = {
        "groups": replytoNoteSignatures,
        "subject":"Your post has received a comment, paper: \"" + origNote.content.title + "\"",
        "message": "One of your posts has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, comment_mail, 'POST', token );
    };

    var origNoteP = or3client.or3request(or3client.notesUrl+'?id='+note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl+'?id='+note.replyto,{},'GET',token) : null;

    Promise.all([
      origNoteP,
      replytoNoteP
    ]).then(result => {
      var origNote = result[0].notes[0];

      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteReaders = replytoNote ? replytoNote.readers : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : null;

      var promises = [];

      var visibleToEveryone = note.readers.indexOf('everyone')>-1 ? true : false;
      var visibleToReviewers = note.readers.indexOf('ICLR.cc/2017/workshop/reviewers')>-1 ? true : false;
      var visibleToPCs = note.readers.indexOf('ICLR.cc/2017/pcs')>-1 ? true : false;

      if(visibleToEveryone){
        var authorMailP = getAuthorEmails(origNote);
        promises.push(authorMailP);
      };

      if(visibleToEveryone || visibleToReviewers){
        var reviewerMailP = getReviewerEmails(origNote);
        promises.push(reviewerMailP);
      };

      if(visibleToReviewers || visibleToPCs){
        var pcMailP = getPCEmails(origNote);
        promises.push(pcMailP);
      }

      var rootComment = note.forum == note.replyto;
      var anonComment = replytoNoteSignatures.indexOf('(anonymous)')>-1 ? true : false;
      var selfComment = replytoNoteSignatures.indexOf(note.signatures[0])>-1 ? true : false;

      if(!rootComment && !anonComment && !selfComment) {
        var commentMailP = getCommentEmails(replytoNoteSignatures, origNote);
        promises.push(commentMailP);
      };

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
