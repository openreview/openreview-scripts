function() {

    var or3client = lib.or3client;

    var CONF = 'ICLR.cc/2018/Conference';
    var PROGRAM_CHAIRS = CONF + '/Program_Chairs';
    var AREA_CHAIRS = CONF + '/Area_Chairs';
    var REVIEWERS = CONF + '/Reviewers';
    var AUTHORS = CONF + '/Authors';
    var REVIEWERS_PLUS = REVIEWERS + '_and_Higher';
    var AREA_CHAIRS_PLUS = AREA_CHAIRS + '_and_Higher';
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

    //Send an email to the author of the submitted note, confirming its receipt
    var mail = {
        "groups": note.content.authorids,
        "subject": "Confirmation of your submission to ICLR 2018: \"" + note.content.title + "\".",
        "message": `Your submission to ICLR 2018 has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
    };


    or3client.or3request(or3client.inviteUrl, addRevisionInvitation, 'POST', token)
    .then(result => or3client.or3request(or3client.notesUrl, blindSubmission, 'POST', token))
    .then(savedNote => {
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

        var reviewerGroupId = savedPaperGroup.id + '/Reviewers';
        var reviewerGroup = {
          id: reviewerGroupId,
          signatures: [CONF],
          writers: [CONF],
          members: [],
          readers: [CONF, PROGRAM_CHAIRS, AREA_CHAIRS],
          nonreaders: [authorGroupId],
          signatories: []
        };

        var anonReviewer1GroupId = savedPaperGroup.id + '/AnonReviewer1';
        var anonReviewer1Group = {
          id: anonReviewer1GroupId,
          signatures: [CONF],
          writers: [CONF],
          members: [],
          readers: [CONF, PROGRAM_CHAIRS, AREA_CHAIRS, anonReviewer1GroupId],
          nonreaders: [authorGroupId],
          signatories: [anonReviewer1GroupId]
        };

        var anonReviewer2GroupId = savedPaperGroup.id + '/AnonReviewer2';
        var anonReviewer2Group = {
          id: anonReviewer2GroupId,
          signatures: [CONF],
          writers: [CONF],
          members: [],
          readers: [CONF, PROGRAM_CHAIRS, AREA_CHAIRS, anonReviewer2GroupId],
          nonreaders: [authorGroupId],
          signatories: [anonReviewer2GroupId]
        };

        var anonReviewer3GroupId = savedPaperGroup.id + '/AnonReviewer3';
        var anonReviewer3Group = {
          id: anonReviewer3GroupId,
          signatures: [CONF],
          writers: [CONF],
          members: [],
          readers: [CONF, PROGRAM_CHAIRS, AREA_CHAIRS, anonReviewer3GroupId],
          nonreaders: [authorGroupId],
          signatories: [anonReviewer3GroupId]
        };

        var anonReviewer4GroupId = savedPaperGroup.id + '/AnonReviewer4';
        var anonReviewer4Group = {
          id: anonReviewer4GroupId,
          signatures: [CONF],
          writers: [CONF],
          members: [],
          readers: [CONF, PROGRAM_CHAIRS, AREA_CHAIRS, anonReviewer4GroupId],
          nonreaders: [authorGroupId],
          signatories: [anonReviewer4GroupId]
        };

        var anonReviewer5GroupId = savedPaperGroup.id + '/AnonReviewer5';
        var anonReviewer5Group = {
          id: anonReviewer5GroupId,
          signatures: [CONF],
          writers: [CONF],
          members: [],
          readers: [CONF, PROGRAM_CHAIRS, AREA_CHAIRS, anonReviewer5GroupId],
          nonreaders: [authorGroupId],
          signatories: [anonReviewer5GroupId]
        };

        var areachairGroupId = savedPaperGroup.id + '/Area_Chair';
        var areachairGroup = {
          id: areachairGroupId,
          signatures: [CONF],
          writers: [CONF],
          members: [],
          readers: [CONF, PROGRAM_CHAIRS, AREA_CHAIRS, areachairGroupId],
          nonreaders: [authorGroupId],
          signatories: [areachairGroupId]
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
              'values-dropdown': ['everyone', REVIEWERS_PLUS, AREA_CHAIRS_PLUS, PROGRAM_CHAIRS]
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
              'values-dropdown': ['everyone', REVIEWERS_PLUS, AREA_CHAIRS_PLUS, PROGRAM_CHAIRS]
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

        var groupPromises = Promise.all([
          or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token),
          or3client.or3request(or3client.grpUrl, reviewerGroup, 'POST', token),
          or3client.or3request(or3client.grpUrl, areachairGroup, 'POST', token),
          or3client.or3request(or3client.grpUrl, anonReviewer1Group, 'POST', token),
          or3client.or3request(or3client.grpUrl, anonReviewer2Group, 'POST', token),
          or3client.or3request(or3client.grpUrl, anonReviewer3Group, 'POST', token),
          or3client.or3request(or3client.grpUrl, anonReviewer4Group, 'POST', token),
          or3client.or3request(or3client.grpUrl, anonReviewer5Group, 'POST', token),
          or3client.or3request(or3client.inviteUrl, withdrawPaperInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, publicCommentInvitation, 'POST', token),
          or3client.or3request(or3client.inviteUrl, officialCommentInvitation, 'POST', token),
          or3client.addGroupMember(AUTHORS, note.content.authorids.concat(note.signatures), token)
        ]);

        return groupPromises
        .then(savedGroups => {
          var authorGroup = savedGroups[0];
          savedNote.content = {
            authorids: [authorGroup.id],
            authors: ['Anonymous']
          };
          return or3client.or3request(or3client.notesUrl, savedNote, 'POST', token);
        });
      });
    })
    .then(result => or3client.or3request(or3client.mailUrl, mail, 'POST', token))
    .then(result => done())
    .catch(error => done(error));

    return true;
}
