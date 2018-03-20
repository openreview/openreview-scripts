// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2018/Workshop';
var INVITATION = CONFERENCE + '/-/Submission';
var BLIND_INVITATION = CONFERENCE + '/-/Blind_Submission';

var initialPageLoad = true;

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();

  renderConferenceTabs();

  load().then(renderContent);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(INVITATION, { pageSize: 1000 });

  var decisionNotesP = Webfield.api.getSubmissions('ICLR.cc/2018/Workshop/-/Acceptance_Decision', {
    noDetails: true,
    pageSize: 1000
  });

  return $.when(notesP, decisionNotesP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'ICLR 2018 Workshop Track',
    subtitle: '6th International Conference on Learning Representations',
    location: 'Vancouver Convention Center, Vancouver, BC, Canada',
    date: 'April 30 - May 3, 2018',
    website: 'http://www.iclr.cc'
    })
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
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, decisionsNotes) {

  var notesDict = {};
  _.forEach(notes, function(n) {
    notesDict[n.id] = n;
  });

  var acceptDecisions = [];
  var rejectDecisions = [];

  _.forEach(decisionsNotes, function(d) {

    if (d.content.decision === 'Accept') {
      acceptDecisions.push(notesDict[d.forum]);
    } else if (d.content.decision === 'Reject') {
      rejectDecisions.push(notesDict[d.forum]);
    }
  });

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
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
