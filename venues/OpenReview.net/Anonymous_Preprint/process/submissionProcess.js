function() {
    // email authors, create revision, withdraw and comment invites
    // create blind submission and author group
    var or3client = lib.or3client;

    var CONF = 'OpenReview.net/Anonymous_Preprint';

    var AUTHORS = CONF + '/Authors';
    var BLIND_SUBMISSION = CONF + '/-/Blind_Submission';

    var withdrawProcess = `function() {
        var or3client = lib.or3client;
        var milliseconds = (new Date).getTime();
        var CONF = 'OpenReview.net/Anonymous_Preprint';

        or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token)
        .then(result => {
            if (result.notes.length > 0){
                var blindedNote = result.notes[0];
                blindedNote.ddate = milliseconds;
                blindedNote.content = {
                  authors: blindedNote.content.authors,
                  authorids: blindedNote.content.authorids
                }
                return or3client.or3request(or3client.notesUrl, blindedNote, 'POST', token);
            } else {
                return Promise.reject('No blinded notes with the original ' + note.forum + ' were found');
            }
        })
        .then(result => or3client.or3request(or3client.notesUrl + '?id=' + result.original, {}, 'GET', token))
        .then(result => {
            if (result.notes.length > 0){
                var originalNote = result.notes[0];
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
      var now = new Date();
      var year = now.getFullYear();
      var firstWord = note.content.title.split(' ')[0].toLowerCase();

      return '@unpublished{\
          \nanonymous' + year + firstWord + ',\
          \ntitle={' + note.content.title + '},\
          \nauthor={Anonymous},\
          \njournal={OpenReview Preprint},\
          \nyear={' + year + '},\
          \nnote={anonymous preprint under review}\
      \n}'
    };

    var blindSubmission = {
      original: note.id,
      invitation: BLIND_SUBMISSION,
      signatures: [CONF],
      writers: [CONF],
      readers: ['everyone'],
      content: {
        authors: ['Anonymous']
      }
    }

    or3client.or3request(or3client.notesUrl, blindSubmission, 'POST', token)
    .then(savedNote => {
      //Send an email to the author of the submitted note, confirming its receipt
      var mail = {
          "groups": note.content.authorids,
          "subject": "Confirmation of your submission to the OpenReview Anonymous Preprint Server: \"" + note.content.title + "\".",
          "message": `Your submission to the OpenReview Anonymous Preprint Server has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + savedNote.forum
      };

      var paperGroup = {
        id: CONF + '/Paper' + savedNote.number,
        signatures: [CONF],
        writers: [CONF],
        members: [],
        readers: [CONF],
        signatories: [CONF]
      };
      return or3client.or3request(or3client.grpUrl, paperGroup, 'POST', token)
      .then(savedPaperGroup => {

        var authorGroupId = savedPaperGroup.id + '/Authors';
        var authorGroup = {
          id: authorGroupId,
          signatures: [CONF],
          writers: [CONF],
          members: note.content.authorids.concat(note.signatures),
          readers: [CONF, authorGroupId],
          signatories: [authorGroupId]
        };

        var withdrawPaperInvitation = {
          id: savedPaperGroup.id + '/-/Withdraw',
          signatures: [CONF],
          writers: [CONF],
          invitees: [authorGroupId],
          noninvitees: [],
          readers: ['everyone'],
          process: withdrawProcess,
          multiReply: false,
          reply: {
            forum: savedNote.id,
            replyto: savedNote.id,
            signatures: {
              'values-regex': authorGroupId,
              description: 'How your identity will be displayed.'
            },
            writers: {
              'values-copied': [
                CONF,
                '{signatures}'
              ]
            },
            readers: invitation.reply.readers,
            content: {
              title: {
                value: 'Submission Withdrawn by the Authors',
                order: 1
              },
              withdrawal_confirmation: {
                  description: 'Please confirm to withdraw.',
                  'value-radio': [
                      'I want to withdraw the anonymous submission on behalf of myself and my co-authors.'
                  ],
                  order: 2,
                  required: true
              }
            }
          }
        }

        var addRevisionInvitation = {
          id: savedPaperGroup.id + '/-/Revision',
          signatures: [CONF],
          writers: [CONF],
          invitees: [authorGroupId],
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

        var batchPromises = Promise.all([
          or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
          or3client.or3request(or3client.inviteUrl, addRevisionInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, withdrawPaperInvitation, 'POST', token),
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
