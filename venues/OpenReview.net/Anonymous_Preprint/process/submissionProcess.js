function() {
    // email authors, create revision, withdraw and comment invites
    // create blind submission and author group
    var or3client = lib.or3client;

    var CONF = 'OpenReview.net/Anonymous_Preprint';

    var AUTHORS = CONF + '/Authors';
    var BLIND_SUBMISSION = CONF + '/-/Blind_Submission';

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
    };

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

        var addRevisionInvitation = {
          id: savedPaperGroup.id + '/-/Revision',
          super: CONF + '/-/Revision',
          invitees: [authorGroupId],
          signatures: [CONF],
          reply: {
            forum: note.id,
            referent: note.id,
            signatures: {
              'values-regex': authorGroupId,
              'description': 'How your identity will be displayed.'
            }
          }
        };

        var commentInvitation = {
          id: savedPaperGroup.id + '/-/Public_Comment',
          super: CONF+ '/-/Public_Comment',
          writers: [CONF],
          invitees: [authorGroupId],
          signatures: [CONF],
          reply: {
            forum: savedNote.id,
            signatures: {
              'values-regex': "~.*|"+authorGroupId,
              'description': 'How your identity will be displayed.'
            }
          }
        };


        var revealInvitation = {
          id: savedPaperGroup.id + '/-/Reveal_Authors',
          super: CONF+ '/-/Reveal_Authors',
          writers: [CONF],
          invitees: [authorGroupId],
          signatures: [CONF],
          reply: {
            forum: savedNote.id,
            replyto: savedNote.id,
            signatures: {
              'values-regex': "~.*",
              'description': 'How your identity will be displayed.'
            }
          }
        };

        var withdrawPaperInvitation = {
          id: savedPaperGroup.id + '/-/Withdraw',
          super: CONF+ '/-/Withdraw',
          writers: [CONF],
          invitees: [authorGroupId],
          signatures: [CONF],
          reply: {
            forum: savedNote.id,
            replyto: savedNote.id,
            signatures: {
              'values-regex': "~.*|"+authorGroupId,
              'description': 'How your identity will be displayed.'
            }
          }
        };


        var batchPromises = Promise.all([
          or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
          or3client.or3request(or3client.inviteUrl, addRevisionInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, revealInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, withdrawPaperInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, commentInvitation, 'POST', token),
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
