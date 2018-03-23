
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE = "OpenReview.net/Anonymous_Preprint";
var SUBMISSION = CONFERENCE + '/-/Submission';
var BLIND_SUBMISSION = CONFERENCE + '/-/Blind_Submission';
var SUBJECT_AREAS = [
  // Add conference specific subject areas here
];
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
    Webfield.setupAutoLoading(BLIND_SUBMISSION, PAGE_SIZE, paperDisplayOptions);
  });
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: "OpenReview.net",
    subtitle: "OpenReview Anonymous Preprint Server",
    location: "Amherst, MA",
    date: "Ongoing",
    website: "https://openreview.net",
    instructions: '<p><strong>Important Information about Anonymity:</strong><br>\
          When you post a submission to this anonymous preprint server, please provide the real names and email addresses of authors in the submission form below.\
          An anonymous record of your paper will appear in the list below, and will be visible to the public. \
          The <em>original</em> record of your submission will be private, and will contain your real name(s); \
          originals can be found in your OpenReview <a href="/tasks">Tasks page</a>.\
          You can also access the original record of your paper by clicking the "Modifiable Original" \
          link in the discussion forum page of your paper. The PDF in your submission should not contain the names of the authors. </p>\
          <p><strong>Posting Revisions to Submissions:</strong><br>\
          To post a revision to your paper, navigate to the original version, and click on the "Add Revision" button. \
          Revisions on originals propagate all changes to anonymous copies, while maintaining anonymity.</p> \
          <p><strong>Withdrawing Submissions:</strong><br>\
          To withdraw your paper, navigate to the anonymous record of your submission and click on the "Withdraw" button. You will be asked to confirm your withdrawal. \
          Withdrawn submissions will be removed from the system entirely. \
          <p><strong>Questions or Concerns:</strong><br> \
          Please contact the OpenReview support team at \
          <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns. \</br>\</p>',
  });

  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(SUBMISSION, {deadlineBuffer: BUFFER});
  var notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION, {pageSize: PAGE_SIZE});
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
          Webfield.setupAutoLoading(BLIND_SUBMISSION, PAGE_SIZE, paperDisplayOptions);
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
        Webfield.setupAutoLoading(BLIND_SUBMISSION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });
}

// Go!
main();

