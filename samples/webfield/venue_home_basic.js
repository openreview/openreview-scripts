// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header, the submit button, and a list
// of all submitted papers.
// ------------------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2017/conference';
var INVITATION = CONFERENCE + '/-/submission';

var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 100;

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container');  // required

  renderConferenceHeader();

  load().then(render).then(function() {
    Webfield.setupAutoLoading(INVITATION, PAGE_SIZE);
  });
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'ICLR 2017 - Conference Track',
    subtitle: 'International Conference on Learning Representations',
    location: 'Toulon, France',
    date: 'April 24 - 26, 2017',
    website: 'http://www.iclr.cc',
    instructions: null,  // Add any custom instructions here. Accepts HTML
    deadline: 'Submission Deadline Extended: Saturday, November 5th, 2016, at 5:00pm Eastern Daylight Time (EDT)'
  });

  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(INVITATION, {deadlineBuffer: BUFFER});
  var notesP = Webfield.api.getSubmissions(INVITATION, {limit: PAGE_SIZE});

  return $.when(invitationP, notesP);
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function render(invitation, notes) {
  // Display submission button and form
  $('#invitation').empty();
  Webfield.ui.submissionButton(invitation, user, {
    onNoteCreated: function() {
      // Callback funtion to be run when a paper has successfully been submitted (required)
      load().then(render);
    }
  });

  // Display the list of all submitted papers
  $('#notes').empty();
  Webfield.ui.notesList(notes, {
    heading: 'Submitted Papers',
    pdfLink: true,
    replyCount: true
  });
}

// Go!
main();
