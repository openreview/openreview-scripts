
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
//<CONFERENCE>
//<AREA_CHAIRS>
//<SUBTITLE>
//<TITLE>
//<RECRUIT_REVIEWERS>
//<PROGRAM_CHAIRS>
//<DEADLINE>
//<DATE>
//<WEBSITE>
//<REVIEWERS>
//<LOCATION>
//<SUBMISSION_INVITATION>
//<CONFERENCE_REGEX>
//<WILDCARD_INVITATION>
//<SUBJECT_AREAS>


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
    Webfield.setupAutoLoading(SUBMISSION_INVITATION, PAGE_SIZE, paperDisplayOptions);
  });
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: TITLE,
    subtitle: SUBTITLE,
    location: LOCATION,
    date: DATE,
    website: WEBSITE,
    instructions: null,  // Add any custom instructions here. Accepts HTML
    deadline: DEADLINE
  });

  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(SUBMISSION_INVITATION, {deadlineBuffer: BUFFER});
  var notesP = Webfield.api.getSubmissions(SUBMISSION_INVITATION, {pageSize: PAGE_SIZE});

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
          Webfield.setupAutoLoading(SUBMISSION_INVITATION, PAGE_SIZE, paperDisplayOptions);
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
      subjectAreas: SUBJECT_AREAS,
      onResults: function(searchResults) {
        Webfield.ui.searchResults(searchResults, paperDisplayOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, paperDisplayOptions);
        Webfield.setupAutoLoading(SUBMISSION_INVITATION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });
}

// Go!
main();

