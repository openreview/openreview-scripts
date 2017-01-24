function(){
    console.log('comment process initiated')
    var or3client = lib.or3client;

    var list = note.invitation.replace(/_/g, ' ').split('/');
    list.splice(list.indexOf('-', 1));
    var conference = list.join(' ')

    var getAuthorEmails = function(origNote){
      console.log('get author emails initiated');
      var origNoteAuthors = origNote.content.authorids;
      var origNoteSignature = origNote.signatures[0];

      var author_mail = {
        "groups": origNoteAuthors,
        "subject": "Comment on your submission to ICLR 2017: \"" + origNote.content.title + "\".",
        "message": "Your submission to " + conference + " has received a comment.\n\nTitle: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      return or3client.or3request(or3client.mailUrl, author_mail, 'POST', token);
    };

    var getReviewerEmails = function(origNote){
      console.log('get reviewer emails initiated');
      var origNoteNumber = origNote.number;
      return or3client.or3request(or3client.grpUrl + '?id=ICLR.cc/2017/conference/paper' + origNoteNumber + '/reviewers', {}, 'GET', token)
      .then(result => {
        var reviewers = result.groups[0].members;
        console.log('reviewers before filter: ' + reviewers);
        var signatureIdx = reviewers.indexOf(note.signatures[0]);
        if (signatureIdx > -1){
          reviewers.splice(signatureIdx, 1);
        };

        console.log('reviewers after filter',reviewers);
        var reviewer_mail = {
          "groups": reviewers,
          "subject": "Comment posted to your assigned paper: \"" + origNote.content.title + "\"",
          "message": "A submission to " + conference + ", for which you are an official reviewer, has received a comment. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum
        };
        return or3client.or3request(or3client.mailUrl, reviewer_mail, 'POST', token);
      })
    };

    var getAreachairEmails = function(origNote){
      console.log('get AC emails initiated');
      var origNoteNumber = origNote.number;
      return or3client.or3request(or3client.grpUrl + '?id=ICLR.cc/2017/conference/paper' + origNoteNumber + '/areachairs', {}, 'GET', token)
      .then(result => {
        var areachairs = result.groups[0].members;
        var signatureIdx = areachairs.indexOf(note.signatures[0]);
        console.log('areachairs before filter: ' + areachairs);
        if (signatureIdx > -1){
          areachairs.splice(signatureIdx, 1);
        };
        console.log('areachairs after filter: ' + areachairs);
        var areachair_mail = {
          "groups": areachairs,
          "subject": "Comment posted to your assigned paper: \"" + origNote.content.title + "\"",
          "message": "A submission to " + conference + ", for which you are an official area chair, has received a comment. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum
        };
        return or3client.or3request(or3client.mailUrl, areachair_mail, 'POST', token);
      })
    };

    var getPCEmails = function(origNote){
      console.log('get PC emails initiated');
      return or3client.or3request(or3client.grpUrl + '?id=ICLR.cc/2017/pcs', {}, 'GET', token)
      .then(result => {
        var pcs = result.groups[0].members;

        console.log('pcs before filter: ' + pcs);

        var workshopIdx = pcs.indexOf('ICLR.cc/2017/workshop');
        if (workshopIdx > -1){
          pcs.splice(workshopIdx, 1);
        }
        var conferenceIdx = pcs.indexOf('ICLR.cc/2017/conference');
        if (conferenceIdx > -1){
          pcs.splice(conferenceIdx, 1);
        }

        var signatureIdx = pcs.indexOf(note.signatures[0]);
        if (signatureIdx > -1){
          pcs.splice(signatureIdx, 1);
        }

        //if any member of the PCs is an author, remove that PC from email recipients
        for (var i = 0; i < origNote.content.authorids.length; i++){
          var currentAuth = origNote.content.authorids[i];

          var pcIdx = pcs.indexOf(currentAuth);

          //workaround for hugo
          if (currentAuth == 'hugo.larochelle@usherbrooke.ca'){
            pcIdx = pcs.indexOf('hugo@twitter.com');
          }

          if (pcIdx > -1){
            pcs.splice(pcIdx, 1);
            console.log('Program chair ' + currentAuth + ' found in authorids. Removing them from email recipients list');
          }
        }
        console.log('pcs after filter: ' + pcs);

        var pc_mail = {
          "groups": pcs,
          "subject": "Private comment posted to a paper: \"" + origNote.content.title + "\"",
          "message": "A submission to " + conference + " has received a private comment. \n\nTitle: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum
        };
        return or3client.or3request( or3client.mailUrl, pc_mail, 'POST', token );
      })
    };

    var getCommentEmails = function(replytoNoteSignatures, origNote){
      console.log('replytoNoteSignatures before filter: ' + replytoNoteSignatures);

      if (note.readers.indexOf('everyone') == -1){
        replytoNoteSignatures = [];
      };
      console.log('replytoNoteSignatures after filter: '+replytoNoteSignatures);
      var comment_mail = {
        "groups": replytoNoteSignatures,
        "subject":"Your post has received a comment, paper: \"" + origNote.content.title + "\"",
        "message": "One of your posts has received a comment.\n\nTitle: " + note.content.title + "\n\nComment: " + note.content.comment + "\n\nTo view the comment, click here: " + baseUrl + "/forum?id=" + note.forum
      };
      return or3client.or3request(or3client.mailUrl, comment_mail, 'POST', token);
    };

    console.log('functions defined')
    var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
    var replytoNoteP = note.replyto ? or3client.or3request(or3client.notesUrl + '?id=' + note.replyto, {}, 'GET', token) : null;
    console.log('promises created')
    Promise.all([
      origNoteP,
      replytoNoteP
    ]).then(result => {
      console.log('promises resolving')
      var origNote = result[0].notes[0];
      var origNoteNumber = origNote.number;

      var replytoNote = note.replyto ? result[1].notes[0] : null;
      var replytoNoteReaders = replytoNote ? replytoNote.readers : null;
      var replytoNoteSignatures = replytoNote ? replytoNote.signatures : null;

      var promises = [];
      var visibleToEveryone = note.readers.indexOf('everyone') > -1 ? true : false;

      var visibleToReviewers = note.readers.indexOf('ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers') > -1 ? true : false;
      var visibleToAreachairs = note.readers.indexOf('ICLR.cc/2017/conference/ACs_and_organizers') > -1 ? true : false;
      var visibleToPCs = note.readers.indexOf('ICLR.cc/2017/conference/organizers') > -1 ? true : false;

      if (visibleToEveryone){
        var authorMailP = getAuthorEmails(origNote);
        promises.push(authorMailP);
      };

      if (visibleToEveryone || visibleToReviewers){
        var reviewerMailP = getReviewerEmails(origNote);
        promises.push(reviewerMailP);
      };

      if (visibleToEveryone || visibleToReviewers || visibleToAreachairs){
        var areachairMailP = getAreachairEmails(origNote);
        promises.push(areachairMailP);
      };

      if (visibleToReviewers || visibleToAreachairs || visibleToPCs){
        var pcMailP = getPCEmails(origNote);
        promises.push(pcMailP);
      }

      var rootComment = note.forum == note.replyto;
      var anonComment = replytoNoteSignatures.indexOf('(anonymous)') > -1 ? true : false;
      var selfComment = replytoNoteSignatures.indexOf(note.signatures[0]) > -1 ? true : false;

      if (!rootComment && !anonComment && !selfComment) {
        var commentMailP = getCommentEmails(replytoNoteSignatures, origNote);
        promises.push(commentMailP);
      };

      return Promise.all(promises);
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
  };
