function httpGet(url, queryOrBody, success, failure) {
  controller.get(url, queryOrBody, success, failure);
}

function $attach(loc, viewFnName, viewFnArgs, append) {
  var $container = $(loc);
  var $el = view[viewFnName].apply(view, viewFnArgs);
  if (append) {
    $container.append($el);
  } else {
    $container.prepend($el);
  }
}

var $containter = $('#group-container');
$containter.append([
  $('<div id = "header">'),
  $('<div id = "invitation">'),
  $('<div id = "notes">')
]);

$attach('#header', 'mkHostHeader', [
  "NIPS 2016 Workshop - NAMPI",
  "Neural Abstract Machines & Program Induction",
  "NIPS 2016, Barcelona, Spain",
  "https://uclmr.github.io/nampi/",
  "Deadline: October 14th, 2016"
], true);

var sm = mkStateManager();

var httpGetP = function(url, queryOrBody) {
  var df = $.Deferred();
  httpGet(url, queryOrBody,
  function(result) {
    df.resolve(result);
  },
  function(result) {
    df.reject(result);
  });
  return df.promise();
};

var invitationP = httpGetP('invitations', {id: 'NIPS.cc/2016/workshop/NAMPI/-/submission'}).then(function(result) {
  console.log('result',result)
  return result.invitations[0];
},
function(error){
  return error
});

var notesP = httpGetP('notes', {invitation: 'NIPS.cc/2016/workshop/NAMPI/-/submission', maxtcdate: Date.now()}).then(function(result) {
  return result.notes;
},
function(error){
  return error
});

$.when(invitationP, notesP).done(function(invitation, notes) {
  console.log('invitation',invitation)
  sm.update('invitationTrip_nips', {
    invitation: invitation
  });
  sm.update('notes_nips', notes);

  sm.addHandler('conference', {
    invitationTrip_nips: function(invitationTrip) { if (invitationTrip) {
      var invitation = invitationTrip.invitation;
      $attach('#invitation', 'mkInvitationButton', [invitation, function() {
        if (user) {
          view.mkNewNoteEditor(invitation, null, null, user, {
            onNoteCreated: function(idRecord) {
              httpGetP('notes', {
                invitation: 'NIPS.cc/2016/workshop/NAMPI/-/submission',
                maxtcdate: Date.now()
              }).then(function(result) {
                console.log("time to update notes: " + result.notes.length);
                sm.update('notes_nips', result.notes);
              },
              function(error){
                return error
              });
            },
            onCompleted: function(editor) {
              $('#notes').prepend(editor);
            }
          });
        } else {
          promptLogin(user);
        }
      }], true);
    }},

    notes_nips: function(notes) {
      if (notes) {
        $('#notes').empty();
        _.forEach(notes, function(note) {
          $attach('#notes', 'mkNotePanel', [note, {
            titleLink: 'HREF',
            withReplyCount: true
          }], true);
        });
      }
    }
  });

})
.fail(function(){
  console.log("Invitation and/or notes not found")
});

