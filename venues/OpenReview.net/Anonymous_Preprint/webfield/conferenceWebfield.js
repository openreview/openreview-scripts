
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE_ID = "OpenReview.net/Anonymous_Preprint";
var SUBMISSION_ID = CONFERENCE_ID + '/-/Submission';
var BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var PAGE_SIZE = 50;

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  renderConferenceHeader();

  renderSubmissionButton();

  renderConferenceTabs();

  load().then(renderContent).then(Webfield.ui.done);
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
          The real name(s) are privately revealed to you and all the co-authors. \
          The PDF in your submission should not contain the names of the authors. </p>\
          <p><strong>Revise your paper:</strong><br>\
          To add a new version of your paper, go to the forum page of your paper and click on the "Revision" button. \
          <p><strong>Withdraw your paper:</strong><br>\
          To withdraw your paper, navigate to the forum page and click on the "Withdraw" button. You will be asked to confirm your withdrawal. \
          Withdrawn submissions will be removed from the system entirely. \
          <p><strong>Questions or Concerns:</strong><br> \
          Please contact the OpenReview support team at \
          <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns. \</br>\</p>',
  });

  Webfield.ui.spinner('#notes', { inline: true });
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(SUBMISSION_ID)
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback function to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission is complete. Check your inbox for a confirmation email. ');
          load().then(renderContent);
        }
      });
    });
}


function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Papers Submitted',
      id: 'all-submissions',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  return Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'replyCount,original',
    includeCount: true
  });
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function renderContent(notesResponse) {

  // Display the list of all submitted papers
  var notes = notesResponse.notes || [];
  var noteCount = notesResponse.count || 0;

  $('#all-submissions').empty();

  var searchResultsListOptions = _.assign({}, paperDisplayOptions, {
    container: '#all-submissions',
    autoLoad: false
  });

  Webfield.ui.submissionList(notes, {
    heading: null,
    container: '#all-submissions',
    search: {
      enabled: true,
      localSearch: false,
      invitation: BLIND_SUBMISSION_ID,
      onResults: function(searchResults) {
        Webfield.ui.searchResults(searchResults, searchResultsListOptions);
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, searchResultsListOptions);
        $('#all-submissions').append(view.paginationLinks(noteCount, PAGE_SIZE, 1));
      }
    },
    displayOptions: paperDisplayOptions,
    autoLoad: false,
    noteCount: noteCount,
    pageSize: PAGE_SIZE,
    onPageClick: function(offset) {
      return Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
        details: 'replyCount,original',
        pageSize: PAGE_SIZE,
        offset: offset
      });
    },
    fadeIn: false
  });

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();
}

// Go!
main();

