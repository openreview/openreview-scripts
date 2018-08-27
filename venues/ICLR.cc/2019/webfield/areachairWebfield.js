
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

var INSTRUCTIONS = '<p class="dark">This page provides information and status \
  updates for ICLR 2019 Area Chairs. It will be regularly updated as the conference \
  progresses, so please check back frequently for news and other updates.</p>';
var SCHEDULE_HTML = '<h4>Registration Phase</h4>\
  <p>\
    <em><strong>Please do the following by Friday, August 10</strong></em>:\
    <ul>\
      <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>\
      <li>Complete the ICLR registration form (found in your Tasks view).</li>\
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
  </p>';

// Main function is the entry point to the webfield code
var main = function() {
  OpenBanner.venueHomepageLink(CONFERENCE);

  renderHeader();

  Webfield.get('/groups', {
    member: user.id, regex: CONFERENCE + '/Paper.*/Area_Chair.*'
  })
  .then(loadData)
  .then(formatData)
  .then(renderTableAndTasks)
  .fail(function() {
    Webfield.ui.errorMessage();
  });
};


// Util functions
var getPaperNumbersfromGroups = function(groups) {
  return _.map(
    _.filter(groups, function(g) { return AREACHAIR_REGEX.test(g.id); }),
    function(fg) { return parseInt(fg.id.match(AREACHAIR_REGEX)[1], 10); }
  );
};

var buildNoteMap = function(noteNumbers) {
  var noteMap = Object.create(null);
  for (var i = 0; i < noteNumbers.length; i++) {
    noteMap[noteNumbers[i]] = Object.create(null);
  }
  return noteMap;
};


// Ajax functions
var loadData = function(result) {
  var noteNumbers = getPaperNumbersfromGroups(result.groups);
  var noteNumbersStr = noteNumbers.join(',');

  var blindedNotesP = Webfield.get('/notes', {
    invitation: BLIND_SUBMISSION_ID, number: noteNumbersStr, noDetails: true
  })
  .then(function(result) {
    return result.notes;
  });

  var metaReviewsP = Webfield.get('/notes', {
    invitation: CONFERENCE + '/-/Paper.*/Meta_Review', noDetails: true
  })
  .then(function(result) {
    return result.notes;
  });

  var invitationsP = Webfield.get('/invitations', {
    invitation: WILDCARD_INVITATION, pageSize: 100, invitee: true,
    duedate: true, replyto: true, details: 'replytoNote,repliedNotes'
  })
  .then(function(result) {
    return result.invitations;
  });

  var tagInvitationsP = Webfield.api.getTagInvitations(BLIND_SUBMISSION_ID);

  return $.when(
    blindedNotesP,
    getOfficialReviews(noteNumbers),
    metaReviewsP,
    getReviewerGroups(noteNumbers),
    invitationsP,
    tagInvitationsP
  );
};

var getOfficialReviews = function(noteNumbers) {
  var noteMap = buildNoteMap(noteNumbers);

  return Webfield.getAll('/notes', {
    invitation: OFFICIAL_REVIEW_INVITATION, noDetails: true
  })
  .then(function(notes) {
    var ratingExp = /^(\d+): .*/;

    _.forEach(notes, function(n) {
      var num, index, ratingMatch;
      var matches = n.signatures[0].match(ANONREVIEWER_REGEX);
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

    return noteMap;
  });
};

var getReviewerGroups = function(noteNumbers) {
  var noteMap = buildNoteMap(noteNumbers);

  return Webfield.get('/groups', { id: ANONREVIEWER_WILDCARD })
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
  });

};

var formatData = function(blindedNotes, officialReviews, metaReviews, noteToReviewerIds, invitations, tagInvitations) {
  var uniqueIds = _.uniq(_.reduce(noteToReviewerIds, function(result, idsObj, noteNum) {
    return result.concat(_.values(idsObj));
  }, []));

  return getUserProfiles(uniqueIds)
  .then(function(profiles) {
    return {
      profiles: profiles,
      blindedNotes: blindedNotes,
      officialReviews: officialReviews,
      metaReviews: metaReviews,
      noteToReviewerIds: noteToReviewerIds,
      invitations: invitations,
      tagInvitations: tagInvitations
    };
  });
};

var getUserProfiles = function(userIds) {
  var profileMap = {};

  return Webfield.post('/user/profiles', { ids: userIds })
  .then(function(result) {
    _.forEach(result.profiles, function(profile) {
      var name = _.find(profile.content.names, ['preferred', true]) || _.first(profile.content.names);
      profile.name = _.isEmpty(name) ? view.prettyId(profile.id) : name.first + ' ' + name.last;
      profile.email = profile.content.preferredEmail;
      profileMap[profile.id] = profile;
    });

    return profileMap;
  });
};


// Render functions
var renderHeader = function() {
  Webfield.ui.setup('#group-container', CONFERENCE);
  Webfield.ui.header(HEADER_TEXT, INSTRUCTIONS);

  var loadingMessage = '<p class="empty-message">Loading...</p>';
  Webfield.ui.tabPanel([
    {
      heading: 'Area Chair Schedule',
      id: 'areachair-schedule',
      content: SCHEDULE_HTML,
      active: true
    },
    {
      heading: 'Area Chair Tasks',
      id: 'areachair-tasks',
      content: loadingMessage,
    },
    {
      heading: 'Assigned Papers',
      id: 'assigned-papers',
      content: loadingMessage
    }
  ]);
};

var renderStatusTable = function(profiles, notes, completedReviews, metaReviews, reviewerIds, container) {
  var rows = _.map(notes, function(note) {
    var revIds = reviewerIds[note.number];
    for (var revNumber in revIds) {
      var uId = revIds[revNumber];
      revIds[revNumber] = _.get(profiles, uId, { id: uId, name: '', email: uId });
    }

    var metaReview = _.find(metaReviews, ['invitation', CONFERENCE + '/-/Paper' + note.number + '/Meta_Review']);

    return buildTableRow(
      note, revIds, completedReviews[note.number], metaReview
    );
  });

  var order = 'desc';
  var sortOptions = {
    Paper_Number: function(row) { return row[0].number; },
    Paper_Title: function(row) { return _.toLower(row[1].content.title); },
    Reviews_Submitted: function(row) { return row[2].numSubmittedReviews; },
    Reviews_Missing: function(row) { return row[2].numReviewers - row[2].numSubmittedReviews; },
    Average_Rating: function(row) { return row[3].averageRating === 'N/A' ? 0 : row[3].averageRating; },
    Max_Rating: function(row) { return row[3].maxRating === 'N/A' ? 0 : row[3].maxRating; },
    Min_Rating: function(row) { return row[3].minRating === 'N/A' ? 0 : row[3].minRating; },
    Average_Confidence: function(row) { return row[4].averageConfidence === 'N/A' ? 0 : row[4].averageConfidence; },
    Max_Confidence: function(row) { return row[4].maxConfidence === 'N/A' ? 0 : row[4].maxConfidence; },
    Min_Confidence: function(row) { return row[4].minConfidence === 'N/A' ? 0 : row[4].minConfidence; },
    Meta_Review_Missing: function(row) { return row[5].rating ? 1 : 0; }
  };
  var sortResults = function(newOption, switchOrder) {
    if (switchOrder) {
      order = (order == 'asc' ? 'desc' : 'asc');
    }

    var selectedOption = newOption;
    renderTableRows(_.orderBy(rows, sortOptions[selectedOption], order), container);
  }

  var sortOptionHtml = Object.keys(sortOptions).map(function(option) {
    return '<option value="' + option + '">' + option.replace(/_/g, ' ') + '</option>';
  }).join('\n');

  var sortBarHtml = '<form class="form-inline search-form clearfix" role="search">' +
    '<strong>Sort By:</strong> ' +
    '<select id="form-sort" class="form-control">' + sortOptionHtml + '</select>' +
    '<button id="form-order" class="btn btn-icon"><span class="glyphicon glyphicon-sort"></span></button>' +
    '<div class="pull-right">' +
      '<button id="message-reviewers" class="btn btn-icon"><span class="glyphicon glyphicon-envelope"></span> &nbsp;Message Reviewers</button>' +
    '</div>' +
    '</form>';
  $(container).empty().append(sortBarHtml);

  $('#form-sort').on('change', function(e) {
    sortResults($(e.target).val(), false);
  });
  $('#form-order').on('click', function(e) {
    sortResults($(this).prev().val(), true);
    return false;
  });

  renderTableRows(rows, container);
};

var renderTableRows = function(rows, container) {
  var templateFuncs = [
    function(data) {
      return '<strong class="note-number">' + data.number + '</strong>';
    },
    Handlebars.templates.noteSummary,
    Handlebars.templates.noteReviewers,
    function(data) {
      return '<h4>Avg: ' + data.averageRating + '</h4><span>Min: ' + data.minRating + '</span>' +
        '<br><span>Max: ' + data.maxRating + '</span>';
    },
    function(data) {
      return '<h4>Avg: ' + data.averageConfidence + '</h4><span>Min: ' + data.minConfidence + '</span>' +
      '<br><span>Max: ' + data.maxConfidence + '</span>';
    },
    Handlebars.templates.noteMetaReviewStatus
  ];

  var rowsHtml = rows.map(function(row) {
    return row.map(function(cell, i) {
      return templateFuncs[i](cell);
    });
  });

  var tableHtml = Handlebars.templates['components/table']({
    headings: ['#', 'Paper Summary', 'Review Progress', 'Rating', 'Confidence', 'Status'],
    rows: rowsHtml,
    extraClasses: 'ac-console-table'
  });

  $('.table-responsive', container).remove();
  $(container).append(tableHtml);
}

var renderTasks = function(invitations, tagInvitations) {
  //  My Tasks tab
  var tasksOptions = {
    container: '#areachair-tasks',
    emptyMessage: 'No outstanding tasks for this conference'
  }
  $(tasksOptions.container).empty();

  // filter out non-areachair tasks
  areachairInvitations = _.filter(invitations, inv => {
    if ( _.some(inv.invitees, invitee => _.includes(invitee, 'Area_Chair')) ) {
      return inv;
    }
  });

  areachairTagInvitations = _.filter(tagInvitations, inv => {
    if ( _.some(inv.invitees, invitee => _.includes(invitee, 'Area_Chair')) ) {
      return inv;
    }
  });

  Webfield.ui.newTaskList(invitations, tagInvitations, tasksOptions);
  $('.tabs-container a[href="#areachair-tasks"]').parent().show();
}

var renderTableAndTasks = function(fetchedData) {
  renderTasks(fetchedData.invitations, fetchedData.tagInvitations);

  renderStatusTable(
    fetchedData.profiles,
    fetchedData.blindedNotes,
    fetchedData.officialReviews,
    fetchedData.metaReviews,
    _.cloneDeep(fetchedData.noteToReviewerIds), // Need to clone this dictionary because some values are missing after the first refresh
    '#assigned-papers'
  );

  registerEventHandlers();

  Webfield.ui.done();
}

var buildTableRow = function(note, reviewerIds, completedReviews, metaReview) {
  // Paper number cell
  var cell0 = { number: note.number};

  // Note summary cell
  note.content.authors = null;  // Don't display 'Blinded Authors'
  var cell1 = note;

  // Review progress cell
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

  var cell2 = {
    noteId: note.id,
    numSubmittedReviews: Object.keys(completedReviews).length,
    numReviewers: Object.keys(reviewerIds).length,
    reviewers: combinedObj,
    sendReminder: true
  };

  // Rating cell
  var cell3 = {
    averageRating: 'N/A',
    minRating: 'N/A',
    maxRating: 'N/A'
  };
  if (ratings.length) {
    cell3.averageRating = _.round(_.sum(ratings) / ratings.length, 2);
    cell3.minRating = _.min(ratings);
    cell3.maxRating = _.max(ratings);
  }

  // Confidence cell
  var cell4 = {
    averageConfidence: 'N/A',
    minConfidence: 'N/A',
    maxConfidence: 'N/A'
  };
  if (confidences.length) {
    cell4.averageConfidence = _.round(_.sum(confidences) / confidences.length, 2);
    cell4.minConfidence = _.min(confidences);
    cell4.maxConfidence = _.max(confidences);
  }

  // Status cell
  var invitationUrlParams = {
    id: note.forum,
    noteId: note.id,
    invitationId: CONFERENCE + '/-/Paper' + note.number + '/Meta_Review'
  };
  var cell5 = {
    invitationUrl: '/forum?' + $.param(invitationUrlParams)
  };
  if (metaReview) {
    cell5.recommendation = metaReview.content.rating;
    cell5.editUrl = '/forum?id=' + note.forum + '&noteId=' + metaReview.id;
  }

  return [cell0, cell1, cell2, cell3, cell4, cell5];
};


// Event Handlers
var registerEventHandlers = function() {
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
      // Save the timestamp in the local storage
      localStorage.setItem(forumUrl + '|' + userId, Date.now());
    }, 'json').fail(function(error) {
      console.log(error);
      promptError('The reminder email could not be sent at this time');
    });

    return false;
  });

  $('a.collapse-btn').on('click', function(e) {
    console.log('here');
    $(this).next().slideToggle();
    if ($(this).text() === 'Show reviewers') {
      $(this).text('Hide reviewers');
    } else {
      $(this).text('Show reviewers');
    }
    return false;
  });
};

main();
