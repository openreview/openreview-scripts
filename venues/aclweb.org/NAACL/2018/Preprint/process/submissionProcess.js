function() {
    // email authors, create revision, withdraw and comment invites
    // create blind submission and author group
    var or3client = lib.or3client;

    var CONF = 'aclweb.org/NAACL/2018/Preprint';

    var AUTHORS = CONF + '/Authors';
    var BLIND_SUBMISSION = CONF + '/-/Blind_Submission';

    var withdrawProcess = `function() {
        var or3client = lib.or3client;

        var CONF = 'aclweb.org/NAACL/2018/Preprint';
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

      return '@unpublished{\
          \nanonymous2018' + firstWord + ',\
          \ntitle={' + note.content.title + '},\
          \nauthor={Anonymous},\
          \njournal={NAACL 2018 Preprint},\
          \nyear={2018},\
          \nnote={anonymous preprint under review}\
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
          "subject": "Confirmation of your submission to NAACL 2018 Preprint: \"" + note.content.title + "\".",
          "message": `Your submission to NAACL 2018 Preprint has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + savedNote.forum
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
          readers: [CONF, authorGroupId],
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

        var batchPromises = Promise.all([
          or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
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
