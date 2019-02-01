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
  "ECCV 2016 - Brave New Motion Representations Workshop",
  "European Conference on Computer Vision",
  "Held in Amsterdam, the Netherlands",
  "http://bravenewmotion.github.io",
  "Submission Deadline: August 26, 2016"
], true);

var sm = mkStateManager();

var httpGetP = function(url, queryOrBody) {
  var df = $.Deferred();
  httpGet(url, queryOrBody, function(result) {
    df.resolve(result);
  }, function(err) {
    df.reject(err);
  });
  return df.promise();
};

var invitationP = httpGetP('invitations', {id: 'ECCV2016.org/BNMW/-/submission'}).then(function(result) {
  return result.invitations[0];
});

var submissionInvitation = 'ECCV2016.org/BNMW/-/submission';

var notesP = httpGetP('notes', {invitation: submissionInvitation, maxtcdate: Date.now()}).then(function(result) {
  return result.notes;
});

$.when(invitationP, notesP).done(function(invitation, notes) {
  sm.update('invitationTrip', {
    invitation: invitation
  });
  sm.update('notes', notes);
});

sm.addHandler('workshop', {

  invitationTrip: function(invitationTrip) { if (invitationTrip) {
    var invitation = invitationTrip.invitation;


  }},

  notes: function(notes) {
    if (notes) {
      $('#notes').empty();

      notes.forEach(function(note) {
        $attach('#notes', 'mkNotePanel', [note, {
          titleLink: 'HREF',
          withReplyCount: true
        }], true);
      });
    }
  }
});
