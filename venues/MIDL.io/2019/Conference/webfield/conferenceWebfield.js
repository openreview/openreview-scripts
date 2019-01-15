// ------------------------------------
// Venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'MIDL.io/2019/Conference';
var ABSTRACT_SUBMISSION_ID = 'MIDL.io/2019/Conference/-/Abstract_Submission';
var FULL_SUBMISSION_ID = 'MIDL.io/2019/Conference/-/Full_Submission';
var REVIEWERS_NAME = 'Reviewers';
var AREA_CHAIRS_NAME = 'Area_Chairs';
var AREA_CHAIRS_ID = 'MIDL.io/2019/Conference/Area_Chairs';
var REVIEWERS_ID = 'MIDL.io/2019/Conference/Reviewers';
var PROGRAM_CHAIRS_ID = 'MIDL.io/2019/Conference/Program_Chairs';
var AUTHORS_ID = 'MIDL.io/2019/Conference/Authors';

var HEADER = {"title": "Medical Imaging with Deep Learning", "subtitle": "MIDL 2019 Conference", "location": "London", "date": "8-10 July 2019", "website": "http://2019.midl.io","instructions": "Full papers were due 17th of December 2018. <br/> Extended abstracts are up to 3 pages (excluding references and acknowledgements) and can, for example, focus on preliminary novel methodological ideas without extensive validation. We also specifically accept extended abstracts of recently published or submitted journal contributions to give authors the opportunity to present their work and obtain feedback from the community. Selection of abstracts is performed via a lightweight single-blind review process via OpenReview. <br/> All accepted abstracts will be presented as posters at the conference. <br/><br/> <p><strong>Questions or Concerns</strong></p> <p>Please contact the OpenReview support team at <a href=\"mailto:info@openreview.net\">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/> Please contact the MIDL 2019 Program Chairs at <a href=\"mailto:program-chairs@midl.io\">program-chairs@midl.io</a> with any questions or concerns about conference administration or policy.</p> <p>We are aware that some email providers inadequately filter emails coming from openreview.net as spam so please check your spam folder regularly. </p>", "deadline": "Submission Deadline: 15th of April, 2018, 17:00 UTC", "reviewers_name": "Reviewers", "area_chairs_name": "Area_Chairs", "reviewers_id": "MIDL.io/2019/Conference/Reviewers", "authors_id": "MIDL.io/2019/Conference/Authors", "program_chairs_id": "MIDL.io/2019/Conference/Program_Chairs", "area_chairs_id": "MIDL.io/2019/Conference/Area_Chairs", "submission_id": "MIDL.io/2019/Conference/-/Abstract_Submission"};

var WILDCARD_INVITATION = CONFERENCE_ID + '/-/.*';
var BUFFER = 1000 * 60;  // 1 minutes
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
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  renderConferenceHeader();

  renderSubmissionButton();

  renderConferenceTabs();

  load().then(renderContent).then(Webfield.ui.done);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {

  var activityNotesP;
  var authorNotesP;
  var absAuthorNotesP;
  var userGroupsP;

  var notesP = Webfield.api.getSubmissions(FULL_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'replyCount'
  });

  var ab_notesP = Webfield.api.getSubmissions(ABSTRACT_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'replyCount'
  });

  if (!user || _.startsWith(user.id, 'guest_')) {
    activityNotesP = $.Deferred().resolve([]);
    userGroupsP = $.Deferred().resolve([]);
    authorNotesP = $.Deferred().resolve([]);
    absAuthorNotesP = $.Deferred().resolve([]);
  } else {
    activityNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
      pageSize: PAGE_SIZE,
      details: 'forumContent,writable'
    });

    userGroupsP = Webfield.get('/groups', { member: user.id, web: true }).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE_ID); }
      );
    });

    authorNotesP = Webfield.api.getSubmissions(FULL_SUBMISSION_ID, {
      pageSize: PAGE_SIZE,
      'content.authorids': user.profile.id,
      details: 'noDetails'
    });
    absAuthorNotesP = Webfield.api.getSubmissions(ABSTRACT_SUBMISSION_ID, {
      pageSize: PAGE_SIZE,
      'content.authorids': user.profile.id,
      details: 'noDetails'
    });
  }

  return $.when(notesP, ab_notesP, userGroupsP, activityNotesP, authorNotesP, absAuthorNotesP);
}

// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  Webfield.ui.spinner('#notes', { inline: true });
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(ABSTRACT_SUBMISSION_ID, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission is complete. Check your inbox for a confirmation email. ' +
            'A list of all submissions will be available after the deadline');

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
      heading: 'Full Submissions',
      id: 'full-submissions',
    },
    {
      heading: 'Abstract Submissions',
      id: 'abstract-submissions',
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

function renderContent(full_notes, abs_notes, userGroups, activityNotes, authorNotes, absAuthorNotes) {

  // Your Consoles tab
  if (userGroups.length || authorNotes.length || absAuthorNotes.length) {

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
          '<a href="/group?id=' + AREA_CHAIRS_ID + '" >',
          AREA_CHAIRS_NAME.replace('_', ' ') + ' Console',
          '</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, REVIEWERS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + REVIEWERS_ID + '" >',
          REVIEWERS_NAME.replace('_', ' ') + ' Console',
          '</a>',
        '</li>'
      ].join(''));
    }

    if (authorNotes.length || absAuthorNotes.length) {
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


  // Full Submitted Papers tab
  var submissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: false,
    container: '#full-submissions'
  });

  $(submissionListOptions.container).empty();

  if (full_notes.length){
    Webfield.ui.submissionList(full_notes, {
      heading: null,
      container: '#full-submissions',
      search: {
        enabled: true,
        localSearch: false,
        onResults: function(searchResults) {
          var blindedSearchResults = searchResults.filter(function(note) {
            return note.invitation === FULL_SUBMISSION_ID;
          });
          Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
          Webfield.disableAutoLoading();
        },
        onReset: function() {
          Webfield.ui.searchResults(full_notes, submissionListOptions);
          if (full_notes.length === PAGE_SIZE) {
            Webfield.setupAutoLoading(FULL_SUBMISSION_ID, PAGE_SIZE, submissionListOptions);
          }
        }
      },
      displayOptions: submissionListOptions,
      fadeIn: false
    });

    if (full_notes.length === PAGE_SIZE) {
      Webfield.setupAutoLoading(FULL_SUBMISSION_ID, PAGE_SIZE, submissionListOptions);
    }
  } else {
    $('.tabs-container a[href="#full-submissions"]').parent().hide();
  }

  // Abstract Submitted Papers tab
  var abSubmissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: false,
    container: '#abstract-submissions'
  });

  $(abSubmissionListOptions.container).empty();

  if (abs_notes.length){
    Webfield.ui.submissionList(abs_notes, {
      heading: null,
      container: '#abstract-submissions',
      search: {
        enabled: true,
        localSearch: false,
        onResults: function(searchResults) {
          var blindedSearchResults = searchResults.filter(function(note) {
            return note.invitation === ABSTRACT_SUBMISSION_ID;
          });
          Webfield.ui.searchResults(blindedSearchResults, abSubmissionListOptions);
          Webfield.disableAutoLoading();
        },
        onReset: function() {
          Webfield.ui.searchResults(abs_notes, abSubmissionListOptions);
          if (abs_notes.length === PAGE_SIZE) {
            Webfield.setupAutoLoading(ABSTRACT_SUBMISSION_ID, PAGE_SIZE, abSubmissionListOptions);
          }
        }
      },
      displayOptions: abSubmissionListOptions,
      fadeIn: false
    });

    if (abs_notes.length === PAGE_SIZE) {
      Webfield.setupAutoLoading(ABSTRACT_SUBMISSION_ID, PAGE_SIZE, abSubmissionListOptions);
    }
  } else {
    $('.tabs-container a[href="#abstract-submissions"]').parent().hide();
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
