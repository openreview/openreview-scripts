
// Assumes the following pattern for meta reviews and official reviews:
// CONFERENCE + '/-/Paper' + number + '/Meta_Review'
// CONFERENCE + '/-/Paper' + number + '/Official_Review'

// Constants
var HEADER_TEXT = 'ICLR 2019 Reviewer Console';
var SHORT_PHRASE = 'ICLR 2019';
var INSTRUCTIONS =  '<p class="dark">This page provides information and status updates \
for ICLR 2019 reviewers. It will be regularly updated as the conference progresses, \
  so please check back frequently for news and other updates.</p>';

var SCHEDULE_HTML = '<h4>Registration Phase</h4>\
    <p>\
      <ul>\
        <li>Update your profile to include your most up-to-date information, including \
        work history and relations, to ensure proper conflict-of-interest detection \
        during the paper matching process.</li> \
      </ul>\
    </p>\
  <br>\
  <h4>Bidding Phase</h4>\
    <p>\
      <em><strong>Please note that the bidding has begun. You are requested to do the\
       following by Friday, October 5.</strong></em>:\
      <ul>\
        <li>Provide your reviewing preferences by bidding on papers using the Bidding \
        Interface.</li>\
        <li><strong><a href="/invitation?id=ICLR.cc/2019/Conference/-/Add_Bid">Go to \
        Bidding Interface</a></strong></li>\
      </ul>\
    </p>\
  <br>';


var CONFERENCE = 'ICLR.cc/2019/Conference';


var BLIND_SUBMISSION_ID = CONFERENCE + '/-/Blind_Submission';

var OFFICIAL_REVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Official_Review';
var METAREVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Meta_Review';
var WILDCARD_INVITATION = CONFERENCE + '/-/.*';


var ANONREVIEWER_WILDCARD = CONFERENCE + '/Paper.*/AnonReviewer.*';
var AREACHAIR_WILDCARD = CONFERENCE + '/Paper.*/Area_Chair.*';

var ANONREVIEWER_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/AnonReviewer(\d+)/;
var AREACHAIR_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/Area_Chair(\d+)/;

// Ajax functions
var getPaperNumbersfromGroups = function(groups) {
  return _.map(
    _.filter(groups, function(g) { return ANONREVIEWER_REGEX.test(g.id); }),
    function(fg) { return parseInt(fg.id.match(ANONREVIEWER_REGEX)[1], 10); }
  );
};

var getBlindedNotes = function(noteNumbers) {
  var noteNumbersStr = noteNumbers.join(',');

  return $.getJSON('notes', { invitation: CONFERENCE + '/-/Blind_Submission', number: noteNumbersStr, noDetails: true })
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

  getPromise(0, 2000);

};

var getReviewRatings = function(noteNumbers) {
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

var getOfficialReviews = function() {
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
      <div id="header" class="panel">\
        <h1>' + HEADER_TEXT + '</h1>\
        <p class="description">' + INSTRUCTIONS + '</p>\
      </div>\
      <div id="notes">\
        <div class="tabs-container"></div>\
      </div>'
    );

    var loadingMessage = '<p class="empty-message">Loading...</p>';
    var tabsData = {
      sections: [
        {
          heading: 'Reviewer Schedule',
          id: 'reviewer-schedule',
          content: SCHEDULE_HTML,
          active: true
        },
        {
          heading: 'Reviewer Tasks',
          id: 'reviewer-tasks',
          content: loadingMessage,
        },
        {
          heading: 'Assigned Papers',
          id: 'assigned-papers',
          content: loadingMessage
        }
      ]
    };
    $panel.find('.tabs-container').append(Handlebars.templates['components/tabs'](tabsData));

    $panel.show('fast', function() {
      headerP.resolve(true);
    });
  });
};

var displayStatusTable = function(profiles, notes, completedRatings, officialReviews, reviewerIds, container, options) {
  console.log('reviewerIds', reviewerIds);
  if (Object.keys(reviewerIds).length){
    console.log('Object.keys(reviewerIds).length', Object.keys(reviewerIds).length);
    var rowData = _.map(notes, function(note) {
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

  // Build Review Progress Cell
  // var reviewObj;
  // var combinedObj = {};
  // var ratings = [];
  // var confidences = [];
  // for (var reviewerNum in reviewerIds) {
  //   var reviewer = reviewerIds[reviewerNum];
  //   if (reviewerNum in completedRatings) {
  //     reviewObj = completedRatings[reviewerNum];
  //     combinedObj[reviewerNum] = {
  //       id: reviewer.id,
  //       name: reviewer.name,
  //       email: reviewer.email,
  //       completedReview: true,
  //       forum: reviewObj.forum,
  //       note: reviewObj.id,
  //       rating: reviewObj.rating,
  //       confidence: reviewObj.confidence,
  //       reviewLength: reviewObj.content.review.length
  //     };
  //     ratings.push(reviewObj.rating);
  //     confidences.push(reviewObj.confidence);
  //   } else {
  //     var forumUrl = '/forum?' + $.param({
  //       id: note.forum,
  //       noteId: note.id,
  //       invitationId: CONFERENCE + '/-/Paper' + note.number + '/Official_Review'
  //     });
  //     var lastReminderSent = localStorage.getItem(forumUrl + '|' + reviewer.id);
  //     combinedObj[reviewerNum] = {
  //       id: reviewer.id,
  //       name: reviewer.name,
  //       email: reviewer.email,
  //       forumUrl: forumUrl,
  //       lastReminderSent: lastReminderSent ? new Date(parseInt(lastReminderSent)).toLocaleDateString('en-GB') : lastReminderSent
  //     };
  //   }
  // }
  // var averageRating = 'N/A';
  // var minRating = 'N/A';
  // var maxRating = 'N/A';
  // if (ratings.length) {
  //   averageRating = _.round(_.sum(ratings) / ratings.length, 2);
  //   minRating = _.min(ratings);
  //   maxRating = _.max(ratings);
  // }

  // var averageConfidence = 'N/A';
  // var minConfidence = 'N/A';
  // var maxConfidence = 'N/A';
  // if (confidences.length) {
  //   averageConfidence = _.round(_.sum(confidences) / confidences.length, 2);
  //   minConfidence = _.min(confidences);
  //   maxConfidence = _.max(confidences);
  // }

  // console.log('combinedObj', combinedObj);
  // console.log('reviewerIds', reviewerIds);
  // var ratingProgressData = {
  //   numSubmittedReviews: Object.keys(completedRatings).length,
  //   numReviewers: Object.keys(reviewerIds).length,
  //   reviewers: combinedObj,
  //   averageRating: averageRating,
  //   maxRating: maxRating,
  //   minRating: minRating,
  //   averageConfidence: averageConfidence,
  //   minConfidence: minConfidence,
  //   maxConfidence: maxConfidence,
  //   sendReminder: true
  // };
  // var ratingHtml = Handlebars.templates.noteRatings(ratingProgressData);

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
    console.log('officialReview detected', officialReview);
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
        console.log('noteNumbers', noteNumbers);
        return $.when(
          getBlindedNotes(noteNumbers),
          getReviewRatings(noteNumbers),
          getOfficialReviews(),
          getReviewerGroups(noteNumbers),
          Webfield.get('/invitations', {
            invitation: WILDCARD_INVITATION,
            pageSize: 100,
            invitee: true,
            duedate: true,
            replyto: true,
            details:'replytoNote,repliedNotes'
          }).then(function(result) {
            return result.invitations;
          }),
          Webfield.api.getTagInvitations(BLIND_SUBMISSION_ID),
          headerLoaded
        );
      })
      .then(function(blindedNotes, reviewRatings, officialReviews, noteToReviewerIds, invitations, tagInvitations, loaded) {
        console.log('blindedNotes', blindedNotes);
        console.log('reviewRatings', reviewRatings);
        console.log('noteToReviewerIds', noteToReviewerIds);
        console.log('invitations', invitations);
        console.log('tagInvitations', tagInvitations);
        var uniqueIds = _.uniq(_.reduce(noteToReviewerIds, function(result, idsObj, noteNum) {
          return result.concat(_.values(idsObj));
        }, []));

        return getUserProfiles(uniqueIds)
        .then(function(profiles) {
          fetchedData = {
            profiles: profiles,
            blindedNotes: blindedNotes,
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
    fetchedData.blindedNotes,
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
