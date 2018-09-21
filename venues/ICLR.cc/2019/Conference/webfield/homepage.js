// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
var SUBMISSION_ID = CONFERENCE_ID + '/-/Submission';
var ADD_BID_ID = CONFERENCE_ID + '/-/Add_Bid';
var BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var RECRUIT_REVIEWERS = CONFERENCE_ID + '/-/Recruit_Reviewers';
var RECRUIT_AREA_CHAIRS = CONFERENCE_ID + '/-/Recruit_Area_Chairs';
var WILDCARD_INVITATION = CONFERENCE_ID + '/-/.*';

var ANON_SIGNATORY_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/(AnonReviewer\d+|Area_Chair\d+)/;
var AUTHORS_SIGNATORY_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/Authors/;

var AREA_CHAIRS_ID = CONFERENCE_ID + '/Area_Chairs';
var REVIEWERS_ID = CONFERENCE_ID + '/Reviewers';
var PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs';
var AUTHORS_ID = CONFERENCE_ID + '/Authors';

var HEADER = {
  title: 'ICLR 2019',
  subtitle: 'International Conference on Learning Representations',
  location: 'New Orleans, Louisiana, United States',
  date: 'May 6 - May 9, 2019',
  website: 'https://iclr.cc/Conferences/2019',
  instructions: '<p><strong>Important note to Authors and Reviewers: Please update your OpenReview profile to have all your recent emails</strong></p>\
    <p><strong>Important Information</strong><br>\
    Note that ICLR 2019 Conference submissions are now open.</p> \
    <p><strong>Questions or Concerns</strong><br> \
    Please contact the OpenReview support team at \
    <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform. \</br> \
    Please contact the ICLR 2019 Program Chairs at \
    <a href="mailto:iclr2019programchairs@googlegroups.com">iclr2019programchairs@googlegroups.com</a> with any questions or concerns about conference administration or policy. \</p>',
  deadline: 'Submission Deadline: 6:00 pm Eastern Standard Time, September 27, 2018'
}

var COMMENT_EXCLUSION = [
  SUBMISSION_ID,
  RECRUIT_REVIEWERS,
  RECRUIT_AREA_CHAIRS
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
var initialPageLoad = true;

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  renderConferenceHeader();

  renderSubmissionButton();

  renderConferenceTabs();

  load().then(renderContent);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'all'
  });

  var activityNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: PAGE_SIZE,
    details: 'forumContent'
  });

  var userGroupsP;

  if (!user || _.startsWith(user.id, 'guest_')) {
    userGroupsP = $.Deferred().resolve([]);

  } else {
    userGroupsP = Webfield.get('/groups', {member: user.id}).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE_ID); }
      );
    });
  }

  var tagInvitationsP = Webfield.api.getTagInvitations(BLIND_SUBMISSION_ID);

  return $.when(
    notesP, userGroupsP, tagInvitationsP, activityNotesP
  );
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  //Webfield.ui.spinner('#notes');
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(SUBMISSION_ID, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission is complete. Check your inbox for a confirmation email. A list of all submissions will be available after the deadline');

          load().then(renderContent).then(function() {
            $('.tabs-container a[href="#your-consoles"]').click();
          });
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Your Consoles',
      id: 'your-consoles',
    },
    // {
    //   heading: 'All Submissions',
    //   id: 'all-submissions',
    // },
    {
      heading: 'Recent Activity',
      id: 'recent-activity',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, userGroups, tagInvitations, activityNotes) {
  // if (_.isEmpty(userGroups)) {
  //   // If the user isn't part of the conference don't render tabs
  //   $('.tabs-container').hide();
  //   return;
  // }

  // Filter out all tags that belong to other users (important for bid tags)
  notes = _.map(notes, function(n) {
    n.tags = _.filter(n.tags, function(t) {
      return !_.includes(t.signatures, user.id);
    });
    return n;
  });

  var authorPaperNumbers = getAuthorPaperNumbersfromGroups(userGroups);

  var submissionActivityNotes = _.filter(activityNotes, function(note) {
    return note.invitation === SUBMISSION_ID;
  });

  // Your Consoles tab
  if (userGroups.length || submissionActivityNotes.length) {

    var $container = $('#your-consoles').empty();
    $container.append('<ul class="list-unstyled submissions-list">');

    if (_.includes(userGroups, PROGRAM_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + PROGRAM_CHAIRS_ID + '">Program Chair Console</a>',
        '</li>'
      ].join(''));
    }

    // Not open yet
    // if (_.includes(userGroups, REVIEWERS_ID) || _.includes(userGroups, AREA_CHAIRS_ID)) {
    //   $('#your-consoles .submissions-list').append([
    //     '<li class="note invitation-link">',
    //       '<a href="/invitation?id=' + ADD_BID_ID + '">Bidding Console</a>',
    //     '</li>'
    //   ].join(''));
    // }

    if (_.includes(userGroups, AREA_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AREA_CHAIRS_ID + '">Area Chair Console</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, REVIEWERS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + REVIEWERS_ID + '" >Reviewer Console</a>',
        '</li>'
      ].join(''));
    }

    if (authorPaperNumbers.length || submissionActivityNotes.length) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AUTHORS_ID + '">Author Console</a>',
        '</li>'
      ].join(''));
    }

    $('.tabs-container a[href="#your-consoles"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-consoles"]').parent().hide();
  }

  // All Submitted Papers tab
  var submissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: false,
    tagInvitations: tagInvitations,
    container: '#all-submissions'
  });

  $(submissionListOptions.container).empty();

  Webfield.ui.submissionList(notes, {
    heading: null,
    container: '#all-submissions',
    search: {
      enabled: true,
      localSearch: false,
      onResults: function(searchResults) {
        var blindedSearchResults = searchResults.filter(function(note) {
          return note.invitation === BLIND_SUBMISSION_ID;
        });
        Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, submissionListOptions);
        if (notes.length === PAGE_SIZE) {
          Webfield.setupAutoLoading(BLIND_SUBMISSION_ID, PAGE_SIZE, submissionListOptions);
        }
      }
    },
    displayOptions: submissionListOptions,
    fadeIn: false
  });

  if (notes.length === PAGE_SIZE) {
    Webfield.setupAutoLoading(BLIND_SUBMISSION_ID, PAGE_SIZE, submissionListOptions);
  }

  // Activity Tab
  if (activityNotes.length) {
    var displayOptions = {
      container: '#recent-activity',
      user: user && user.profile
    };

    $(displayOptions.container).empty();

    Webfield.ui.activityList(activityNotes, displayOptions);

    $('.tabs-container a[href="#recent-activity"]').parent().show();
  } else {
    $('.tabs-container a[href="#recent-activity"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

  // Show first available tab
  if (initialPageLoad) {
    $('.tabs-container ul.nav-tabs li a:visible').eq(0).click();
    initialPageLoad = false;
  }

  Webfield.ui.done();
}

// Helper functions
function getPaperNumbersfromGroups(groups) {
  return _.map(
    _.filter(groups, function(gid) { return ANON_SIGNATORY_REGEX.test(gid); }),
    function(fgid) { return parseInt(fgid.match(ANON_SIGNATORY_REGEX)[1], 10); }
  );
}

function getAuthorPaperNumbersfromGroups(groups) {
  return _.map(
    _.filter(groups, function(gid) { return AUTHORS_SIGNATORY_REGEX.test(gid); }),
    function(fgid) { return parseInt(fgid.match(AUTHORS_SIGNATORY_REGEX)[1], 10); }
  );
}

// Go!
main();
