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
var SUBJECT_AREAS_LIST = [];

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
var initialPageLoad = true;

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

  var assignedNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: 100,
    invitee: true,
    duedate: true
  });

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

  var tagInvitationsP = Webfield.api.getTagInvitations(BLIND_INVITATION);

  return $.when(notesP, submittedNotesP, assignedNotesP, userGroupsP, tagInvitationsP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'ICLR 2018 Conference Track',
    subtitle: '6th International Conference on Learning Representations',
    location: 'Vancouver Convention Center, Vancouver, BC, Canada',
    date: 'April 30 - May 3, 2018',
    website: 'http://www.iclr.cc',
    instructions: '<p><strong>Important Information about Anonymity:</strong><br>\
      When you post a submission to ICLR 2018, please provide the real names and email addresses of authors in the submission form below.\
      An anonymous record of your paper will appear in the "All Submitted Papers" tab, and will be visible to the public. \
      The <em>original</em> record of your submission will be private, and will contain your real name(s); \
      originals can be found in your OpenReview <a href="/tasks">Tasks page</a>.\
      You can also access the original record of your paper by clicking the "Modifiable Original" \
      link in the discussion forum page of your paper. The PDF in your submission should not contain the names of the authors. </p>\
      <p><strong>Posting Revisions to Submissions:</strong><br>\
      To post a revision to your paper, navigate to the original version, and click on the "Add Revision" button if available. \
      Revisions are not allowed during the formal review process.\
      Revisions on originals propagate all changes to anonymous copies, while maintaining anonymity.</p> \
      <p><strong>Questions or Concerns:</strong><br> \
      Please contact the OpenReview support team at \
      <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform. \</br> \
      Please contact the ICLR 2018 Program Chairs at \
      <a href="mailto:iclr2018.programchairs@gmail.com">iclr2018.programchairs@gmail.com</a> with any questions or concerns about conference administration or policy. \</p>',
    deadline: 'Submission Deadline: 5:00pm Eastern Standard Time, October 27, 2017'
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
      heading: 'My Tasks',
      id: 'my-tasks',
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
    },
    {
      heading: 'All Submitted Papers',
      id: 'all-submitted-papers',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(allNotes, submittedNotes, assignedNotePairs, userGroups, tagInvitations) {
  var data, commentNotes;

  // if (_.isEmpty(userGroups)) {
  //   // If the user isn't part of the conference don't render tabs
  //   $('.tabs-container').hide();
  //   return;
  // }

  commentNotes = [];
  _.forEach(submittedNotes, function(note) {
    if (_.startsWith(note.invitation, CONFERENCE) &&
        !COMMENT_EXCLUSION.includes(note.invitation) &&
        _.isNil(note.ddate)) {
      // TODO: remove this client side filtering when DB query is fixed
      commentNotes.push(note);
    }
  });

  // ICLR specific
  var notes = _.filter(allNotes, function(n) {
    return n.content.withdrawal !== 'Confirmed';
  });

  // Filter out all tags that belong to other users (important for bid tags)
  notes = _.map(notes, function(n) {
    n.tags = _.filter(n.tags, function(t) {
      return !_.includes(t.signatures, user.id);
    });
    return n;
  });

  var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
  assignedNotes = _.filter(notes, function(n) {
    return _.includes(assignedPaperNumbers, n.number);
  });

  var authorPaperNumbers = getAuthorPaperNumbersfromGroups(userGroups);
  submittedNotes = _.filter(notes, function(n) {
    return _.includes(authorPaperNumbers, n.number);
  });

  // My Tasks tab
  if (userGroups.length) {
    var tasksOptions = {
      container: '#my-tasks',
      emptyMessage: 'No outstanding tasks for ICLR 2018'
    }
    Webfield.ui.taskList(assignedNotePairs, tagInvitations, tasksOptions)

    // Custom links for ICLR
    var acId = CONFERENCE + '/Area_Chairs';
    if (_.includes(userGroups, acId)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + acId + '">ICLR 2018 Area Chair Console</a>',
        '</li>'
      ].join(''));
    }

    var pcId = CONFERENCE + '/Program_Chairs';
    if (_.includes(userGroups, pcId)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/reviewers?invitation=' + CONFERENCE + '/-/Paper_Assignments&label=reviewers">',
            'ICLR 2018 Reviewer Assignments Browser',
          '</a>',
        '</li>'
      ].join(''));

      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + CONFERENCE + '/Program_Chairs">',
            'ICLR 2018 Program Chair Console',
          '</a>',
        '</li>'
      ].join(''));
    }
  } else {
    $('.tabs-container a[href="#my-tasks"]').parent().hide();
  }

  // All Submitted Papers tab
  var submissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: true,
    tagInvitations: tagInvitations,
    container: '#all-submitted-papers'
  });

  Webfield.ui.submissionList(notes, {
    heading: null,
    container: '#all-submitted-papers',
    search: {
      enabled: true,
      subjectAreas: SUBJECT_AREAS_LIST,
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
    displayOptions: submissionListOptions,
    fadeIn: false
  });

  if (notes.length === PAGE_SIZE) {
    Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
  }

  // My Submitted Papers tab
  if (submittedNotes.length) {
    Webfield.ui.searchResults(
      submittedNotes,
      _.assign({}, paperDisplayOptions, {container: '#my-submitted-papers'})
    );
  } else {
    $('.tabs-container a[href="#my-submitted-papers"]').parent().hide();
  }

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

function getDueDateStatus(date) {
  var day = 24 * 60 * 60 * 1000;
  var diff = Date.now() - date.getTime();

  if (diff > 0) {
    return 'expired';
  }
  if (diff > -3 * day) {
    return 'warning';
  }
  return '';
}

// Go!
main();
