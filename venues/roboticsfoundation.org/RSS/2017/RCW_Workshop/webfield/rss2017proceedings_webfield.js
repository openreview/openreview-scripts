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
  "RSS 2017 RCW Workshop - Proceedings Track",
  "Robot Communication in the Wild: Meeting the Challenges of Real-world Systems",
  "MIT Cambridge, MA, USA - July 12-16, 2017",
  "https://rss2017-rcw.mit.edu/"
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

var duedate_buffer = 1000 * 60 * 15; // 15 minutes buffer
var invitationP = httpGetP('invitations', {id: 'roboticsfoundation.org/RSS/2017/RCW_Workshop/-_Proceedings/-/Submission'}).then(function(result) {
  console.log('result',result);
  var valid_invitations = _.filter(result.invitations, function(inv){
    return (inv.duedate + duedate_buffer) > Date.now();
  });
  return valid_invitations[0];
},
function(error){
  return error;
});

var getNotes = function() {
  return httpGetP('notes', {invitation: 'roboticsfoundation.org/RSS/2017/RCW_Workshop/-_Proceedings/-/Submission'}).then(function(result) {
    return result.notes;
  },
  function(error){
    return error;
  });
};

$.when(invitationP, getNotes()).done(function(invitation, notes) {

  if (invitation) {
    sm.update('invitationTrip', {
      invitation: invitation
    });
  }
  sm.update('notes', {
    notes: notes
  });

  sm.addHandler('conference', {
    invitationTrip: function(invitationTrip) { if (invitationTrip) {
      var invitation = invitationTrip.invitation;
      $attach('#invitation', 'mkInvitationButton', [invitation, function() {
        if (user && invitation) {
          view.mkNewNoteEditor(invitation, null, null, user, {
            onNoteCreated: function(idRecord) {
              $.when(getNotes()).done(function(notes) {
                sm.update('notes', {
                  notes: notes
                });
              });
            },
            onCompleted: function(editor) {
              $('#invitation .panel').append(editor);
            }
          });
        } else {
          promptLogin(user);
        }
      }], true);
    }},

    notes: function(data) {

      var notes = data.notes;

      if (notes.length > 0) {
        $('#notes').empty().append('<h3>Submitted Papers</h3><hr>');
        _.forEach(notes, function(note) {
          $attach('#notes', 'mkNotePanel', [note, {
            titleLink: 'HREF',
            withReplyCount: true,
            user: user
          }], true);
        });
      }
    }
  });

})
.fail(function(){
  console.log("Invitation and/or notes not found")
});

