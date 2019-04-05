function(){
    var or3client = lib.or3client;
    var CONFERENCE_ID = 'learningtheory.org/COLT/2019/Conference';
    var SHORT_PHRASE = 'COLT 2019';
    var PC_MEMBERS_SUBMITTED = 'Program_Committee/Submitted';
    var PROGRAM_CHAIRS = CONFERENCE_ID + '/Program_Chairs';

    or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
    .then(function(result) {
      var forumNote = result.notes[0];
      var paper_pc_submitted_grp = CONFERENCE_ID + '/Paper' + forumNote.number + '/' + PC_MEMBERS_SUBMITTED;
      return or3client.or3request(or3client.grpUrl + '?id=' + paper_pc_submitted_grp, {}, 'GET', token)
      .then(result => {
        var submitted_pc_grp = result.groups[0];
        members = submitted_pc_grp.members
        if (members.length){
          var program_committee_mail = {
            groups: members,
            subject: '[' + SHORT_PHRASE + '] Comment posted to a paper for which you are on the Program Committee. Paper Number: ' + forumNote.number + ', Paper Title: \"' + forumNote.content.title + '\"',
            message: 'A comment was posted to a paper for which you are on the Program Committee.\n\nPaper Title: ' + forumNote.content.title + '\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
          };
          return or3client.or3request(or3client.mailUrl, program_committee_mail, 'POST', token);
        }
        else {
          console.log('No members in submitted group: ', submitted_pc_grp.id);
        }
        return Promise.resolve();
      })
      .then(result => {
        var program_chair_mail = {
          groups: [PROGRAM_CHAIRS],
          subject: '[' + SHORT_PHRASE + '] Comment posted to Paper Number: ' + forumNote.number + ', Paper Title: \"' + forumNote.content.title + '\"',
          message: 'Following comment was posted:\n\nPaper Title: ' + forumNote.content.title + '\n\nComment title: ' + note.content.title + '\n\nComment: ' + note.content.comment + '\n\nTo view the comment, click here: ' + baseUrl + '/forum?id=' + note.forum + '&noteId=' + note.id
        };
        return or3client.or3request(or3client.mailUrl, program_chair_mail, 'POST', token);
      })
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
};
