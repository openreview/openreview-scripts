// Assumes the following pattern for meta reviews and official reviews:
// CONFERENCE + '/-/Paper' + number + '/Meta_Review'
// CONFERENCE + '/-/Paper' + number + '/Official_Review'

// Constants
var HEADER_TEXT = 'MIDL 2019 Reviewer Console';
var SHORT_PHRASE = 'MIDL 2019';
var INSTRUCTIONS = '<p class="dark">This page provides information and status updates \
  for MIDL 2019 reviewers. It will be regularly updated as the conference progresses, \
  so please check back frequently for news and other updates.</p>';

var SCHEDULE_HTML = '<h4>Registration Phase</h4>\
    <p>\
      <ul>\
        <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
      </ul>\
    </p>\
  <h4>Bidding Phase</h4>\
  <p>\
    <ul>\
      <li>Provide your reviewing preferences by bidding on papers using the Bidding \
      Interface.</li>\
      <li>Bidding is closed.</li>\
    </ul>\
  </p>\
  <h4>Review Phase</h4>\
  <p><em>8 - 28 January 2019</em>\
    <ul>\
      <li>Submit reviews.</li>\
      <li>See Reviewer Tasks for your assigned papers.</li>\
    </ul>\
  </p>\
  <h4>Rebuttal Period</h4>\
  <p><em>28 January - 10 February 2019</em>\
  </p>\
    <h4>Decision Phase</h4>\
  <p><em>11 February - 20 February 2019</em>\
  </p>\
  ';

var CONFERENCE = 'MIDL.io/2019/Conference';


var FULL_SUBMISSION_ID = CONFERENCE + '/-/Full_Submission';

var OFFICIAL_REVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Official_Review';
var METAREVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Meta_Review';
var WILDCARD_INVITATION = CONFERENCE + '/-/.*';


var ANONREVIEWER_WILDCARD = CONFERENCE + '/Paper.*/AnonReviewer.*';
var AREACHAIR_WILDCARD = CONFERENCE + '/Paper.*/Area_Chair.*';

var ANONREVIEWER_REGEX = /^MIDL\.io\/2019\/Conference\/Paper(\d+)\/AnonReviewer(\d+)/;
var AREACHAIR_REGEX = /^MIDL\.io\/2019\/Conference\/Paper(\d+)\/Area_Chair(\d+)/;

// Ajax functions
var getPaperNumbersfromGroups = function(groups) {
  return _.map(
    _.filter(groups, function(g) { return ANONREVIEWER_REGEX.test(g.id); }),
    function(fg) { return parseInt(fg.id.match(ANONREVIEWER_REGEX)[1], 10); }
  );
};

var getFullNotes = function(noteNumbers) {
  if (!noteNumbers.length) {
    return $.Deferred().resolve([]);
  }

  var noteNumbersStr = noteNumbers.join(',');

  return $.getJSON('notes', { invitation: FULL_SUBMISSION_ID, number: noteNumbersStr, noDetails: true })
    .then(function(result) {
      return result.notes;
    });
};

var getAllRatings = function(callback) {
  var invitationId = CONFERENCE + '/-/Paper.*/Review_Rating';
  var allNotes = [];

  function getPromise(offset, limit) {
    return $.getJSON('notes', { invitation: invitationId, offset: offset, limit: limit, noDetails: true })
    .then(function(result) {
      allNotes = _.union(allNotes, result.notes);
      if (result.notes.length == limit) {
        return getPromise(offset + limit, limit);
      } else {
        callback(allNotes);
      }
    });
  };

  getPromise(0, 1000);

};

var getReviewRatings = function(noteNumbers) {

  if (!noteNumbers.length) {
    return $.Deferred().resolve([]);
  }

  var dfd = $.Deferred();

  var noteMap = buildNoteMap(noteNumbers);

  getAllRatings(function(notes) {
    _.forEach(notes, function(n) {
      var paperPart = _.find(n.invitation.split('/'), function(part) {
        return part.indexOf('Paper') !== -1;
      });
      var num = parseInt(paperPart.split('Paper')[1], 10);
      if (num in noteMap) {
        noteMap[num][n.forum] = n;
      }
    });

    dfd.resolve(noteMap);
  });

  return dfd.promise();
};

var getReviewerGroups = function(noteNumbers) {

  if (!noteNumbers.length) {
    return $.Deferred().resolve({});
  }

  var noteMap = buildNoteMap(noteNumbers);

  return $.getJSON('groups', { id: CONFERENCE + '/Paper.*/AnonReviewer.*' })
    .then(function(result) {

      _.forEach(result.groups, function(g) {
        var matches = g.id.match(ANONREVIEWER_REGEX);
        var num, index;
        if (matches) {
          num = parseInt(matches[1], 10);
          index = parseInt(matches[2], 10);

          if ((num in noteMap) && g.members.length) {
            noteMap[num][index] = g.members[0];
          }
        }
      });
      return noteMap;
    })
    .fail(function(error) {
      displayError();
      return null;
    });
};

var getUserProfiles = function(userIds) {
  if (!userIds.length) {
    return $.Deferred().resolve([]);
  }

  return $.post('/user/profiles', JSON.stringify({ids: userIds}))
  .then(function(result) {

    var profileMap = {};

    _.forEach(result.profiles, function(profile) {

      var name = _.find(profile.content.names, ['preferred', true]) || _.first(profile.content.names);
      profile.name = _.isEmpty(name) ? view.prettyId(profile.id) : name.first + ' ' + name.last;
      profile.email = profile.content.preferredEmail;
      profileMap[profile.id] = profile;
    })

    return profileMap;
  })
  .fail(function(error) {
    displayError();
    return null;
  });
};

var findProfile = function(profiles, id) {
  var profile = profiles[id];
  if (profile) {
    return profile;
  } else {
    return {
      id: id,
      name: '',
      email: id
    }
  }
}

var getOfficialReviews = function(noteNumbers) {

  if (!noteNumbers.length) {
    return $.Deferred().resolve({});
  }

  return $.getJSON('notes', { invitation: CONFERENCE + '/-/Paper.*/Official_Review', tauthor: true, noDetails: true })
    .then(function(result) {
      return result.notes;
    }).fail(function(error) {
      displayError();
      return null;
    });
};

// Render functions
var displayHeader = function(headerP) {
  var $panel = $('#group-container');
  $panel.hide('fast', function() {
    $panel.prepend('\
      <div id="header">\
        <h1>' + HEADER_TEXT + '</h1>\
        <div class="description">' + INSTRUCTIONS + '</div>\
      </div>\
      <div id="notes">\
        <div class="tabs-container"></div>\
      </div>'
    );

    var loadingMessage = '<p class="empty-message">Loading...</p>';
    //var noPapersMessage = '<p class="no-papers-message">You have no assigned papers. Please check again after the paper assignment process. </p>';
    var tabsData = {
      sections: [
        {
          heading: 'Assigned Papers',
          id: 'assigned-papers',
          content: loadingMessage,
          active: true
        },
        {
          heading: 'Reviewer Schedule',
          id: 'reviewer-schedule',
          content: SCHEDULE_HTML
        },
        {
          heading: 'Reviewer Tasks',
          id: 'reviewer-tasks',
          content: loadingMessage,
        }
      ]
    };
    $panel.find('.tabs-container').append(Handlebars.templates['components/tabs'](tabsData));

    $panel.show('fast', function() {
      headerP.resolve(true);
    });
  });
};

var displayStatusTable = function(profiles, fullNotes, completedRatings, officialReviews, reviewerIds, container, options) {
  if (Object.keys(reviewerIds).length){
    var rowData = _.map(fullNotes, function(note) {
      var revIds = reviewerIds[note.number];
      for (var revNumber in revIds) {
        var profile = findProfile(profiles, revIds[revNumber]);
        revIds[revNumber] = profile;
      }

      var officialReview = _.find(officialReviews, ['invitation', CONFERENCE + '/-/Paper' + note.number + '/Official_Review']);
      return buildTableRow(
        note, revIds, completedRatings[note.number], officialReview
      );
    });

    var tableHTML = Handlebars.templates['components/table']({
      //headings: ['#', 'Paper Summary', 'Status', 'Your Ratings'],
      headings: ['#', 'Paper Summary', 'Status'],
      rows: rowData,
      extraClasses: 'console-table'
    });

    $(container).empty().append(tableHTML);
  } else {
    $(container).empty().append('<p class="empty-message">You have no assigned papers. Please check again after the paper assignment process. ');
  }
};

var displayTasks = function(invitations, tagInvitations){
  console.log('displayTasks');
  //  My Tasks tab
  var tasksOptions = {
    container: '#reviewer-tasks',
    emptyMessage: 'No outstanding tasks for this conference'
  }
  $(tasksOptions.container).empty();

  // Filter out non-reviewer tasks
  var filterFunc = function(inv) {
    return _.some(inv.invitees, function(invitee) { return invitee.indexOf('Reviewer') !== -1; });
  };
  var reviewerInvitations = _.filter(invitations, filterFunc);
  var reviewerTagInvitations = _.filter(tagInvitations, filterFunc);

  Webfield.ui.newTaskList(reviewerInvitations, reviewerTagInvitations, tasksOptions)
  $('.tabs-container a[href="#reviewer-tasks"]').parent().show();
}

var displayError = function(message) {
  message = message || 'The group data could not be loaded.';
  $('#notes').empty().append('<div class="alert alert-danger"><strong>Error:</strong> ' + message + '</div>');
};


// Helper functions
var buildTableRow = function(note, reviewerIds, completedRatings, officialReview) {
  var number = '<strong class="note-number">' + note.number + '</strong>';

  // Build Note Summary Cell
  note.content.authors = null;  // Don't display 'Blinded Authors'
  //note.content.authorDomains = domains;
  var summaryHtml = Handlebars.templates.noteSummary(note);

  // Build Status Cell
  var invitationUrlParams = {
    id: note.forum,
    noteId: note.id,
    invitationId: CONFERENCE + '/-/Paper' + note.number + '/Official_Review'
  };
  var reviewStatus = {
    invitationUrl: '/forum?' + $.param(invitationUrlParams),
    invitationName: 'Official Review'
  };
  if (officialReview) {
    reviewStatus.paperRating = officialReview.content.rating;
    reviewStatus.review = officialReview.content.review;
    reviewStatus.editUrl = '/forum?id=' + note.forum + '&noteId=' + officialReview.id;
  }
  var statusHtml = Handlebars.templates.noteReviewStatus(reviewStatus);

  //return [number, summaryHtml, statusHtml, ratingHtml];
  return [number, summaryHtml, statusHtml];
};

var buildNoteMap = function(noteNumbers) {
  var noteMap = Object.create(null);
  for (var i = 0; i < noteNumbers.length; i++) {
    noteMap[noteNumbers[i]] = Object.create(null);
  }
  return noteMap;
};


// Kick the whole thing off
var headerLoaded = $.Deferred();
displayHeader(headerLoaded);

$.ajaxSetup({
  contentType: 'application/json; charset=utf-8'
});

var fetchedData = {};
controller.addHandler('reviewers', {
  token: function(token) {
    var pl = model.tokenPayload(token);
    var user = pl.user;

    var userReviewerGroupsP = $.getJSON('groups', { member: user.id, regex: CONFERENCE + '/Paper.*/AnonReviewer.*' })
      .then(function(result) {
        var noteNumbers = getPaperNumbersfromGroups(result.groups);
        return $.when(
          getFullNotes(noteNumbers),
          getReviewRatings(noteNumbers),
          getOfficialReviews(noteNumbers),
          getReviewerGroups(noteNumbers),
          Webfield.get('/invitations', {
            invitation: WILDCARD_INVITATION,
            invitee: true,
            duedate: true,
            replyto: true,
            details:'replytoNote,repliedNotes'
          }).then(function(result) {
            return result.invitations;
          }),
          Webfield.get('/invitations', {
            invitation: WILDCARD_INVITATION,
            invitee: true,
            duedate: true,
            tags: true,
            details:'repliedTags'
          }).then(function(result) {
            return result.invitations;
          }),
          headerLoaded
        );
      })
      .then(function(fullNotes, reviewRatings, officialReviews, noteToReviewerIds, invitations, tagInvitations, loaded) {
        var uniqueIds = _.uniq(_.reduce(noteToReviewerIds, function(result, idsObj, noteNum) {
          return result.concat(_.values(idsObj));
        }, []));

        return getUserProfiles(uniqueIds)
        .then(function(profiles) {
          fetchedData = {
            profiles: profiles,
            fullNotes: fullNotes,
            reviewRatings: reviewRatings,
            officialReviews: officialReviews,
            noteToReviewerIds: noteToReviewerIds,
            invitations: invitations,
            tagInvitations: tagInvitations
          }
          renderTable();
        });

      })
      .fail(function(error) {
        displayError();
      });
  }
});

var renderTable = function() {
  displayStatusTable(
    fetchedData.profiles,
    fetchedData.fullNotes,
    fetchedData.reviewRatings,
    fetchedData.officialReviews,
    _.cloneDeep(fetchedData.noteToReviewerIds), // Need to clone this dictionary because some values are missing after the first refresh
    '#assigned-papers'
  );

  displayTasks(fetchedData.invitations, fetchedData.tagInvitations);

  Webfield.ui.done();
}

$('#group-container').on('click', 'a.note-contents-toggle', function(e) {
  var hiddenText = 'Show paper details';
  var visibleText = 'Hide paper details';
  var updated = $(this).text() === hiddenText ? visibleText : hiddenText;
  $(this).text(updated);
});

$('#group-container').on('click', 'a.send-reminder-link', function(e) {
  var userId = $(this).data('userId');
  var forumUrl = $(this).data('forumUrl');
  var postData = {
    subject: SHORT_PHRASE + ' Reminder',
    message: 'This is a reminder to please submit your review for ' + SHORT_PHRASE + '. ' +
      'Click on the link below to go to the review page:\n\n' + location.origin + forumUrl + '\n\nThank you.',
    groups: [userId]
  };

  $.post('/mail', JSON.stringify(postData), function(result) {
    promptMessage('A reminder email has been sent to ' + view.prettyId(userId));
    //Save the timestamp in the local storage
    localStorage.setItem(forumUrl + '|' + userId, Date.now());
    renderTable();
  }, 'json').fail(function(error) {
    console.log(error);
    promptError('The reminder email could not be sent at this time');
  });
  return false;
});

OpenBanner.venueHomepageLink(CONFERENCE);