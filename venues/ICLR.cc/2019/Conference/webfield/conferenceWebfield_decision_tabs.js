// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2019/Conference';
var INVITATION = CONFERENCE + '/-/Submission';
var BLIND_INVITATION = CONFERENCE + '/-/Blind_Submission';
var WITHDRAWN_INVITATION = CONFERENCE + '/-/Withdrawn_Submission';

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
  var notesP = Webfield.getAll('/notes', { invitation: BLIND_INVITATION, details: 'replyCount' });

  var withdrawnNotesP = Webfield.getAll('/notes', { invitation: WITHDRAWN_INVITATION, noDetails: true });

  var decisionNotesP = Webfield.getAll('/notes', { invitation: 'ICLR.cc/2019/Conference/-/Paper.*/Meta_Review', noDetails: true });

  return $.when(notesP, withdrawnNotesP, decisionNotesP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'ICLR 2019',
    subtitle: 'International Conference on Learning Representations',
    location: 'New Orleans, Louisiana, United States',
    date: 'May 6 - May 9, 2019',
    website: 'https://iclr.cc/Conferences/2019',
    instructions: '<p><strong>Questions or Concerns</strong></p>\
      <p>Please contact the OpenReview support team at \
      <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>\
      Please contact the ICLR 2019 Program Chairs at \
      <a href="mailto:iclr2019programchairs@googlegroups.com">iclr2019programchairs@googlegroups.com</a> with any questions or concerns about conference administration or policy.\
      </p>'
  });

  Webfield.ui.spinner('#notes');
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Oral Presentations',
      id: 'accepted-oral-papers',
    },
    {
      heading: 'Poster Presentations',
      id: 'accepted-poster-papers',
    },
    {
      heading: 'Submitted Papers',
      id: 'rejected-papers',
    },
    {
      heading: 'Withdrawn Papers',
      id: 'withdrawn-papers',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, withdrawnNotes, decisionsNotes) {

  var notesDict = {};
  _.forEach(notes, function(n) {
    notesDict[n.id] = n;
  });

  var oralDecisions = [];
  var posterDecisions = [];
  var rejectDecisions = [];

  _.forEach(decisionsNotes, function(d) {

    if (_.has(notesDict, d.forum)) {
      if (d.content.recommendation === 'Accept (Oral)') {
        oralDecisions.push(notesDict[d.forum]);
      } else if (d.content.recommendation === 'Accept (Poster)') {
        posterDecisions.push(notesDict[d.forum]);
      } else if (d.content.recommendation === 'Reject') {
        rejectDecisions.push(notesDict[d.forum]);
      }
    }
  });

  oralDecisions = _.sortBy(oralDecisions, function(o) { return o.id; });
  posterDecisions = _.sortBy(posterDecisions, function(o) { return o.id; });
  rejectDecisions = _.sortBy(rejectDecisions, function(o) { return o.id; });
  withdrawnNotes = _.sortBy(withdrawnNotes, function(o) { return o.id; });

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true
  };

  Webfield.ui.searchResults(
    oralDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#accepted-oral-papers'})
  );

  Webfield.ui.searchResults(
    posterDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#accepted-poster-papers'})
  );

  Webfield.ui.searchResults(
    rejectDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#rejected-papers'})
  );

  Webfield.ui.searchResults(
    withdrawnNotes,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#withdrawn-papers'})
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
