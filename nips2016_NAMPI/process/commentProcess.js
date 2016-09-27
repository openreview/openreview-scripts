var commentProcess = function(){
    "use strict";
    var or3client = lib.or3client;
    
    var conference = or3client.getConference(note);

    var getAuthorEmails = function(origNote){
      var origNoteAuthors = origNote.content.author_emails.trim().split(",");

      var author_mail = {
        "groups": origNoteAuthors,
        "subject": "Comment on your submission to " + conference + ": \"" + note.content.title + "\".",
        "message": "Your submission to "+ conference +" has received a comment.\n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
      };
      return or3client.or3request( or3client.mailUrl, author_mail, 'POST', token );
    };

    var getReviewerEmails = function(origNoteNumber){
      return or3client.or3request(or3client.grpUrl+'?id=NIPS.cc/2016/workshop/NAMPI/paper'+origNoteNumber+'/reviewers',{},'GET',token)
      .then(result=>{
        var reviewers = result.groups[0].members;
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if(signatureIdx>-1){
          reviewers.splice(signatureIdx,1);
        }

        var reviewer_mail = {
          "groups": reviewers,
          "subject": "Comment posted to your assigned paper: \"" + note.content.title + "\"",
          "message": "A submission to "+ conference+", for which you are an official reviewer, has received a comment. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, reviewer_mail, 'POST', token );
      });
    };

    var getPCEmails = function(){
      return or3client.or3request(or3client.grpUrl+'?id=NIPS.cc/2016/workshop/NAMPI/pcs',{},'GET',token)
      .then(result=>{      
        var pcs = result.groups[0].members;
        var signatureIdx = pcs.indexOf(note.signatures[0]);
        if(signatureIdx>-1){
          pcs.splice(signatureIdx,1);
        }
        var pc_mail = {
          "groups": pcs,
          "subject": "Private comment posted to a paper: \"" + note.content.title + "\"",
          "message": "A submission to "+ conference+" has received a comment for the Program Chairs. \n\nTitle: "+note.content.title+"\n\nComment: "+note.content.comment+"\n\nTo view the comment, click here: "+baseUrl+"/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token );
      });
    };

    var getCommentEmails = function(replytoNoteSignatures){

      if(!note.readers.includes('everyone')){
        replytoNoteSignatures=[];
      }
      var comment_mail = {
        "groups": replytoNoteSignatures,
        "subject":"Your post has received a comment",
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
      var origNoteNumber = origNote.number;

      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : null;

      var promises = [];
      var visibleToEveryone = note.readers.includes('everyone');
      var visibleToReviewers = note.readers.includes('NIPS.cc/2016/workshop/NAMPI/reviewers');
      var visibleToPCs = note.readers.includes('NIPS.cc/2016/workshop/NAMPI/pcs');

      if(visibleToEveryone){
        var authorMailP = getAuthorEmails(origNote);
        promises.push(authorMailP);
      }

      if(visibleToReviewers){
        var reviewerMailP = getReviewerEmails(origNoteNumber);
        promises.push(reviewerMailP);
      }

      if(visibleToPCs){
        var pcMailP = getPCEmails();
        promises.push(pcMailP);
      }

      var rootComment = note.forum == note.replyto;
      var anonComment = replytoNoteSignatures ? replytoNoteSignatures.includes('(anonymous)') : null;
      var selfComment = replytoNoteSignatures ? replytoNoteSignatures.includes(note.signatures[0]) : null;

      if(!rootComment && !anonComment && !selfComment) { 
        var commentMailP = getCommentEmails(replytoNoteSignatures);
        promises.push(commentMailP);
      }

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };  