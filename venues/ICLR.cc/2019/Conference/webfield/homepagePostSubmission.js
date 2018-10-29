// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header),
// important instructions for this phase of the conference,
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
var SUBMISSION_ID = CONFERENCE_ID + '/-/Submission';
var ADD_BID_ID = CONFERENCE_ID + '/-/Add_Bid';
var BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var WITHDRAWN_SUBMISSION_ID = CONFERENCE_ID + '/-/Withdrawn_Submission';
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
  instructions: '<p><strong>Important Information</strong>\
    <ul>\
    <li>Note to Authors and Reviewers: Please update your OpenReview profile to have all your recent emails.</li>\
    <li>ICLR 2019 Conference submissions are now closed.</li>\
    <li>For more details refer to the <a href="https://iclr.cc/Conferences/2019/CallForPapers">ICLR 2019 - Call for Papers</a>.</li>\
    </ul></p> \
    <p><strong>Questions or Concerns</strong></p>\
    <p>Please contact the OpenReview support team at \
    <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>\
    Please contact the ICLR 2019 Program Chairs at \
    <a href="mailto:iclr2019programchairs@googlegroups.com">iclr2019programchairs@googlegroups.com</a> with any questions or concerns about conference administration or policy.\
    </p>',
  deadline: 'Submission Deadline: 6:00 pm EDT, September 27, 2018'
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

  load().then(renderContent).then(Webfield.ui.done);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'replyCount'
  });

  var withdrawnNotesP = Webfield.api.getSubmissions(WITHDRAWN_SUBMISSION_ID, {
    pageSize: 1000
  });

  var activityNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: PAGE_SIZE,
    details: 'forumContent'
  });

  var userGroupsP;
  var authorNotesP;

  if (!user || _.startsWith(user.id, 'guest_')) {
    userGroupsP = $.Deferred().resolve([]);
    authorNotesP = $.Deferred().resolve([]);

  } else {
    userGroupsP = Webfield.get('/groups', { member: user.id, web: true }).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE_ID); }
      );
    });

    authorNotesP = Webfield.api.getSubmissions(SUBMISSION_ID, {
      pageSize: PAGE_SIZE,
      'content.authorids': user.profile.id,
      details: 'noDetails'
    });
  }

  return $.when(
    notesP, withdrawnNotesP, userGroupsP, activityNotesP, authorNotesP
  );
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  Webfield.ui.spinner('#notes', { inline: true });
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
    {
      heading: 'All Submissions',
      id: 'all-submissions',
    },
    {
      heading: 'Withdrawn Papers',
      id: 'withdrawn-papers',
    },
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

function renderContent(notes, withdrawnNotes, userGroups, activityNotes, authorNotes) {

  // Your Consoles tab
  if (userGroups.length || authorNotes.length) {

    var $container = $('#your-consoles').empty();
    $container.append('<ul class="list-unstyled submissions-list">');

    if (_.includes(userGroups, PROGRAM_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + PROGRAM_CHAIRS_ID + '">Program Chair Console</a>',
        '</li>'
      ].join(''));
    }

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

    if (authorNotes.length) {
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
    container: '#all-submissions'
  });

  $(submissionListOptions.container).empty();

  if (notes.length){
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
  } else {
    $('.tabs-container a[href="#all-submissions"]').parent().hide();
  }

  // Withdrawn Tab
  if (withdrawnNotes.length) {
    Webfield.ui.searchResults(
      withdrawnNotes,
      _.assign({}, paperDisplayOptions, {showTags: false, container: '#withdrawn-papers'})
    );
  } else {
    $('.tabs-container a[href="#withdrawn-papers"]').parent().hide();
  }

  // Activity Tab
  if (activityNotes.length) {
    var displayOptions = {
      container: '#recent-activity',
      user: user && user.profile,
      showActionButtons: true
    };

    $(displayOptions.container).empty();

    Webfield.ui.activityList(activityNotes, displayOptions);

    $('.tabs-container a[href="#recent-activity"]').parent().show();
  } else {
    $('.tabs-container a[href="#recent-activity"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();
}

// Go!
main();
