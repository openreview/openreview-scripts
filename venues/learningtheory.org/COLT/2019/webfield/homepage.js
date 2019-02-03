// ------------------------------------
// Venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'learningtheory.org/COLT/2019/Conference';
var SUBMISSION_ID = 'learningtheory.org/COLT/2019/Conference/-/Submission';
var BLIND_SUBMISSION_ID = 'learningtheory.org/COLT/2019/Conference/-/Blind_Submission';
var REVIEWERS_NAME = 'Reviewers';
var AREA_CHAIRS_NAME = 'Program_Committee';
var AREA_CHAIRS_ID = 'learningtheory.org/COLT/2019/Conference/Program_Committee';
var REVIEWERS_ID = 'learningtheory.org/COLT/2019/Conference/Reviewers';
var PROGRAM_CHAIRS_ID = 'learningtheory.org/COLT/2019/Conference/Program_Chairs';
var AUTHORS_ID = 'learningtheory.org/COLT/2019/Conference/Authors';

var instructions = '<strong>Authors: Please see the <a href="http://learningtheory.org/colt2019/call.html">call for papers</a> for detailed submission instructions.</strong><br>\
When you have successfully submitted a paper, a link to your "Author Console" should appear below, in the "Your Consoles" tab.<br>\
Please contact <a href="mailto:info@openreview.net">info@openreview.net</a> for any questions about the platform. For policy-specific questions, please contact the COLT program chairs at <a href="colt2019pc@gmail.com">colt2019pc@gmail.com</a>.\
<br><br>\
<strong>Important Notes about Submitting a Paper:</strong>\
<ul>\
  <li>Unlike at some of the other conferences that have used OpenReview, neither submissions nor the reviewing process will be public.</li>\
  <li>When submitting your paper, you can safely ignore the "readers" field in the submission form (it will be set automatically).</li>\
  <li>In the "signatures" field, most users will have just one valid identity, which will be set automatically. If you have more than one valid identity, you may select the one that you wish to use. Your identity will be revealed only to the Program Committee and Program Chairs. Please contact OpenReview support if you have any questions.</li>\
</ul>\
<strong>Frequently Asked Questions:</strong>\
<ul>\
  <strong>Q: </strong><em>My paper has "COLT 2019 Conference" in its list of readers -- what does that mean?</em>\
  <br>\
  <strong>A: </strong>This is related to the way that OpenReview\'s permission system works. It means that the <em>conference entity itself</em> has permission to see your paper, which it needs in order to perform automated checks and analyses during the course of the reviewing process.\
  <br>\
  <strong>Q: </strong><em>Something I read on OpenReview is different from what I see on the COLT Call for Papers -- what should I do?</em>\
  <br>\
  <strong>A: </strong>The official COLT website should be considered correct at all times. If you notice a discrepancy, please contact OpenReview support.\
  <br>\
</ul>\
<br>'

var HEADER = {
  "title": "COLT 2019",
  "subtitle": "Conference on Learning Theory",
  "location": "Phoenix, Arizona, United States",
  "date": "June 25 - June 28, 2019",
  "website": "http://learningtheory.org/colt2019/",
  "instructions": instructions,
  "deadline": "Submission Deadline: 11:00pm Eastern Standard Time, February 1, 2019",
  "reviewers_name": "Reviewers",
  "area_chairs_name": "Program_Committee",
  "reviewers_id": "learningtheory.org/COLT/2019/Conference/Reviewers",
  "authors_id": "learningtheory.org/COLT/2019/Conference/Authors",
  "program_chairs_id": "learningtheory.org/COLT/2019/Conference/Program_Chairs",
  "area_chairs_id": "learningtheory.org/COLT/2019/Conference/Program_Committee",
  "submission_id": "learningtheory.org/COLT/2019/Conference/-/Submission"
};

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
  var userGroupsP;

  var notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'replyCount,original'
  });

  if (!user || _.startsWith(user.id, 'guest_')) {
    activityNotesP = $.Deferred().resolve([]);
    userGroupsP = $.Deferred().resolve([]);
    authorNotesP = $.Deferred().resolve([]);
  } else {
    activityNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
      pageSize: PAGE_SIZE,
      details: 'forumContent,writable,original'
    });

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

  return $.when(notesP, userGroupsP, activityNotesP, authorNotesP);
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
      heading: 'All Submissions',
      id: 'all-submissions',
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

function renderContent(notes, userGroups, activityNotes, authorNotes) {
  console.log('userGroups', userGroups);
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
    container: '#all-submissions',
    queryParams: {
      details: 'replyCount,original'
    }
  });

  $(submissionListOptions.container).empty();

  if (notes.length && (_.includes(userGroups, PROGRAM_CHAIRS_ID) || _.includes(userGroups, AREA_CHAIRS_ID)) ){
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
