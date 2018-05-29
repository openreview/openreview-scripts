
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE_ID = 'MIDL.amsterdam/2018/Abstract';
var INVITATION = CONFERENCE_ID + '/-/Submission';
var SUBJECT_AREAS = [
  // Add conference specific subject areas here
];
var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 150;
var DECISION = 'MIDL.amsterdam/2018/Abstract/-/Paper.*/Acceptance_Decision'

var initialPageLoad = true
var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  renderConferenceHeader();
  renderConferenceTabs();

  load().then(render);
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'Medical Imaging with Deep Learning',
    subtitle: 'Conference Track',
    location: 'Amsterdam',
    date: '4-6th July 2018',
    website: 'https://midl.amsterdam',
    instructions: null,  // Add any custom instructions here. Accepts HTML
    deadline: "April 11, 2018, 23:59 CET"
  });

  Webfield.ui.spinner('#notes');
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Accepted Papers',
      id: 'accepted-papers',
    },
    {
      heading: 'Rejected Papers',
      id: 'rejected-papers',
    },
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}
// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(INVITATION, {pageSize:PAGE_SIZE});
  var decisionNotesP = Webfield.api.getSubmissions(DECISION, {
    pageSize:PAGE_SIZE,
    noDetails: true
  });
  return $.when(notesP, decisionNotesP);
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function render(notes, decisionNotes) {
  var notesDict = {};
  _.forEach(notes, function(n) {
    notesDict[n.id] = n;
  });

  var acceptDecisions = [];
  var rejectDecisions = [];

  _.forEach(decisionNotes, function(d) {

    if (d.content.decision === 'Accept') {
      acceptDecisions.push(notesDict[d.forum]);
    } else if (d.content.decision === 'Reject') {
      rejectDecisions.push(notesDict[d.forum]);
    }
  });

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: false,
    showContents: true
  };

  Webfield.ui.searchResults(
    acceptDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#accepted-papers'})
  );

  Webfield.ui.searchResults(
    rejectDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#rejected-papers'})
  );

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

  // Show first available tab
  if (initialPageLoad) {
    $('.tabs-container ul.nav-tabs li a:visible').eq(0).click();
    initialPageLoad = false;
  }
}

// Go!
main();

