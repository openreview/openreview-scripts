// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2017/conference';
var INVITATION = CONFERENCE + '/-/submission';
var SUBJECT_AREAS = [
  'All',
  'Algorithms: Approximate Inference',
  'Algorithms: Belief Propagation',
  'Algorithms: Distributed and Parallel',
  'Algorithms: Exact Inference',
  'Algorithms: Graph Theory',
  'Algorithms: Heuristics',
  'Algorithms: Lifted Inference',
  'Algorithms: MCMC methods',
  'Algorithms: Optimization',
  'Algorithms: Other',
  'Algorithms: Software and Tools'
  // ...
  // Incomplete list, add more subject areas here
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
// never changes it can be rendered first before everything else is loaded.
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
  var notesP = Webfield.api.getSubmissions(INVITATION, {pageSize: PAGE_SIZE});
  var tagInvitationsP = Webfield.api.getTagInvitations(INVITATION);

  return $.when(invitationP, notesP, tagInvitationsP);
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function render(invitation, notes, tagInvitations) {
  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true,
    showTags: true,
    tagInvitations: tagInvitations
  };

  // Display submission button and form (if invitation is readable)
  $('#invitation').empty();
  if (invitation) {
    Webfield.ui.submissionButton(invitation, user, {
      onNoteCreated: function() {
        // Callback funtion to be run when a paper has successfully been submitted (required)
        load().then(render);
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
        Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });

  // Load more papers when the user reaches the bottom of the page
  Webfield.setupAutoLoading(INVITATION, PAGE_SIZE, paperDisplayOptions);
}

// Go!
main();
