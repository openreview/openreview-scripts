function() {
    // email authors, create blind submission, create revision and withdraw invites

    var or3client = lib.or3client;

    var CONF = 'ICLR.cc/2018/Conference';
    var PROGRAM_CHAIRS = CONF + '/Program_Chairs';
    var AUTHORS = CONF + '/Authors';
    var BLIND_SUBMISSION = CONF + '/-/Blind_Submission';

    var getBibtex = function(note) {
      var firstWord = note.content.title.split(' ')[0].toLowerCase();

      return '@article{\
          \nanonymous2017' + firstWord + ',\
          \ntitle={' + note.content.title + '},\
          \nauthor={Anonymous},\
          \njournal={International Conference on Learning Representations},\
          \nyear={2017}\
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

    or3client.or3request(or3client.notesUrl, blindSubmission, 'POST', token)
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
          reply: {
            forum: savedNote.id,
            referent: savedNote.id,
            signatures: invitation.reply.signatures,
            writers: invitation.reply.writers,
            readers: invitation.reply.readers,
            content: {
              withdrawal: {
                description: 'Confirm your withdrawal',
                order: 1,
                'value-radio': ['Confirmed'],
                required: true
              }
            }
          }
        }

        var batchPromises = Promise.all([
          or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
          or3client.or3request(or3client.inviteUrl, withdrawPaperInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, addRevisionInvitation, 'POST', token),
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
