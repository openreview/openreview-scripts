// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE = "NIPS.cc/2017/Workshop/Autodiff";
var INVITATION = CONFERENCE + '/-/Submission';
var TAG_INVITATION = CONFERENCE + '/-/Decision';
var SUBJECT_AREAS = [
  // Add conference specific subject areas here
];
var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 50;


// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();

  load().then(render);
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: "NIPS 2017 Autodiff Workshop",
    subtitle: "The future of gradient-based machine learning software and techniques",
    location: "Long Beach, California",
    date: "December 9, 2017",
    website: "https://autodiff-workshop.github.io/",
    instructions: null,  // Add any custom instructions here. Accepts HTML
    deadline: "Submission Deadline: October 28, 2017 at midnight UTC"
  });

  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(INVITATION, {deadlineBuffer: BUFFER});
  var notesP = Webfield.api.getSubmissions(INVITATION, {pageSize: PAGE_SIZE});
  var tagInvitationsP = Webfield.get('/invitations', {id: TAG_INVITATION, tags: true})
    .then(function(result) {
      return result.invitations;
    });

  return $.when(invitationP, notesP, tagInvitationsP);
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function render(invitation, notes, tagInvitations) {
  // Display submission button and form (if invitation is readable)
  $('#invitation').empty();
  if (invitation) {
    Webfield.ui.submissionButton(invitation, user, {
      onNoteCreated: function() {
        // Callback funtion to be run when a paper has successfully been submitted (required)
        load().then(render).then(function() {
          Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
        });
      }
    });
  }

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true,
    showTags: true,
    tagInvitations: tagInvitations
  };

  // Display the list of all submitted papers
  $('#notes').empty();
  Webfield.ui.submissionList(notes, {
    heading: 'Submitted Papers',
    container: '#notes',
    displayOptions: paperDisplayOptions,
    fadeIn: true,
    search: {
      enabled: true,
      subjectAreas: SUBJECT_AREAS,
      onResults: function(searchResults) {
        Webfield.ui.searchResults(searchResults, paperDisplayOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, paperDisplayOptions);
        Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });

  Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
}

// Go!
main();

