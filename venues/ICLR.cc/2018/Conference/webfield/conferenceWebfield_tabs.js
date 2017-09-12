// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2018/Conference';
var INVITATION = CONFERENCE + '/-/Submission';
var BLIND_INVITATION = CONFERENCE + '/-/Blind_Submission';
var RECRUIT_REVIEWERS = CONFERENCE + '/-/Recruit_Reviewers';
var WILDCARD_INVITATION = CONFERENCE + '/-/.*';
var AC_GROUPS = [
  CONFERENCE + '/Reviewers',
  CONFERENCE + '/Area_Chairs',
  CONFERENCE + '/Program_Chairs'
];
var COMMENT_EXCLUSION = [
  INVITATION,
  RECRUIT_REVIEWERS
];

var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 50;

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
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {pageSize: PAGE_SIZE});
  var submittedNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {pageSize: PAGE_SIZE, tauthor: true});
  var userGroupsP;
  if (!user || _.startsWith(user.id, 'guest_')) {
    userGroupsP = Promise.resolve([]);
  } else {
    userGroupsP = Webfield.get('/groups', {member: user.id}).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE); }
      );
    });
  }

  return $.when(notesP, submittedNotesP, userGroupsP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: "ICLR 2018 Conference Track",
    subtitle: "6th International Conference on Learning Representations",
    location: "Vancouver Convention Center, Vancouver, BC, Canada",
    date: "April 30 - May 3, 2018",
    website: "http://www.iclr.cc",
    instructions: null,  // Add any custom instructions here. Accepts HTML
    deadline: "Submission Deadline: 5:00pm Eastern Standard Time, October 27, 2017"
  });

  Webfield.ui.spinner('#notes');
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(INVITATION, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          load().then(renderContent);
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'All Submitted Papers',
      id: 'all-submitted-papers',
    },
    {
      heading: 'My Submitted Papers',
      id: 'my-submitted-papers',
    },
    {
      heading: 'My Assigned Papers',
      id: 'my-assigned-papers',
    },
    {
      heading: 'My Comments & Reviews',
      id: 'my-comments-reviews',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    overwrite: true
  });
}

function renderContent(allNotes, submittedNotes, userGroups) {
  var data, commentNotes;

  // if (_.isEmpty(userGroups)) {
  //   // If the user isn't part of the conference don't render tabs
  //   $('.tabs-container').hide();
  //   return;
  // }

  commentNotes = [];

  _.forEach(submittedNotes, function(note) {
    if (_.startsWith(note.invitation, CONFERENCE) && !COMMENT_EXCLUSION.includes(note.invitation) && _.isNil(note.ddate)) {
      // TODO: remove this client side filtering when DB query is fixed
      commentNotes.push(note);
    }
  });

  var notes = _.filter(allNotes, function(n) { return n.content['withdrawal'] != 'Confirmed' });

  var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
  assignedNotes = _.filter(notes, function(n) { return _.includes(assignedPaperNumbers, n.number); });

  var authorPaperNumbers = getAuthorPaperNumbersfromGroups(userGroups);
  submittedNotes = _.filter(notes, function(n) { return _.includes(authorPaperNumbers, n.number); });

  // All Submitted Papers tab (only show for admins)
  var submissionListOptions = _.assign(
    {}, paperDisplayOptions, {container: '#all-submitted-papers'}
  );
  Webfield.ui.submissionList(notes, {
    heading: null,
    container: '#all-submitted-papers',
    search: {
      enabled: false,
      //subjectAreas: SUBJECT_AREAS_LIST,
      onResults: function(searchResults) {
        Webfield.ui.searchResults(searchResults, submissionListOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, submissionListOptions);
        if (notes.length === PAGE_SIZE) {
          Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
        }
      }
    },
    displayOptions: paperDisplayOptions,
    fadeIn: false
  });

  if (notes.length === PAGE_SIZE) {
    Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
  }

  // My Submitted Papers tab
  if (submittedNotes.length) {
    Webfield.ui.searchResults(submittedNotes, _.assign(
      {}, paperDisplayOptions, {container: '#my-submitted-papers'}
    ));
  } else {
    $('.tabs-container a[href="#my-submitted-papers"]').parent().hide();
  }

  // My Assigned Papers tab (only show if not empty)
  if (assignedNotes.length) {
    Webfield.ui.searchResults(assignedNotes, _.assign(
      {}, paperDisplayOptions, {container: '#my-assigned-papers'}
    ));
  } else {
    $('.tabs-container a[href="#my-assigned-papers"]').parent().hide();
  }

  // My Comments & Reviews tab (only show if not empty)
  if (commentNotes.length) {
    Webfield.ui.searchResults(commentNotes, _.assign(
      {}, commentDisplayOptions, {container: '#my-comments-reviews', emptyMessage: 'No comments or reviews to display'}
    ));
  } else {
    $('.tabs-container a[href="#my-comments-reviews"]').parent().hide();
  }

  // Show first available tab
  $('.tabs-container ul.nav-tabs li a').eq(0).click();
}


// Helper functions
function getPaperNumbersfromGroups(groups) {
  // Should be customized for the conference
  var re = /^ICLR\.cc\/2018\/Conference\/Paper(\d+)\/(AnonReviewer\d+|Area_Chair)/;
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

function getAuthorPaperNumbersfromGroups(groups) {
  // Should be customized for the conference
  var re = /^ICLR\.cc\/2018\/Conference\/Paper(\d+)\/Authors/;
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

// Go!
main();
