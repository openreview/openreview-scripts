
// Assumes the following pattern for meta reviews and official reviews:
// CONFERENCE + '/-/Paper' + number + '/Meta_Review'
// CONFERENCE + '/-/Paper' + number + '/Official_Review'

// Constants
var HEADER_TEXT = 'Area Chair Console';
var SHORT_PHRASE = 'ICLR 2019';
var CONFERENCE = 'ICLR.cc/2019/Conference';

var BLIND_SUBMISSION_ID = CONFERENCE + '/-/Blind_Submission';

var OFFICIAL_REVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Official_Review';
var METAREVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Meta_Review';
var WILDCARD_INVITATION = CONFERENCE + '/-/.*';

var ANONREVIEWER_WILDCARD = CONFERENCE + '/Paper.*/AnonReviewer.*';
var AREACHAIR_WILDCARD = CONFERENCE + '/Paper.*/Area_Chair.*';

var ANONREVIEWER_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/AnonReviewer(\d+)/;
var AREACHAIR_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/Area_Chair(\d+)/;

var INSTRUCTIONS =  '<p><strong>This page provides information and status updates for ICLR 2019 Area Chairs. It will be regularly updated as the conference progresses, so please check back frequently for news and other updates.</strong></p>\
  <br>'

var SCHEDULE_HTML = '<h4>Registration Phase</h4>\
    <p>\
      <em><strong>Please do the following by Friday, August 10</strong></em>:\
      <ul>\
        <li>Register as an Official Reviewer by <strong>(1)</strong> updating your profile to include your most up-to-date information, and <strong>(2)</strong> submitting ICLR Subject Areas and Data Collection consent forms.</li>\
        <li><strong><a href="/forum?id=ryxFlFHvSQ">Complete Reviewer Registration</a></strong></li>\
      </ul>\
    </p>\
  <br>\
  <h4>Bidding Phase</h4>\
    <p>\
      <em><strong>Please do the following by Friday, August 17</strong></em>:\
      <ul>\
        <li>Provide your reviewing preferences by bidding on papers using the Bidding Interface.</li>\
        <li><strong><a href="/invitation?id=ICLR.cc/2019/Conference/-/Add_Bid">Go to Bidding Interface</a></strong></li>\
      </ul>\
    </p>\
  <br>'

// Ajax functions
var getPaperNumbersfromGroups = function(groups) {
  return _.map(
    _.filter(groups, function(g) { return AREACHAIR_REGEX.test(g.id); }),
    function(fg) { return parseInt(fg.id.match(AREACHAIR_REGEX)[1], 10); }
  );
};

var getBlindedNotes = function(noteNumbers) {
  var noteNumbersStr = noteNumbers.join(',');

  return $.getJSON('notes', { invitation: CONFERENCE + '/-/Blind_Submission', number: noteNumbersStr, noDetails: true })
    .then(function(result) {
      return result.notes;
    });
};

var getAllReviews = function(callback) {
  var invitationId = CONFERENCE + '/-/Paper.*/Official_Review';
  var allNotes = [];

  function getPromise(offset, limit) {
    return $.getJSON('notes', { invitation: CONFERENCE + '/-/Paper.*/Official_Review', offset: offset, limit: limit, noDetails: true })
    .then(function(result) {
      allNotes = _.union(allNotes, result.notes);
      if (result.notes.length == limit) {
        return getPromise(offset + limit, limit);
      } else {
        callback(allNotes);
      }
    });
  };

  getPromise(0, 2000);

};

var getOfficialReviews = function(noteNumbers) {

  var dfd = $.Deferred();

  var noteMap = buildNoteMap(noteNumbers);

  getAllReviews(function(notes) {
    var ratingExp = /^(\d+): .*/;

    _.forEach(notes, function(n) {
      var matches = n.signatures[0].match(ANONREVIEWER_REGEX);
      var num, index, ratingMatch;
      if (matches) {
        num = parseInt(matches[1], 10);
        index = parseInt(matches[2], 10);

        if (num in noteMap) {
          // Need to parse rating and confidence strings into ints
          ratingMatch = n.content.rating.match(ratingExp);
          n.rating = ratingMatch ? parseInt(ratingMatch[1], 10) : null;
          confidenceMatch = n.content.confidence.match(ratingExp);
          n.confidence = confidenceMatch ? parseInt(confidenceMatch[1], 10) : null;

          noteMap[num][index] = n;
        }
      }
    });
    dfd.resolve(noteMap);

  });

  return dfd.promise();

};

var getReviewerGroups = function(noteNumbers) {
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

var getMetaReviews = function() {
  return $.getJSON('notes', { invitation: CONFERENCE + '/-/Paper.*/Meta_Review', noDetails: true })
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
    $panel.empty().append(
      '<div id="header" class="panel">' +
        '<h1>' + HEADER_TEXT + '</h1>' +
      '</div>\
      <div class="description">' + INSTRUCTIONS + '</div>\
      <div id="notes">\
        <div class="tabs-container"></div>\
      </div>'
    );

    var loadingMessage = '<p class="empty-message">Loading...</p>';
    var tabsData = {
      sections: [
        {
          heading: 'Area Chair Schedule',
          id: 'areachair-schedule',
          content: SCHEDULE_HTML,
          active: true
        },
        {
          heading: 'Area Chair Tasks',
          id: 'your-iclr-tasks',
          content: loadingMessage,
        },
        {
          heading: 'Assigned Papers',
          id: 'assigned-papers',
          content: loadingMessage
        },
      ]
    };
    $panel.find('.tabs-container').append(Handlebars.templates['components/tabs'](tabsData));

    $panel.show('fast', function() {
      headerP.resolve(true);
    });
  });
};

var displayStatusTable = function(profiles, notes, completedReviews, metaReviews, reviewerIds, container, options) {
  console.log('displayStatusTable')
  console.log('profiles', profiles);
  var rowData = _.map(notes, function(note) {
    var revIds = reviewerIds[note.number];
    for (var revNumber in revIds) {
      var profile = findProfile(profiles, revIds[revNumber]);
      revIds[revNumber] = profile;
    }

    var metaReview = _.find(metaReviews, ['invitation', CONFERENCE + '/-/Paper' + note.number + '/Meta_Review']);
    return buildTableRow(
      note, revIds, completedReviews[note.number], metaReview
    );
  });

  var tableHTML = Handlebars.templates['components/table']({
    headings: ['#', 'Paper Summary', 'Review Progress', 'Status'],
    rows: rowData,
    extraClasses: 'console-table'
  });

  $(container).empty().append(tableHTML);
};

var displayTasks = function(assignedNotePairs, tagInvitations){
  console.log('displayTasks');
  //  My Tasks tab
  var tasksOptions = {
    container: '#your-iclr-tasks',
    emptyMessage: 'No outstanding tasks for this conference'
  }
  $(tasksOptions.container).empty();
  console.log('assignedNotePairs', assignedNotePairs);
  Webfield.ui.taskList(assignedNotePairs, tagInvitations, tasksOptions)
  $('.tabs-container a[href="#your-iclr-tasks"]').parent().show();
}

var displayError = function(message) {
  message = message || 'The group data could not be loaded.';
  $('#notes').empty().append('<div class="alert alert-danger"><strong>Error:</strong> ' + message + '</div>');
};


// Helper functions
var buildTableRow = function(note, reviewerIds, completedReviews, metaReview) {
  var number = '<strong class="note-number">' + note.number + '</strong>';

  // Build Note Summary Cell
  note.content.authors = null;  // Don't display 'Blinded Authors'
  //note.content.authorDomains = domains;
  var summaryHtml = Handlebars.templates.noteSummary(note);

  // Build Review Progress Cell
  var reviewObj;
  var combinedObj = {};
  var ratings = [];
  var confidences = [];
  for (var reviewerNum in reviewerIds) {
    var reviewer = reviewerIds[reviewerNum];
    if (reviewerNum in completedReviews) {
      reviewObj = completedReviews[reviewerNum];
      combinedObj[reviewerNum] = {
        id: reviewer.id,
        name: reviewer.name,
        email: reviewer.email,
        completedReview: true,
        forum: reviewObj.forum,
        note: reviewObj.id,
        rating: reviewObj.rating,
        confidence: reviewObj.confidence,
        reviewLength: reviewObj.content.review.length
      };
      ratings.push(reviewObj.rating);
      confidences.push(reviewObj.confidence);
    } else {
      var forumUrl = '/forum?' + $.param({
        id: note.forum,
        noteId: note.id,
        invitationId: CONFERENCE + '/-/Paper' + note.number + '/Official_Review'
      });
      var lastReminderSent = localStorage.getItem(forumUrl + '|' + reviewer.id);
      combinedObj[reviewerNum] = {
        id: reviewer.id,
        name: reviewer.name,
        email: reviewer.email,
        forumUrl: forumUrl,
        lastReminderSent: lastReminderSent ? new Date(parseInt(lastReminderSent)).toLocaleDateString('en-GB') : lastReminderSent
      };
    }
  }
  var averageRating = 'N/A';
  var minRating = 'N/A';
  var maxRating = 'N/A';
  if (ratings.length) {
    averageRating = _.round(_.sum(ratings) / ratings.length, 2);
    minRating = _.min(ratings);
    maxRating = _.max(ratings);
  }

  var averageConfidence = 'N/A';
  var minConfidence = 'N/A';
  var maxConfidence = 'N/A';
  if (confidences.length) {
    averageConfidence = _.round(_.sum(confidences) / confidences.length, 2);
    minConfidence = _.min(confidences);
    maxConfidence = _.max(confidences);
  }

  console.log('combinedObj', combinedObj);
  console.log('reviewerIds', reviewerIds);
  var reviewProgressData = {
    numSubmittedReviews: Object.keys(completedReviews).length,
    numReviewers: Object.keys(reviewerIds).length,
    reviewers: combinedObj,
    averageRating: averageRating,
    maxRating: maxRating,
    minRating: minRating,
    averageConfidence: averageConfidence,
    minConfidence: minConfidence,
    maxConfidence: maxConfidence,
    sendReminder: true
  };
  var reviewHtml = Handlebars.templates.noteReviewers(reviewProgressData);

  // Build Status Cell
  var invitationUrlParams = {
    id: note.forum,
    noteId: note.id,
    invitationId: CONFERENCE + '/-/Paper' + note.number + '/Meta_Review'
  };
  var reviewStatus = {
    invitationUrl: '/forum?' + $.param(invitationUrlParams)
  };
  if (metaReview) {
    reviewStatus.recommendation = metaReview.content.recommendation;
    reviewStatus.editUrl = '/forum?id=' + note.forum + '&noteId=' + metaReview.id;
  }
  var statusHtml = Handlebars.templates.noteMetaReviewStatus(reviewStatus);

  return [number, summaryHtml, reviewHtml, statusHtml];
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
controller.addHandler('areachairs', {
  token: function(token) {
    var pl = model.tokenPayload(token);
    var user = pl.user;

    var userAreachairGroupsP = $.getJSON('groups', { member: user.id, regex: CONFERENCE + '/Paper.*/Area_Chair.*' })
      .then(function(result) {
        var noteNumbers = getPaperNumbersfromGroups(result.groups);
        console.log('noteNumbers', noteNumbers);
        return $.when(
          getBlindedNotes(noteNumbers),
          getOfficialReviews(noteNumbers),
          getMetaReviews(),
          getReviewerGroups(noteNumbers),
          Webfield.api.getSubmissions(WILDCARD_INVITATION, {
            pageSize: 100,
            invitee: true,
            duedate: true,
            // replyto: true,
            details:'replytoNote,repliedNotes'
          }),
          Webfield.api.getTagInvitations(BLIND_SUBMISSION_ID),
          headerLoaded
        );
      })
      .then(function(blindedNotes, officialReviews, metaReviews, noteToReviewerIds, assignedNotePairs, tagInvitations, loaded, authorDomains) {
        console.log('blindedNotes', blindedNotes);
        console.log('noteToReviewerIds', noteToReviewerIds);
        var uniqueIds = _.uniq(_.reduce(noteToReviewerIds, function(result, idsObj, noteNum) {
          return result.concat(_.values(idsObj));
        }, []));

        return getUserProfiles(uniqueIds)
        .then(function(profiles) {
          fetchedData = {
            profiles: profiles,
            blindedNotes: blindedNotes,
            officialReviews: officialReviews,
            metaReviews: metaReviews,
            noteToReviewerIds: noteToReviewerIds,
            authorDomains: authorDomains,
            assignedNotePairs: assignedNotePairs,
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
    fetchedData.blindedNotes,
    fetchedData.officialReviews,
    fetchedData.metaReviews,
    _.cloneDeep(fetchedData.noteToReviewerIds), // Need to clone this dictionary because some values are missing after the first refresh
    //fetchedData.authorDomains,
    '#assigned-papers'
  );

  displayTasks(fetchedData.assignedNotePairs, fetchedData.tagInvitations);
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

OpenBanner.breadcrumbs([
  { link: '/', text: 'Venues' },
  { link: '/group?id=' + CONFERENCE, text: view.prettyId(CONFERENCE) }
]);
