
// Assumes the following pattern for meta reviews and official reviews:
// CONFERENCE + '/-/Paper' + number + '/Meta_Review'
// CONFERENCE + '/-/Paper' + number + '/Official_Review'

// Constants
var HEADER_TEXT = 'Program Committee Console';
var SHORT_PHRASE = 'COLT 2019';
var CONFERENCE = 'learningtheory.org/COLT/2019/Conference';

var BLIND_SUBMISSION_ID = CONFERENCE + '/-/Blind_Submission';

var OFFICIAL_REVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Official_Review';
var METAREVIEW_INVITATION = CONFERENCE + '/-/Paper.*/Meta_Review';
var WILDCARD_INVITATION = CONFERENCE + '/-/.*';

var ANONREVIEWER_WILDCARD = CONFERENCE + '/Paper.*/Program_Committee.*/Reviewer.*';
var AREACHAIR_WILDCARD = CONFERENCE + '/Paper.*/Program_Committee.*';

var ANONREVIEWER_REGEX = /^learningtheory\.org\/COLT\/2019\/Conference\/Paper(\d+)\/AnonReviewer(\d+)/;
var AREACHAIR_REGEX = /^learningtheory\.org\/COLT\/2019\/Conference\/Paper(\d+)\/Program_Committee_Member(\d+)/;
var REVIEWER_REGEX = /^learningtheory\.org\/COLT\/2019\/Conference\/Paper(\d+)\/Program_Committee_Member(\d+)\/Reviewers$/;
var REVIEWER_INVITED_REGEX = /^learningtheory\.org\/COLT\/2019\/Conference\/Paper(\d+)\/Program_Committee_Member(\d+)\/Reviewers_Invited$/;
var REVIEWER_DECLINED_REGEX = /^learningtheory\.org\/COLT\/2019\/Conference\/Paper(\d+)\/Program_Committee_Member(\d+)\/Reviewers_Declined$/;

var INSTRUCTIONS = '<p class="dark">\
  This page provides information and status \
  updates for COLT 2019 Program Committee. It will be regularly updated as the conference \
  progresses, so please check back frequently for news and other updates.\
  </p>\
  <p class="dark">\
  <strong>Instructions for Managing Subreviewers:</strong>\
  <ul>\
  <li>Enter the email address of a subreviewer that you would like to invite to review a paper.</li>\
  <li>Click the "Invite" button to send the invitation email to that subreviewer.</li>\
  <li>Once the reviewer has been invited, their email address and response status will appear below the invitation box.</li>\
  <li>It may take some time for the Review Progress column to update with the correct total number of reviewers (this is normal).</li>\
  <li>This subreviewer management interface is a prototype system. If you have any issues or questions, please contact info@openreview.net as soon as possible.</li>\
  </ul>\
  </p>';

var SCHEDULE_HTML = '<h4>Registration Phase</h4>\
  <p>\
    <ul>\
      <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>\
    </ul>\
  </p>\
  <br>\
  <h4>Bidding Phase</h4>\
  <p>\
    <em><strong>Please note that bidding is now open. You are requested to do the\
     following by 5:00 PM EDT, February 6, 2019</strong></em>:\
    <ul>\
      <li>Provide your reviewing preferences by bidding on papers using the Bidding \
      Interface.</li>\
      <li><strong><a href="/invitation?id=' + CONFERENCE + '/-/Bid' + '">Go to \
      Bidding Interface</a></strong></li>\
    </ul>\
  </p>';



var invitedMap = {};

// Main function is the entry point to the webfield code
var main = function() {
  OpenBanner.venueHomepageLink(CONFERENCE);

  renderHeader();

  Webfield.get('/groups', {
    member: user.id, regex: CONFERENCE + '/Paper.*/Program_Committee_Member.*'
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
    invitedMap[noteNumbers[i]] = {
      accepted: [],
      invited: [],
      declined: []
    };
  }
  return noteMap;
};


// Ajax functions
var loadData = function(result) {
  var noteNumbers = getPaperNumbersfromGroups(result.groups);
  var individualGroupIds = _.map(result.groups, function(g) { return g.id; });
  var blindedNotesP;
  var metaReviewsP;

  if (noteNumbers.length) {
    var noteNumbersStr = noteNumbers.join(',');

    blindedNotesP = Webfield.getAll('/notes', {
      invitation: BLIND_SUBMISSION_ID, number: noteNumbersStr, noDetails: true
    });

    metaReviewsP = Webfield.getAll('/notes', {
      invitation: CONFERENCE + '/-/Paper.*/Meta_Review', noDetails: true
    });
  } else {
    blindedNotesP = $.Deferred().resolve([]);
    metaReviewsP = $.Deferred().resolve([]);
  }

  var invitationsP = Webfield.getAll('/invitations', {
    invitation: WILDCARD_INVITATION, invitee: true,
    duedate: true, replyto: true, details: 'replytoNote,repliedNotes'
  });

  var tagInvitationsP = Webfield.api.getTagInvitations(BLIND_SUBMISSION_ID);

  return $.when(
    individualGroupIds,
    blindedNotesP,
    getOfficialReviews(noteNumbers),
    metaReviewsP,
    getReviewerGroups(noteNumbers),
    invitationsP,
    tagInvitationsP
  );
};

var getOfficialReviews = function(noteNumbers) {
  if (!noteNumbers.length) {
    return $.Deferred().resolve({});
  }

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
  if (!noteNumbers.length) {
    return $.Deferred().resolve({});
  };

  var noteMap = buildNoteMap(noteNumbers);

  return Webfield.getAll('/groups', { id: ANONREVIEWER_WILDCARD })
  .then(function(groups) {
    _.forEach(groups, function(g) {
      var matches = g.id.match(ANONREVIEWER_REGEX);
      var num, index;
      if (matches) {
        num = parseInt(matches[1], 10);
        index = parseInt(matches[2], 10);

        if ((num in noteMap) && g.members.length) {
          noteMap[num][index] = g.members[0];
        }
      }

      var matches = g.id.match(REVIEWER_REGEX);
      if (matches) {
        num = parseInt(matches[1], 10);
        if ((num in noteMap) && g.members.length) {
          invitedMap[num]['accepted'] = g.members;
        }
      }

      var matches = g.id.match(REVIEWER_INVITED_REGEX);
      if (matches) {
        num = parseInt(matches[1], 10);
        if ((num in noteMap) && g.members.length) {
          invitedMap[num]['invited'] = g.members;
        }
      }

      var matches = g.id.match(REVIEWER_DECLINED_REGEX);
      if (matches) {
        num = parseInt(matches[1], 10);
        if ((num in noteMap) && g.members.length) {
          invitedMap[num]['declined'] = g.members;
        }
      }

    });
    return noteMap;
  });
};

var formatData = function(individualGroupIds, blindedNotes, officialReviews, metaReviews, noteToReviewerIds, invitations, tagInvitations) {
  var uniqueIds = _.uniq(_.reduce(noteToReviewerIds, function(result, idsObj, noteNum) {
    return result.concat(_.values(idsObj));
  }, []));

  return getUserProfiles(uniqueIds)
  .then(function(profiles) {
    return {
      individualGroupIds: individualGroupIds,
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
      profile.email = profile.content.preferredEmail || profile.content.emails[0];
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
      heading: 'Assigned Papers',
      id: 'assigned-papers',
      content: loadingMessage,
      extraClasses: 'horizontal-scroll',
      active: true
    },
    {
      heading: 'Program Committee Schedule',
      id: 'program-committee-schedule',
      content: SCHEDULE_HTML
    },
    {
      heading: 'Program Committee Tasks',
      id: 'program-committee-tasks',
      content: loadingMessage
    }
  ]);
};

var renderStatusTable = function(individualGroupIds, profiles, notes, completedReviews, metaReviews, reviewerIds, container) {
  var rows = _.map(notes, function(note, index) {
    var revIds = reviewerIds[note.number] || Object.create(null);
    for (var revNumber in revIds) {
      var uId = revIds[revNumber];
      revIds[revNumber] = _.get(profiles, uId, { id: uId, name: '', email: uId });
    }

    var metaReview = _.find(metaReviews, ['invitation', CONFERENCE + '/-/Paper' + note.number + '/Meta_Review']);
    var noteCompletedReviews = completedReviews[note.number] || Object.create(null);

    return buildTableRow(individualGroupIds[index], note, revIds, noteCompletedReviews, metaReview);
  });

  // Sort form handler
  var order = 'desc';
  var sortOptions = {
    Paper_Number: function(row) { return row[1].number; },
    Paper_Title: function(row) { return _.toLower(_.trim(row[2].content.title)); },
    Number_of_Reviews_Submitted: function(row) { return row[3].numSubmittedReviews; },
    Number_of_Reviews_Missing: function(row) { return row[3].numReviewers - row[3].numSubmittedReviews; },
    Average_Rating: function(row) { return row[4].averageRating === 'N/A' ? 0 : row[4].averageRating; },
    Max_Rating: function(row) { return row[4].maxRating === 'N/A' ? 0 : row[4].maxRating; },
    Min_Rating: function(row) { return row[4].minRating === 'N/A' ? 0 : row[4].minRating; },
    Average_Confidence: function(row) { return row[5].averageConfidence === 'N/A' ? 0 : row[5].averageConfidence; },
    Max_Confidence: function(row) { return row[5].maxConfidence === 'N/A' ? 0 : row[5].maxConfidence; },
    Min_Confidence: function(row) { return row[5].minConfidence === 'N/A' ? 0 : row[5].minConfidence; },
    Meta_Review_Rating: function(row) { return row[6].recommendation ? _.toInteger(row[6].recommendation.split(':')[0]) : 0; }
  };
  var sortResults = function(newOption, switchOrder) {
    if (switchOrder) {
      order = order === 'asc' ? 'desc' : 'asc';
    }
    renderTableRows(_.orderBy(rows, sortOptions[newOption], order), container);
  }

  // Message modal handler
  var sendReviewerReminderEmailsStep1 = function(e) {
    var subject = $('#message-reviewers-modal input[name="subject"]').val().trim();
    var message = $('#message-reviewers-modal textarea[name="message"]').val().trim();
    var group   = $('#message-reviewers-modal select[name="group"]').val();
    var filter  = $('#message-reviewers-modal select[name="filter"]').val();

    var count = 0;
    var selectedRows = rows;
    var reviewerMessages = [];
    var reviewerCounts = Object.create(null);
    if (group === 'selected') {
      selectedIds = _.map(
        $('.ac-console-table input.select-note-reviewers:checked'),
        function(checkbox) { return $(checkbox).data('noteId'); }
      );
      selectedRows = rows.filter(function(row) {
        return _.includes(selectedIds, row[2].forum);
      });
    }

    selectedRows.forEach(function(row) {
      var users = _.values(row[4].reviewers);
      if (filter === 'submitted') {
        users = users.filter(function(u) {
          return u.completedReview;
        });
      } else if (filter === 'unsubmitted') {
        users = users.filter(function(u) {
          return !u.completedReview;
        });
      }

      if (users.length) {
        var forumUrl = 'https://openreview.net/forum?' + $.param({
          id: row[2].forum,
          noteId: row[2].id,
          invitationId: CONFERENCE + '/-/Paper' + row[2].number + '/Official_Review'
        });
        reviewerMessages.push({
          groups: _.map(users, 'id'),
          forumUrl: forumUrl,
          subject: subject,
          message: message,
        });

        users.forEach(function(u) {
          if (u.id in reviewerCounts) {
            reviewerCounts[u.id].count++;
          } else {
            reviewerCounts[u.id] = {
              name: u.name,
              email: u.email,
              count: 1
            };
          }
        });

        count += users.length;
      }
    });
    localStorage.setItem('reviewerMessages', JSON.stringify(reviewerMessages));
    localStorage.setItem('messageCount', count);

    // Show step 2
    var namesHtml = _.flatMap(reviewerCounts, function(obj) {
      var text = obj.name + ' <span>&lt;' + obj.email + '&gt;</span>';
      if (obj.count > 1) {
        text += ' (&times;' + obj.count + ')';
      }
      return text;
    }).join(', ');
    $('#message-reviewers-modal .reviewer-list').html(namesHtml);
    $('#message-reviewers-modal .num-reviewers').text(count);
    $('#message-reviewers-modal .step-1').hide();
    $('#message-reviewers-modal .step-2').show();

    return false;
  };

  var sendReviewerReminderEmailsStep2 = function(e) {
    var reviewerMessages = localStorage.getItem('reviewerMessages');
    var messageCount = localStorage.getItem('messageCount');
    if (!reviewerMessages || !messageCount) {
      $('#message-reviewers-modal').modal('hide');
      promptError('Could not send reminder emails at this time. Please refresh the page and try again.');
    }
    JSON.parse(reviewerMessages).forEach(postReviewerEmails);

    localStorage.removeItem('reviewerMessages');
    localStorage.removeItem('messageCount');

    $('#message-reviewers-modal').modal('hide');
    promptMessage('Successfully sent ' + messageCount + ' reminder emails');
  };

  var sortOptionHtml = Object.keys(sortOptions).map(function(option) {
    return '<option value="' + option + '">' + option.replace(/_/g, ' ') + '</option>';
  }).join('\n');

  var sortBarHtml = '<form class="form-inline search-form clearfix" role="search">' +
    '<strong>Sort By:</strong> ' +
    '<select id="form-sort" class="form-control">' + sortOptionHtml + '</select>' +
    '<button id="form-order" class="btn btn-icon"><span class="glyphicon glyphicon-sort"></span></button>' +
    '<div class="pull-right">' +
      '<button id="message-reviewers-btn" class="btn btn-icon"><span class="glyphicon glyphicon-envelope"></span> &nbsp;Message Reviewers</button>' +
    '</div>' +
    '</form>';
  if (rows.length) {
    $(container).empty().append(sortBarHtml);
  }

  // Need to add event handlers for these controls inside this function so they have access to row
  // data
  $('#form-sort').on('change', function(e) {
    sortResults($(e.target).val(), false);
  });
  $('#form-order').on('click', function(e) {
    sortResults($(this).prev().val(), true);
    return false;
  });

  $('#message-reviewers-btn').on('click', function(e) {
    $('#message-reviewers-modal').remove();

    var modalHtml = Handlebars.templates.messageReviewersModal({
      defaultSubject: SHORT_PHRASE + ' Reminder',
      defaultBody: 'This is a reminder to please submit your review for ' + SHORT_PHRASE + '. ' +
        'Click on the link below to go to the review page:\n\n[[SUBMIT_REVIEW_LINK]]' +
        '\n\nThank you,\n' + SHORT_PHRASE + ' Program Committee',
    });
    $('body').append(modalHtml);

    $('#message-reviewers-modal .btn-primary.step-1').on('click', sendReviewerReminderEmailsStep1);
    $('#message-reviewers-modal .btn-primary.step-2').on('click', sendReviewerReminderEmailsStep2);
    $('#message-reviewers-modal form').on('submit', sendReviewerReminderEmailsStep1);

    $('#message-reviewers-modal').modal();

    if ($('.ac-console-table input.select-note-reviewers:checked').length) {
      $('#message-reviewers-modal select[name="group"]').val('selected');
    }
    return false;
  });

  if (rows.length) {
    renderTableRows(rows, container);
  } else {
    $(container).empty().append('<p class="empty-message">No assigned papers. ' +
      'Check back later or contact info@openreview.net if you believe this to be an error.</p>');
  }

};

var renderInvitedReviewers = function(data) {
  var accepted = '';
  var declined = '';
  var invited = '';
  data.invited.accepted.forEach(function(r) {
    accepted = accepted + '<tr><td>' + r + '<span class="text-muted">(accepted)</span></td></tr>';
  })
  data.invited.declined.forEach(function(r) {
    declined = declined + '<tr><td>' + r + '<span class="text-muted">(declined)</span></td></tr>';
  })
  data.invited.invited.forEach(function(r) {
    if (!data.invited.accepted.includes(r) && !data.invited.declined.includes(r)) {
      invited = invited + '<tr><td>' + r + '<span class="text-muted">(invited)</span></td></tr>';
    }
  })
  return '<div id= "' + data.noteId +'-invited-reviewers" class="collapse" style="display: block;">' +
  '<table class="table table-condensed table-minimal">' +
  '  <tbody>' +
        accepted +
        declined +
        invited +
    ' </tbody>' +
  '</table>' +
  '</div>';
};

var renderTableRows = function(rows, container) {
  var templateFuncs = [
    function(data) {
      var checked = data.selected ? 'checked="checked"' : '';
      return '<label><input type="checkbox" class="select-note-reviewers" data-note-id="' +
        data.noteId + '" ' + checked + '></label>';
    },
    function(data) {
      return '<strong class="note-number">' + data.number + '</strong>';
    },
    Handlebars.templates.noteSummary,
    function(data) {
      return '<div class="reviewer-invite"><input data-individual-group-id="' + data.individualGroupId + '" data-note-id="' + data.noteId + '" data-note-number="' + data.noteNumber +
      '"></input><button class="btn invite">Invite</button></div>' +
      renderInvitedReviewers(data);
    },
    Handlebars.templates.noteReviewers,
    function(data) {
      return '<h4>Avg: ' + data.averageRating + '</h4><span>Min: ' + data.minRating + '</span>' +
        '<br><span>Max: ' + data.maxRating + '</span>';
    },
    function(data) {
      return '<h4>Avg: ' + data.averageConfidence + '</h4><span>Min: ' + data.minConfidence + '</span>' +
        '<br><span>Max: ' + data.maxConfidence + '</span>';
    }
  ];

  var rowsHtml = rows.map(function(row) {
    return row.map(function(cell, i) {
      return templateFuncs[i](cell);
    });
  });

  var tableHtml = Handlebars.templates['components/table']({
    headings: [
      '<span class="glyphicon glyphicon-envelope"></span>', '#', 'Paper Summary',
      'Reviewer Invite', 'Review Progress', 'Rating', 'Confidence'
    ],
    rows: rowsHtml,
    extraClasses: 'ac-console-table'
  });

  $('.table-container', container).remove();
  $(container).append(tableHtml);
}

var renderTasks = function(invitations, tagInvitations) {
  //  My Tasks tab
  var tasksOptions = {
    container: '#program-committee-tasks',
    emptyMessage: 'No outstanding tasks for this conference'
  }
  $(tasksOptions.container).empty();

  // Filter out non-areachair tasks
  var filterFunc = function(inv) {
    return _.some(inv.invitees, function(invitee) { return invitee.indexOf('Area_Chair') !== -1; });
  };
  var areachairInvitations = _.filter(invitations, filterFunc);
  var areachairTagInvitations = _.filter(tagInvitations, filterFunc);

  Webfield.ui.newTaskList(areachairInvitations, areachairTagInvitations, tasksOptions);
  $('.tabs-container a[href="#program-committee-tasks"]').parent().show();
}

var renderTableAndTasks = function(fetchedData) {
  renderTasks(fetchedData.invitations, fetchedData.tagInvitations);

  renderStatusTable(
    fetchedData.individualGroupIds,
    fetchedData.profiles,
    fetchedData.blindedNotes,
    fetchedData.officialReviews,
    fetchedData.metaReviews,
    _.cloneDeep(fetchedData.noteToReviewerIds), // Need to clone this dictionary because some values are missing after the first refresh
    '#assigned-papers'
  );

  registerEventHandlers(fetchedData.blindedNotes);

  //Set another table widths
  $('.row-4').css('width', '25%');
  $('.row-6').css('width', '11%');

  Webfield.ui.done();
}

var buildTableRow = function(individualGroupId, note, reviewerIds, completedReviews, metaReview) {
  var cellCheck = { selected: false, noteId: note.id };

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
      var forumUrl = 'https://openreview.net/forum?' + $.param({
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
        lastReminderSent: lastReminderSent ? new Date(parseInt(lastReminderSent)).toLocaleDateString() : lastReminderSent
      };
    }
  }

  var cell2 = {
    noteId: note.id,
    noteNumber: note.number,
    individualGroupId: individualGroupId,
    invited: invitedMap[note.number]
  }

  var cell3 = {
    noteId: note.id,
    numSubmittedReviews: Object.keys(completedReviews).length,
    numReviewers: Object.keys(reviewerIds).length,
    reviewers: combinedObj,
    sendReminder: true
  };

  // Rating cell
  var cell4 = {
    averageRating: 'N/A',
    minRating: 'N/A',
    maxRating: 'N/A'
  };
  if (ratings.length) {
    cell4.averageRating = _.round(_.sum(ratings) / ratings.length, 2);
    cell4.minRating = _.min(ratings);
    cell4.maxRating = _.max(ratings);
  }

  // Confidence cell
  var cell5 = {
    averageConfidence: 'N/A',
    minConfidence: 'N/A',
    maxConfidence: 'N/A'
  };
  if (confidences.length) {
    cell5.averageConfidence = _.round(_.sum(confidences) / confidences.length, 2);
    cell5.minConfidence = _.min(confidences);
    cell5.maxConfidence = _.max(confidences);
  }

  if (metaReview) {
    cell5.recommendation = metaReview.content.recommendation;
    cell5.editUrl = '/forum?id=' + note.forum + '&noteId=' + metaReview.id;
  }

  return [cellCheck, cell0, cell1, cell2, cell3, cell4, cell5];
};


// Event Handlers
var registerEventHandlers = function(blindedNotes) {
  $('#group-container').on('click', 'a.note-contents-toggle', function(e) {
    var hiddenText = 'Show paper details';
    var visibleText = 'Hide paper details';
    var updated = $(this).text() === hiddenText ? visibleText : hiddenText;
    $(this).text(updated);
  });

  $('#group-container').on('click', 'a.send-reminder-link', function(e) {
    var $link = $(this);
    var userId = $link.data('userId');
    var forumUrl = $link.data('forumUrl');

    var sendReviewerReminderEmails = function(e) {
      var postData = {
        groups: [userId],
        forumUrl: forumUrl,
        subject: $('#message-reviewers-modal input[name="subject"]').val().trim(),
        message: $('#message-reviewers-modal textarea[name="message"]').val().trim(),
      };

      $('#message-reviewers-modal').modal('hide');
      // promptMessage('Your reminder email has been sent to ' + view.prettyId(userId));
      postReviewerEmails(postData);
      $link.after(' (Last sent: ' + (new Date()).toLocaleDateString());

      return false;
    };

    var modalHtml = Handlebars.templates.messageReviewersModal({
      singleRecipient: true,
      reviewerId: userId,
      forumUrl: forumUrl,
      defaultSubject: SHORT_PHRASE + ' Reminder',
      defaultBody: 'This is a reminder to please submit your review for ' + SHORT_PHRASE + '. ' +
        'Click on the link below to go to the review page:\n\n[[SUBMIT_REVIEW_LINK]]' +
        '\n\nThank you,\n' + SHORT_PHRASE + ' Program Committee',
    });
    $('#message-reviewers-modal').remove();
    $('body').append(modalHtml);

    $('#message-reviewers-modal .btn-primary').on('click', sendReviewerReminderEmails);
    $('#message-reviewers-modal form').on('submit', sendReviewerReminderEmails);

    $('#message-reviewers-modal').modal();
    return false;
  });

  $('#group-container').on('click', 'a.collapse-btn', function(e) {
    $(this).next().slideToggle();
    if ($(this).text() === 'Show reviewers') {
      $(this).text('Hide reviewers');
    } else {
      $(this).text('Show reviewers');
    }
    return false;
  });

  $('#group-container').on('click', 'button.invite', function(e) {
    $parent = $(this).parent();
    noteId = $parent.find('input').data('noteId');
    noteNumber = $parent.find('input').data('noteNumber');
    invididualGroupId = $parent.find('input').data('individualGroupId');
    reviewer = $parent.find('input').val();
    noteObj = _.find(blindedNotes, {'id' : noteId});
    noteName = noteObj.content['title'];

    inviteReviewer(invididualGroupId, noteId, noteNumber, noteName, reviewer, function() {
      $parent.find('input').val('');
      invitedMap[noteNumber].invited.push(reviewer);
      var data = {
        noteId: noteId,
        noteNumber: noteNumber,
        noteName: noteName,
        invited: {
          accepted: invitedMap[noteNumber].accepted,
          invited: invitedMap[noteNumber].invited,
          declined: invitedMap[noteNumber].declined
        }
      }
      $('#' + noteId + '-invited-reviewers').html(renderInvitedReviewers(data));
      console.log('Done');
    });
    return false;
  });
};

var postReviewerEmails = function(postData) {
  postData.message = postData.message.replace(
    '[[SUBMIT_REVIEW_LINK]]',
    postData.forumUrl
  );

  return Webfield.post('/mail', postData)
    .then(function(response) {
      // Save the timestamp in the local storage
      for (var i = 0; i < postData.groups.length; i++) {
        var userId = postData.groups[i];
        localStorage.setItem(postData.forumUrl + '|' + userId, Date.now());
      }
    });
};

var inviteReviewer = function(invididualGroupId, noteId, noteNumber, noteName, reviewer, done) {

  var postData = {
    id: invididualGroupId + '/-/Recruit_Reviewers',
    duedate: 1575488730000,
    super: 'learningtheory.org/COLT/2019/Conference/-/Recruit_Reviewers',
    reply: {
      forum: noteId
    },
    signatures: [invididualGroupId],
    readers: ['everyone'],
    writers: [invididualGroupId]
  }
  return Webfield.post('/invitations', postData)
  .then(function(response) {
    console.log('Invitation posted');
    var key = CryptoJS.HmacSHA256(reviewer, '1234');
    var acceptUrl = 'https://openreview.net/invitation?id=' + response.id + '&email=' + reviewer + '&key=' + key +'&response=Yes';
    var declineUrl = 'https://openreview.net/invitation?id=' + response.id + '&email=' + reviewer + '&key=' + key + '&response=No';
    var email = {
      groups: [reviewer],
      subject: SHORT_PHRASE + ': Invitation to review paper title: ' + noteName,
      message: 'You have been invited to ' + SHORT_PHRASE + ' to review a paper. \n\nPaper title: ' + noteName + ' \n\n\n\nTo accept please follow this link: ' + acceptUrl + '\n\nTo reject follow this link: ' + declineUrl + '\n\nTo find more details about the paper please sign up on openreview.net using the address you received this email at and then follow this link: https://openreview.net/forum?id=' +  noteId
    }
    return Webfield.post('/messages', email)
  })
  .then(function(response) {
    console.log('Email sent');
    return Webfield.put('/groups/members', {
      id: invididualGroupId + '/Reviewers_Invited',
      members: [reviewer] });
  })
  .then(function(response) {
    console.log('User added to invited group');
    done();
  });
}

main();
