/**
 * This is the template for a venue homepage webfield
 *
 **/

// CONSTANTS
var CONFERENCE = 'auai.org/UAI/2017';
var SUBJECT_AREAS_LIST = [
  'All',
  'Algorithms: Approximate Inference',
  'Algorithms: Belief Propagation',
  'Algorithms: Distributed and Parallel',
  'Algorithms: Exact Inference',
  'Algorithms: Graph Theory',
  'Algorithms: Heuristics',
  'Algorithms: Lifted Inference',
  'Algorithms: MCMC methods',
  'Algorithms: Optimization',
  'Algorithms: Other',
  'Algorithms: Software and Tools',
  'Applications: Biology',
  'Applications: Databases',
  'Applications: Decision Support',
  "Applications: Diagnosis and Reliability",
  'Applications: Economics',
  'Applications: Education',
  'Applications: General',
  'Applications: Medicine',
  'Applications: Planning and Control',
  'Applications: Privacy and Security',
  'Applications: Robotics',
  'Applications: Sensor Data',
  'Applications: Social Network Analysis',
  'Applications: Speech',
  'Applications: Sustainability and Climate',
  'Applications: Text and Web Data',
  'Applications: User Models',
  'Applications: Vision',
  'Data: Big Data',
  'Data: Multivariate',
  'Data: Other',
  'Data: Relational',
  'Data: Spatial',
  'Data: Temporal or Sequential',
  'Learning: Active Learning',
  'Learning: Classification',
  'Learning: Clustering',
  'Learning: Deep Learning',
  'Learning: General',
  'Learning: Nonparametric Bayes',
  'Learning: Online and Anytime Learning',
  'Learning: Other',
  'Learning: Parameter Estimation',
  'Learning: Probabilistic Generative Models',
  'Learning: Ranking',
  'Learning: Recommender Systems',
  'Learning: Regression',
  'Learning: Reinforcement Learning',
  'Learning: Relational Learning',
  'Learning: Relational Models',
  'Learning: Scalability',
  'Learning: Semi-Supervised Learning',
  'Learning: Structure Learning',
  'Learning: Structured Prediction',
  'Learning: Theory',
  'Learning: Unsupervised',
  'Methodology: Bayesian Methods',
  'Methodology: Calibration',
  'Methodology: Elicitation',
  'Methodology: Evaluation',
  'Methodology: Human Expertise and Judgement',
  'Methodology: Other',
  'Methodology: Probabilistic Programming',
  'Models: Bayesian Networks',
  'Models: Directed Graphical Models',
  'Models: Dynamic Bayesian Networks',
  'Models: Markov Decision Processes',
  'Models: Mixed Graphical Models',
  'Models: Other',
  'Models: Relational Models',
  'Models: Topic Models',
  'Models: Undirected Graphical Models',
  'None of the above',
  'Principles: Causality',
  'Principles: Cognitive Models',
  'Principles: Decision Theory',
  'Principles: Game Theory',
  'Principles: Information Theory',
  'Principles: Other',
  'Principles: Probability Theory',
  'Principles: Statistical Theory',
  'Representation: Constraints',
  'Representation: Dempster-Shafer',
  'Representation: Fuzzy Logic',
  'Representation: Influence Diagrams',
  'Representation: Non-Probabilistic Frameworks',
  'Representation: Probabilistic'
];

var dueDateBuffer = 1000 * 60 * 30;  // 30 minutes

var getInvitation = function() {
  return httpGetP('invitations', {id: 'auai.org/UAI/2017/-/submission'}).then(function(result) {
    var valid_invitations = _.filter(result.invitations, function(inv) {
      return (inv.duedate + dueDateBuffer) > Date.now();
    });
    return valid_invitations[0];
  }, function(error) {
    return error;
  });
};

var getAllNotes = function() {
  return httpGetP('notes', {invitation: 'auai.org/UAI/2017/-/blind-submission'}).then(function(result) {
    return result.notes;
  }, function(error) {
    return error;
  });
};

var getSubmittedNotes = function() {
  return httpGetP('notes', {invitation: 'auai.org/UAI/2017/-/.*', tauthor: true}).then(function(result) {
    return result.notes;
  }, function(error) {
    return error;
  });
};

var getAssignedNotes = function() {
  return httpGetP('notes', {invitation: 'auai.org/UAI/2017/-/.*', invitee: true, duedate: true}).then(function(result) {
    return _.filter(result.notes, function(note) {
      return _.startsWith(note.invitation.id, 'auai.org/UAI/2017');
    });
  }, function(error) {
    return error;
  });
};

var getTagInvitations = function() {
  return httpGetP('invitations', {replyInvitation: 'auai.org/UAI/2017/-/blind-submission', tags: true}).then(function(result) {
    return result.invitations;
  }, function(error) {
    return error;
  });
};

var getUserGroups = function() {
  if (!user || _.startsWith(user.id, 'guest_')) {
    return Promise.resolve([]);
  }

  return httpGetP('groups', {member: user.id}).then(function(result) {
    return _.filter(
      _.map(result.groups, function(g) { return g.id; }),
      function(id) { return _.startsWith(id, 'auai.org/UAI/2017') || id === '~Super_User1'; }
    );
  }, function(error) {
    return error;
  });
};


// Helper functions
var filterPapers = function() {
  var $formElem = $('.tabs-container .search-form');
  var term = $formElem.find('.search-content input').val().trim().toLowerCase();
  var selectedSubject = $formElem.find('.subject-area-dropdown input').val().trim();
  var filterSubjects = selectedSubject && selectedSubject !== 'All';
  var filteredNotes;

  if (!term) {
    if (filterSubjects) {
      filteredNotes = _.filter(allNotes, function(n) {
        var content = n.content;
        return _.includes(content['subject areas'], selectedSubject);
      });
    } else {
      filteredNotes = allNotes;
    }
  } else {
    filteredNotes = _.filter(allNotes, function(n) {
      var content = n.content;
      var contentFields = ['TL;DR', 'abstract', 'keywords', 'subject areas', 'title'];

      for (var i = 0; i < contentFields.length; i++) {
        var searchText;
        var contentField = contentFields[i];
        var contentValue = _.has(content, contentField) ? content[contentField] : '';

        if (_.isArray(contentValue)) {
          searchText = contentValue.join(' ').toLowerCase();
        } else {
          searchText = contentValue.toLowerCase();
        }

        if (searchText.indexOf(term) !== -1) {
          if (filterSubjects) {
            return _.includes(content['subject areas'], selectedSubject);
          } else {
            return true;
          }
        }
      }

      return false;
    });
  }

  $('#all-submitted-papers .note.panel').remove();
  $('#all-submitted-papers .empty-message').remove();
  displayNotes(filteredNotes, '#all-submitted-papers');
  return false;
};

var processRawNoteData = function(blindedNotes, authorNotes, assignedPairs) {
  var commentNotes = [];

  _.forEach(authorNotes, function(note) {
    if (_.startsWith(note.invitation, 'auai.org/UAI/2017') &&
        (note.invitation !== 'auai.org/UAI/2017/-/submission') &&
        (_.isNull(note.ddate) || _.isUndefined(note.ddate))) {
      // TODO: remove this client side filtering when DB query is fixed
      commentNotes.push(note);
    }
  });

  var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
  var assignedNotes = _.filter(blindedNotes, function(n) { return _.includes(assignedPaperNumbers, n.number); });

  var authorPaperNumbers = getAuthorPaperNumbersfromGroups(userGroups);
  var submittedNotes = _.filter(blindedNotes, function(n) { return _.includes(authorPaperNumbers, n.number); });

  return {
    allNotes: blindedNotes,
    submittedNotes: submittedNotes,
    assignedNotes: assignedNotes,
    commentNotes: commentNotes,
    tasksList: assignedPairs
  };
};

var getPaperNumbersfromGroups = function(groups) {
  var re = /^auai\.org\/UAI\/2017\/Paper(\d+)\/(AnonReviewer\d+|Area_Chair)/;
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
};

var getAuthorPaperNumbersfromGroups = function(groups) {
  var re = /auai.org\/UAI\/2017\/Paper(\d+)\/Authors/;
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
};

var getDueDateStatus = function(date) {
  var day = 24 * 60 * 60 * 1000;
  var diff = Date.now() - date.getTime();

  if (diff > 0) {
    return 'expired';
  }

  if (diff > (-1 * 3 * day)) {
    return 'warning';
  }

  return '';
};


// Render functions
var renderConferenceHeader = function() {
  Webfield.ui.setup('#group-container');
  Webfield.ui.venueHeader({
    title: 'UAI 2017 Conference',
    subtitle: 'International Conference on Uncertainty in Artificial Intelligence',
    location: 'Sydney, Australia',
    date: 'August 11 - 15, 2017',
    website: 'http://auai.org/uai2017/',
    instructions: 'Submission Deadline: March 31st, 2017, 11:59 pm SST (Samoa Standard Time)'
  });
};

var renderConferenceInvitations = function(invitationTrip) {
  if (!invitationTrip) {
    return;
  }

  var invitation = invitationTrip.invitation;

  var onInvitationButtonClicked = function() {
    if (!user || _.startsWith(user.id, 'guest_')) {
      promptLogin(user);
      return;
    }

    view.mkNewNoteEditor(invitation, null, null, user, {
      onNoteCreated: function(idRecord) {
        promptMessage('Thank you for submitting to UAI. Your paper submission will appear shortly in the "My Submitted Papers" tab. If you don\'t see your paper after 15 minutes please contact us at info@openreview.net', {noTimeout: true});

        $.when(
          getUserGroups(),
          getAllNotes(),
          getSubmittedNotes(),
          getAssignedNotes(),
          getTagInvitations()
        ).done(function(groups, notes, submittedNotes, assignedNotes, tagInvitations) {
          userGroups = groups;
          allNotes = notes;

          var tabContents = processRawNoteData(notes, submittedNotes, assignedNotes);
          tabContents.tagInvitations = tagInvitations;
          sm.update('notes', tabContents);
        });
      },

      onCompleted: function(editor) {
        $('#invitation .panel').append(editor);
      }
    });
  };

  Webfield.ui.invitationButton(invitation, onInvitationButtonClicked, { largeLabel: true });
};

var renderConferenceTabs = function() {
  $('#notes .tabs-container').empty();

  var allOptions = '<option>' + SUBJECT_AREAS_LIST.join('</option>\n<option>') + '</option>';
  var searchBarHTML = '<form class="form-inline search-form" role="search">' +
    '<div class="form-group search-content has-feedback">' +
      '<input id="paper-search-input" type="text" class="form-control" placeholder="Search paper titles and metadata" autocomplete="off">' +
      '<span class="glyphicon glyphicon-search form-control-feedback" aria-hidden="true"></span>' +
    '</div>' +
    '<div class="form-group subject-area">' +
      '<label for="subject-area-dropdown">Subject Area</label>' +
    '</div>' +
    '</form>';

  var templateData = {
    sections: [
      {
        heading: 'My Tasks',
        id: 'my-tasks',
        content: null,
        active: true
      },
      {
        heading: 'All Submitted Papers',
        id: 'all-submitted-papers',
        content: searchBarHTML,
      },
      {
        heading: 'My Submitted Papers',
        id: 'my-submitted-papers',
        content: null,
      },
      {
        heading: 'My Assigned Papers',
        id: 'my-assigned-papers',
        content: null,
      },
      {
        heading: 'My Comments & Reviews',
        id: 'my-comments-reviews',
        content: null,
      }
    ]
  };

  $('#notes .tabs-container').append(Handlebars.templates['components/tabs'](templateData));

  // Add subject area dropdown to search form
  var subjectAreaFilter = function(update, prefix) {
    prefix = prefix.trim().toLowerCase();
    if (!prefix) {
      update(SUBJECT_AREAS_LIST);
      subjectAreaSelected('');
    } else {
      update(_.filter(SUBJECT_AREAS_LIST, function(subject) {
        return subject.toLowerCase().indexOf(prefix) !== -1;
      }));
    }
  };
  var subjectAreaSelected = function(selectedSubject, subjectId, focus) {
    if (!focus ) {
      filterPapers();
    }
  };

  $('form.search-form .subject-area').append(view.mkDropdown(
    'Enter a subject area to filter by',
    false,
    '',
    _.debounce(subjectAreaFilter, 300),
    _.debounce(subjectAreaSelected, 300),
    'subject-area-dropdown show-arrow'
  ));
};

var renderConferenceNotes = function(data) {
  var notes = data.allNotes;
  var submittedNotes = data.submittedNotes;
  var assignedNotes = data.assignedNotes;
  var commentNotes = data.commentNotes;
  var tasksList = data.tasksList;
  var tagInvitations = data.tagInvitations;

  var displayOptions = {
    tagInvitations: tagInvitations
  };

  if (_.isEmpty(userGroups)) {
    return;
  }

  // My Tasks tab
  displayTasks(tasksList, tagInvitations, '#my-tasks');

  // All Submitted Papers tab
  var acGroups = ['auai.org/UAI/2017/Program_Committee', 'auai.org/UAI/2017/Senior_Program_Committee', 'auai.org/UAI/2017/Program_Co-Chairs'];
  if (_.intersection(userGroups, acGroups).length) {
    displayNotes(notes, '#all-submitted-papers', displayOptions);
  } else {
    $('.tabs-container a[href="#all-submitted-papers"]').parent().hide();
  }

  // My Submitted Papers tab
  displayNotes(submittedNotes, '#my-submitted-papers', displayOptions);

  // My Assigned Papers tab
  if (assignedNotes.length) {
    displayNotes(assignedNotes, '#my-assigned-papers', displayOptions);
  } else {
    $('.tabs-container a[href="#my-assigned-papers"]').parent().hide();
  }

  // My Comments & Reviews tab
  if (commentNotes.length) {
    displayNotes(commentNotes, '#my-comments-reviews', {withParentNote: true});
  } else {
    $('.tabs-container a[href="#my-comments-reviews"]').parent().hide();
  }

  $('#notes .tabs-container').fadeIn('fast');
};

var displayNotes = function(notes, container, options) {
  var config = {
    titleLink: 'HREF',
    withReplyCount: true,
    user: user,
    tagInvitations: null,
    emptyMessage: 'No papers to display'
  };
  _.assign(config, options);

  $('.note.panel, .empty-message', container).remove();

  _.forEach(notes, function(note) {
    $attach(container, 'mkNotePanel', [note, config], true);
  });

  if (!notes.length) {
    $(container).append('<p class="empty-message">' + config.emptyMessage + '</p>');
  }
};

var displayTasks = function(invitationPairs, tagInvitations, container) {
  var $rows = [];
  var consoleLink;

  $('.note.panel, .empty-message, .invitation-link', container).remove();

  var pcId = 'auai.org/UAI/2017/Program_Co-Chairs';
  if (_.includes(userGroups, pcId)) {
    consoleLink = '<div class="note panel"><a href="/reviewers?id=auai.org/UAI/2017" class="console-link">UAI 2017 Matching Browser</a></div>';
    $(container).append(consoleLink);

    consoleLink = '<div class="note panel"><a href="/group?id=auai.org/UAI/2017/Program_Co-Chairs" class="console-link">UAI 2017 Program Co-Chairs Console</a></div>';
    $(container).append(consoleLink);
  }

  var spcId = 'auai.org/UAI/2017/Senior_Program_Committee';
  if (_.includes(userGroups, spcId)) {
    consoleLink = '<div class="note panel"><a href="/group?id=' + spcId + '" class="console-link">UAI 2017 Senior Program Committee Console</a></div>';
    $(container).append(consoleLink);
  }

  _.forEach(tagInvitations, function(inv) {
    var duedate = new Date(inv.duedate);
    var duedateStr = duedate.toLocaleDateString('en-GB', { hour: 'numeric', minute: 'numeric', day: '2-digit', month: 'short', year: 'numeric'});

    if (inv.web) {
      $rows.push($('<div>', {class: 'panel invitation-link'}).append(
        $('<a>', {href: '/invitation?id=' + inv.id, text: view.prettyId(inv.id), class: 'console-link'}),
        $('<span>', {class: 'invitation-duedate', text: 'Due: ' + duedateStr}).addClass(getDueDateStatus(duedate))
      ));
    }
  });

  _.forEach(invitationPairs, function(pair) {
    var inv = pair.invitation;
    var replytoNote = pair.replytoNote;
    var duedate = new Date(inv.duedate);
    var duedateStr = duedate.toLocaleDateString('en-GB', { hour: 'numeric', minute: 'numeric', day: '2-digit', month: 'short', year: 'numeric'});

    $rows.push(
      view.mkNotePanel(replytoNote, {
        invitation: inv,
        titleLink: 'HREF',
        withReplyCount: true
      }),
      $('<div class="invitation-link">').append(
        $('<a href="#">' + view.prettyInvitationId(inv.id) + '</a>').click(function() {
          controller.removeHandler('tasks');
          pushForum(inv.reply.forum, inv.reply.replyto, inv.id);
          return false;
        }),
        '<span class="invitation-duedate ' + getDueDateStatus(duedate) + '">Due: ' + duedateStr + '</span>'
      )
    );
  });

  if ($rows.length) {
    $(container).append($rows);
  } else {
    $(container).append('<p class="empty-message">No outstanding tasks for UAI 2017</p>');
  }
};

var displayError = function(message) {
  message = message || 'The venue invitation and/or papers could not be loaded.';
  $('#notes').empty().append('<div class="alert alert-danger"><strong>Error:</strong> ' + message + '</div>');
};
var displayWarning = function(message) {
  message = message || 'Please login to submit or review papers for this venue.';
  $('#notes').empty().append('<div class="alert alert-warning">' + message + '</div>');
};


// Start the whole thing running
var userGroups = [];
var allNotes = [];
var sm = null;

renderConferenceHeader();

renderConferenceTabs();

$.when(
  getUserGroups(),
  getInvitation(),
  getAllNotes(),
  getSubmittedNotes(),
  getAssignedNotes(),
  getTagInvitations()
).done(function(groups, invitation, notes, submittedNotes, assignedNotes, tagInvitations) {
  sm = mkStateManager();
  userGroups = groups;
  allNotes = notes;

  sm.update('invitationTrip', {invitation: invitation});

  var tabContents = processRawNoteData(notes, submittedNotes, assignedNotes);
  tabContents.tagInvitations = tagInvitations;
  sm.update('notes', tabContents);

  sm.addHandler('conference', {
    invitationTrip: renderConferenceInvitations,
    notes: renderConferenceNotes,
  });

  $('#group-container').on('shown.bs.tab', 'ul.nav-tabs li a', function (e) {
    activeTab = $(e.target).data('tabIndex');
  });

  $('#group-container').on('submit', 'form.search-form', filterPapers);
  $('#group-container').on('keyup', 'form.search-form .search-content input', _.debounce(filterPapers, 300));

}).fail(function() {
  displayError();
});

