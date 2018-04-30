var SUBJECT_AREAS_LIST = [];
var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 400;
var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};
var commentDisplayOptions = {
  pdfLink: false,
  replyCount: true,
  showContents: false,
  showParent: true
};
var initialPageLoad = true;

//<CONFERENCE>
//<AREA_CHAIRS>
//<SUBTITLE>
//<TITLE>
//<RECRUIT_REVIEWERS>
//<PROGRAM_CHAIRS>
//<DEADLINE>
//<DATE>
//<BLIND_INVITATION>
//<INSTRUCTIONS>
//<WEBSITE>
//<REVIEWERS>
//<LOCATION>
//<SUBMISSION_INVITATION>
//<CONFERENCE_REGEX>
//<WILDCARD_INVITATION>
//<SUBJECT_AREAS>

var CONFERENCE_REGEX = CONFERENCE.replace('.', '\\.').replace('/','\\/')
var WILDCARD_INVITATION = CONFERENCE + '/-/.*';

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required
  renderConferenceHeader();
  renderSubmissionButton();
  renderConferenceTabs();
  load().then(renderContent);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {
    pageSize: PAGE_SIZE
  });

  var submittedNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: PAGE_SIZE,
    tauthor: true
  });

  var assignedNotePairsP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: 100,
    invitee: true,
    duedate: true
  });

  var userGroupsP;
  var authorNotesP;
  if (!user || _.startsWith(user.id, 'guest_')) {
    userGroupsP = $.Deferred().resolve([]);
    authorNotesP = $.Deferred().resolve([]);

  } else {
    userGroupsP = Webfield.get('/groups', {member: user.id}).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE); }
      );
    });

    authorNotesP = Webfield.get('/notes/search', {
      term: user.profile.id,
      group: CONFERENCE,
      content: 'authors',
      source: 'forum'
    }).then(function(result) {
      return result.notes;
    });
  }

  var tagInvitationsP = Webfield.api.getTagInvitations(BLIND_INVITATION);

  return userGroupsP
  .then(function(userGroups) {

    var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
    var assignedNotesP = $.Deferred().resolve([]);

    if (assignedPaperNumbers.length) {
        assignedNotesP = Webfield.api.getSubmissions(BLIND_INVITATION, {
        pageSize: PAGE_SIZE,
        number: assignedPaperNumbers.join()
      });
    }

    return $.when(
      notesP, submittedNotesP, assignedNotePairsP, assignedNotesP, userGroups,
      authorNotesP, tagInvitationsP
    );
  });

}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: TITLE,
    subtitle: SUBTITLE,
    location: LOCATION,
    date: DATE,
    website: WEBSITE,
    instructions: INSTRUCTIONS,
    deadline: DEADLINE
  });

  Webfield.ui.spinner('#notes');
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(SUBMISSION_INVITATION, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission to ' + TITLE + ' is complete.');

          load().then(renderContent).then(function() {
            $('.tabs-container a[href="#my-submitted-papers"]').click();
          });
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'My Tasks',
      id: 'my-tasks',
    },
    {
      heading: 'My Submitted Papers',
      id: 'my-submitted-papers',
    },
    {
      heading: 'My Papers Under Review',
      id: 'my-papers-under-review',
    },
    {
      heading: 'My Assigned Papers',
      id: 'my-assigned-papers',
    },
    {
      heading: 'My Comments & Reviews',
      id: 'my-comments-reviews',
    },
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, submittedNotes, assignedNotePairs, assignedNotes, userGroups, authorNotes, tagInvitations) {
  console.log('userGroups', userGroups);

  var data, commentNotes;

  // if (_.isEmpty(userGroups)) {
  //   // If the user isn't part of the conference don't render tabs
  //   $('.tabs-container').hide();
  //   return;
  // }

  commentNotes = [];
  _.forEach(submittedNotes, function(note) {
    if (!_.isNil(note.ddate)) {
      return;
    }
    if (!_.includes([SUBMISSION_INVITATION, RECRUIT_REVIEWERS], note.invitation)) {
      commentNotes.push(note);
    }
  });

  // Filter out all tags that belong to other users (important for bid tags)
  notes = _.map(notes, function(n) {
    n.tags = _.filter(n.tags, function(t) {
      return !_.includes(t.signatures, user.id);
    });
    return n;
  });

  var authorNoteIds = _.map(authorNotes, function(n){
    return n.id;
  });
  console.log('authorNoteIds', authorNoteIds);

  var blindNotes = _.filter(notes, function(n){
    return authorNoteIds.includes(n.original)
  });

  console.log('blindNotes', blindNotes);

  var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
  if (assignedPaperNumbers.length !== assignedNotes.length) {
    console.warn('WARNING: The number of assigned notes returned by API does not ' +
      'match the number of assigned note groups the user is a member of.');
  }

  var authorPaperNumbers = getAuthorPaperNumbersfromGroups(userGroups);
  if (authorPaperNumbers.length !== authorNotes.length) {
    console.warn('WARNING: The number of submitted notes returned by API does not ' +
      'match the number of submitted note groups the user is a member of.');
  }

  var submissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: true,
    tagInvitations: tagInvitations,
    container: '#my-submitted-papers'
  });

  // MLS: Removing this because there won't be any users that submit more than a couple papers.
  // if (notes.length === PAGE_SIZE) {
  //   Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
  // }

  // My Tasks tab
  if (userGroups.length) {
    var tasksOptions = {
      container: '#my-tasks',
      emptyMessage: 'No outstanding tasks for ' + TITLE
    }
    Webfield.ui.taskList(assignedNotePairs, tagInvitations, tasksOptions)

    // Custom links for UAI
    var acId = CONFERENCE + '/Senior_Program_Committee';
    if (_.includes(userGroups, acId)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + acId + '">UAI 2018 Area Chair Console</a>',
        '</li>'
      ].join(''));
    }

     // Custom links for UAI
    var pcId = 'auai.org/UAI/2018/Program_Chairs';
    if (_.includes(userGroups, pcId)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + pcId + '">UAI 2018 Program Chairs Console</a>',
        '</li>'
      ].join(''));
    }

  } else {
    $('.tabs-container a[href="#my-tasks"]').parent().hide();
  }

  // All Submitted Papers tab
  // Webfield.ui.submissionList(notes, {
  //   heading: null,
  //   container: '#my-papers-under-review',
  //   search: {
  //     enabled: false,
  //     subjectAreas: SUBJECT_AREAS_LIST,
  //     onResults: function(searchResults) {
  //       var blindedSearchResults = searchResults.filter(function(note) {
  //         return note.invitation === BLIND_INVITATION;
  //       });
  //       Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
  //       Webfield.disableAutoLoading();
  //     },
  //     onReset: function() {
  //       Webfield.ui.searchResults(notes, submissionListOptions);
  //       if (notes.length === PAGE_SIZE) {
  //         Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
  //       }
  //     }
  //   },
  //   displayOptions: submissionListOptions,
  //   fadeIn: false
  // });

  // My Papers Under Review tab
  Webfield.ui.searchResults(
    blindNotes,
    _.assign({}, paperDisplayOptions, {
      container: '#my-papers-under-review',
      emptyMessage: 'You have no papers currently under review.'
    })
  );

  // My Submitted Papers tab

  Webfield.ui.searchResults(
    authorNotes,
    _.assign({}, paperDisplayOptions, {
      container: '#my-submitted-papers',
      emptyMessage: 'You have not submitted any papers.'
    })
  );


  // My Assigned Papers tab (only show if not empty)
  if (assignedNotes.length) {
    Webfield.ui.searchResults(
      assignedNotes,
      _.assign({}, paperDisplayOptions, {container: '#my-assigned-papers'})
    );
  } else {
    $('.tabs-container a[href="#my-assigned-papers"]').parent().hide();
  }

  // My Comments & Reviews tab (only show if not empty)
  if (commentNotes.length) {
    Webfield.ui.searchResults(
      commentNotes,
      _.assign({}, commentDisplayOptions, {
        container: '#my-comments-reviews',
        emptyMessage: 'No comments or reviews to display'
      })
    );
  } else {
    $('.tabs-container a[href="#my-comments-reviews"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

  // Show first available tab
  if (initialPageLoad) {
    $('.tabs-container ul.nav-tabs li a:visible').eq(0).click();
    initialPageLoad = false;
  }
}

// Helper functions
function getPaperNumbersfromGroups(groups) {
  var re = new RegExp('^' + CONFERENCE_REGEX + '\/Paper([0-9]+)\/(AnonReviewer[0-9]+|Area_Chair)');
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

function getAuthorPaperNumbersfromGroups(groups) {
  var re = new RegExp('^' + CONFERENCE_REGEX + '\/Paper(\d+)\/Authors');
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

function getDueDateStatus(date) {
  var day = 24 * 60 * 60 * 1000;
  var diff = Date.now() - date.getTime();

  if (diff > 0) {
    return 'expired';
  }
  if (diff > -3 * day) {
    return 'warning';
  }
  return ;
}

// Go!
main();
