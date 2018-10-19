
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE = 'NIPS.cc/2018/Workshop/IRASL';
var SUBTITLE = '32nd Annual Conference on Neural Information Processing Systems';
var TITLE = 'NIPS 2018 Interpretability and Robustness for Audio, Speech and Language Workshop';
var CONF_DATE_STRING = '8 December, 2018';
var WEBSITE = 'https://irasl.gitlab.io/';
var LOCATION = 'Montreal, Canada';
var SUBMISSION_INVITATION = 'NIPS.cc/2018/Workshop/IRASL/-/Submission';
var BLIND_INVITATION = 'NIPS.cc/2018/Workshop/IRASL/-/Blind_Submission';
var INSTRUCTIONS = 'October 22, 2018, 11:59 pm UTC';
var DEADLINE_STRING = 'October 29, 2018, 11:59 pm UTC';

var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 50;

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();

  load().then(render).then(function() {
    Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, paperDisplayOptions);
  });
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: TITLE,
    subtitle: SUBTITLE,
    location: LOCATION,
    date: CONF_DATE_STRING,
    website: WEBSITE,
    instructions: "Abstract Submission Deadline: "+INSTRUCTIONS,
    deadline: "Conference Submission Deadline: "+DEADLINE_STRING
  });
  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(SUBMISSION_INVITATION, {deadlineBuffer: BUFFER});
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {pageSize: PAGE_SIZE});

  return $.when(invitationP, notesP);
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function render(invitation, notes) {
  // Display submission button and form (if invitation is readable)
  $('#invitation').empty();
  if (invitation) {
    Webfield.ui.submissionButton(invitation, user, {
      onNoteCreated: function() {
        // Callback funtion to be run when a paper has successfully been submitted (required)
        load().then(render).then(function() {
          Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, paperDisplayOptions);
        });
      }
    });
  }

  // Display the list of all submitted papers
  $('#notes').empty();
  Webfield.ui.submissionList(notes, {
    heading: 'Submitted Papers',
    displayOptions: paperDisplayOptions,
    search: {
      enabled: true,
      onResults: function(searchResults) {
        Webfield.ui.searchResults(searchResults, paperDisplayOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, paperDisplayOptions);
        Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });
}

// Go!
main();

