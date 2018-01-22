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
var WITHDRAWN_INVITATION = CONFERENCE + '/-/Withdrawn_Submission';
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

  var withdrawnNotesP = Webfield.api.getSubmissions(WITHDRAWN_INVITATION, {
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
      group: 'ICLR.cc/2018/Conference',
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
      authorNotesP, tagInvitationsP, withdrawnNotesP
    );
  });

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
      originals can be found in the My Submissions tab, or your OpenReview <a href="/tasks">Tasks page</a>.\
      You can also access the original record of your paper by clicking the "Modifiable Original" \
      link in the discussion forum page of your paper. The PDF in your submission should not contain the names of the authors. </p>\
      <p><strong>Posting Revisions to Submissions:</strong><br>\
      To post a revision to your paper, navigate to the original version, and click on the "Add Revision" button if available. \
      Revisions are not allowed during the formal review process.\
      Revisions on originals propagate all changes to anonymous copies, while maintaining anonymity.</p> \
      <p><strong>Withdrawing Submissions:</strong><br>\
      To withdraw your paper, navigate to the anonymous record of your submission and click on the "Withdraw" button. You will be asked to confirm your withdrawal. \
      Withdrawn submissions before the submission deadline will be removed from public view entirely. \
      Withdrawn submissions after the submission deadline will be de-anonymized and moved to the "Withdrawn Papers" tab.</p> \
      <p><strong>A Note to Reviewers about Bidding:</strong><br> \
      To access the bidding interface, please ensure that your profile is linked to the email address where you received your initial reviewer invitation email. \
      To do this, click on your name at the top right corner of the page, go to your Profile, enter "edit mode," and add your email address. \
      You will also need to confirm your address by pressing the "Confirm" button. This will involve a round-trip email verification.</p>\
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
          promptMessage('Your submission to ICLR 2018 is complete. The list of all current submissions is shown below.');

          load().then(renderContent).then(function() {
            $('.tabs-container a[href="#all-submitted-papers"]').click();
          });
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
      heading: 'Withdrawn Papers',
      id: 'withdrawn-papers',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, submittedNotes, assignedNotePairs, assignedNotes, userGroups, authorNotes, tagInvitations, withdrawnNotes) {
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
    if (!_.includes([INVITATION, RECRUIT_REVIEWERS, WITHDRAWN_INVITATION], note.invitation)) {
      // ICLR specific: Not all conferences will have the withdrawn invitation
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
          '<a href="/group?id=' + pcId + '">ICLR 2018 Program Chair Console</a>',
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
        var blindedSearchResults = searchResults.filter(function(note) {
          return note.invitation === BLIND_INVITATION;
        });
        Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
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

  // Withdrawn Papers tab
  if (withdrawnNotes.length) {
    Webfield.ui.searchResults(
      withdrawnNotes,
      _.assign({}, paperDisplayOptions, {showTags: false, container: '#withdrawn-papers'})
    );
  } else {
    $('.tabs-container a[href="#withdrawn-papers"]').parent().hide();
  }

  // My Submitted Papers tab
  if (authorNotes.length) {
    Webfield.ui.searchResults(
      authorNotes,
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
  // ICLR specific
  var re = /^ICLR\.cc\/2018\/Conference\/Paper(\d+)\/(AnonReviewer\d+|Area_Chair)/;
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

function getAuthorPaperNumbersfromGroups(groups) {
  // ICLR specific
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
