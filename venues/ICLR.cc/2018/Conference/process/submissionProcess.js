function() {
    // email authors, create revision, withdraw and comment invites
    // create blind submission and author group
    var or3client = lib.or3client;

    var CONF = 'ICLR.cc/2018/Conference';
    var PROGRAM_CHAIRS = CONF + '/Program_Chairs';
    var AREA_CHAIRS = CONF + '/Area_Chairs';
    var REVIEWERS = CONF + '/Reviewers';
    var AUTHORS = CONF + '/Authors';
    var REVIEWERS_PLUS = REVIEWERS + '_and_Higher';
    var AREA_CHAIRS_PLUS = AREA_CHAIRS + '_and_Higher';
    var BLIND_SUBMISSION = CONF + '/-/Blind_Submission';

    var withdrawProcess = `function() {
        var or3client = lib.or3client;

        var CONF = 'ICLR.cc/2018/Conference';
        var BLIND_INVITATION = CONF + '/-/Blind_Submission';

        or3client.or3request(or3client.notesUrl + '?id=' + note.referent, {}, 'GET', token)
        .then(result => {
            if (result.notes.length > 0){
                var blindedNote = result.notes[0];

                var milliseconds = (new Date).getTime();
                blindedNote.ddate = milliseconds
                return or3client.or3request(or3client.notesUrl, blindedNote, 'POST', token);
            } else {
                return Promise.reject('No notes with the id ' + note.referent + ' were found');
            }
        })
        .then(result => or3client.or3request(or3client.notesUrl + '?id=' + result.original, {}, 'GET', token))
        .then(result => {
            if (result.notes.length > 0){
                var originalNote = result.notes[0];

                var milliseconds = (new Date).getTime();
                originalNote.ddate = milliseconds;
                originalNote.signatures = [CONF];
                return or3client.or3request(or3client.notesUrl, originalNote, 'POST', token);
            } else {
                return Promise.reject('No notes with the id ' + note.original + ' were found');
            }
        })
        .then(result => done())
        .catch(error => done(error));
        return true;
    }`

    var getBibtex = function(note) {
      var firstWord = note.content.title.split(' ')[0].toLowerCase();

      return '@article{\
          \nanonymous2018' + firstWord + ',\
          \ntitle={' + note.content.title + '},\
          \nauthor={Anonymous},\
          \njournal={International Conference on Learning Representations},\
          \nyear={2018}\
      \n}'
    };


    var addRevisionInvitation = {
      id: CONF + '/-/Paper' + note.number + '/Add_Revision',
      signatures: [CONF],
      writers: [CONF],
      invitees: note.content.authorids.concat(note.signatures),
      noninvitees: [],
      readers: ['everyone'],
      reply: {
        forum: note.id,
        referent: note.id,
        signatures: invitation.reply.signatures,
        writers: invitation.reply.writers,
        readers: invitation.reply.readers,
        content: invitation.reply.content
      }
    }

    var blindSubmission = {
      original: note.id,
      invitation: BLIND_SUBMISSION,
      forum: null,
      parent: null,
      signatures: [CONF],
      writers: [CONF],
      readers: ['everyone'],
      content: {
        authors: ['Anonymous'],
        authorids: ['Anonymous'],
        _bibtex: getBibtex(note)
      }
    }



    or3client.or3request(or3client.inviteUrl, addRevisionInvitation, 'POST', token)
    .then(result => or3client.or3request(or3client.notesUrl, blindSubmission, 'POST', token))
    .then(savedNote => {
      //Send an email to the author of the submitted note, confirming its receipt
      var mail = {
          "groups": note.content.authorids,
          "subject": "Confirmation of your submission to ICLR 2018: \"" + note.content.title + "\".",
          "message": `Your submission to ICLR 2018 has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + savedNote.forum
      };

      var paperGroup = {
        id: CONF + '/Paper' + savedNote.number,
        signatures: [CONF],
        writers: [CONF],
        members: [],
        readers: [CONF],
        signatories: []
      };
      return or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token)
      .then(savedPaperGroup => {

        var reviewerGroupId = savedPaperGroup.id + '/Reviewers';
        var areachairGroupId = savedPaperGroup.id + '/Area_Chair';

        var authorGroupId = savedPaperGroup.id + '/Authors';
        var authorGroup = {
          id: authorGroupId,
          signatures: [CONF],
          writers: [CONF],
          members: note.content.authorids.concat(note.signatures),
          readers: [CONF, PROGRAM_CHAIRS, authorGroupId],
          signatories: [authorGroupId]
        };

        var withdrawPaperInvitation = {
          id: CONF + '/-/Paper' + savedNote.number + '/Withdraw_Paper',
          signatures: [CONF],
          writers: [CONF],
          invitees: [authorGroupId],
          noninvitees: [],
          readers: ['everyone'],
          process: withdrawProcess,
          reply: {
            forum: savedNote.id,
            referent: savedNote.id,
            signatures: invitation.reply.signatures,
            writers: invitation.reply.writers,
            readers: invitation.reply.readers,
            content: {
              withdrawal: {
                description: 'Confirm your withdrawal. The blind record of your paper will be deleted. Your identity will NOT be revealed. This cannot be undone.',
                order: 1,
                'value-radio': ['Confirmed'],
                required: true
              }
            }
          }
        }

        var publicCommentInvitation = {
          id: CONF + '/-/Paper' + savedNote.number + '/Public_Comment',
          signatures: [CONF],
          writers: [CONF],
          invitees: ['~'],
          noninvitees: [authorGroupId, reviewerGroupId, areachairGroupId],
          readers: ['everyone'],
          reply: {
            forum: savedNote.id,
            replyto: null,
            readers: {
              description: 'The users who will be allowed to read the above content.',
              'value-dropdown': ['everyone', REVIEWERS_PLUS, AREA_CHAIRS_PLUS, PROGRAM_CHAIRS]
            },
            signatures: {
              description: 'How your identity will be displayed with the above content.',
              'values-regex': '~.*|\\(anonymous\\)'
            },
            writers: {
              'values-regex': '~.*|\\(anonymous\\)'
            },
            content:{
              title: {
                order: 0,
                'value-regex': '.{1,500}',
                description: 'Brief summary of your comment.',
                required: true
              },
              comment: {
                order: 1,
                'value-regex': '[\\S\\s]{1,5000}',
                description: 'Your comment or reply.',
                required: true
              }
            }
          }
        }

        var officialCommentInvitation = {
          id: CONF + '/-/Paper' + savedNote.number + '/Official_Comment',
          signatures: [CONF],
          writers: [CONF],
          invitees: [reviewerGroupId, authorGroupId, areachairGroupId, PROGRAM_CHAIRS],
          readers: ['everyone'],
          reply: {
            forum: savedNote.id,
            replyto: null,
            readers: {
              description: 'The users who will be allowed to read the above content.',
              'value-dropdown': ['everyone', REVIEWERS_PLUS, AREA_CHAIRS_PLUS, PROGRAM_CHAIRS]
            },
            signatures: {
              description: 'How your identity will be displayed with the above content.',
              'values-regex': [reviewerGroupId, authorGroupId, areachairGroupId, PROGRAM_CHAIRS].join('|')
            },
            writers: {
              'values-regex': [reviewerGroupId, authorGroupId, areachairGroupId, PROGRAM_CHAIRS].join('|')
            },
            content:{
              title: {
                order: 0,
                'value-regex': '.{1,500}',
                description: 'Brief summary of your comment.',
                required: true
              },
              comment: {
                order: 1,
                'value-regex': '[\\S\\s]{1,5000}',
                description: 'Your comment or reply.',
                required: true
              }
            }
          }
        }

        var batchPromises = Promise.all([
          or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
          or3client.or3request(or3client.inviteUrl, withdrawPaperInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, publicCommentInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, officialCommentInvitation, 'POST', token),
          or3client.or3request(or3client.mailUrl, mail, 'POST', token)
        ]);

        return batchPromises
        .then(savedGroups => {
          var authorGroup = savedGroups[0];
          savedNote.content = {
            authors: ['Anonymous'],
            authorids: [authorGroup.id],
            _bibtex: getBibtex(note)
          }
          return or3client.or3request(or3client.notesUrl, savedNote, 'POST', token);
        });
      });
    })
    .then(result => done())
    .catch(error => done(error));

    return true;
}
