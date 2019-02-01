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
  "ICLR 2016 - Workshop Track",
  "International Conference on Learning Representations",
  "May 2 - 4, 2016, Caribe Hilton, San Juan, Puerto Rico",
  "http://www.iclr.cc/doku.php?id=iclr2016:main",
  "Submission Deadline: 18 Feb 2016"
], true);

var sm = mkStateManager();

var httpGetP = function(url, queryOrBody) {
  var df = $.Deferred();
  httpGet(url, queryOrBody, function(result) {
    df.resolve(result);
  }, function(err) {
    df.reject(result);
  });
  return df.promise();
};

var invitationP = httpGetP('invitations', {id: 'ICLR.cc/2016/workshop/-/submission'}).then(function(result) {
  return result.invitations[0];
});

var notesP = httpGetP('notes', {invitation: 'ICLR.cc/2016/workshop/-/submission', maxtcdate: Date.now()}).then(function(result) {
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
      _.forEach(notes, function(note) {
        $attach('#notes', 'mkNotePanel', [note, {
          titleLink: 'HREF',
          withReplyCount: true
        }], true);
      });
    }
  }
});

