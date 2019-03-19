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

  load().then(renderContent).then(Webfield.ui.done);
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

function renderContent(notes, withdrawnNotes, decisionsNotes) {

  var notesDict = {};
  _.forEach(notes, function(n) {
    notesDict[n.id] = n;
  });

  var oralDecisions = [];
  var posterDecisions = [];
  var submittedPapers = withdrawnNotes;

  _.forEach(decisionsNotes, function(d) {

    if (_.has(notesDict, d.forum)) {
      if (d.content.recommendation === 'Accept (Oral)') {
        oralDecisions.push(notesDict[d.forum]);
      } else if (d.content.recommendation === 'Accept (Poster)') {
        posterDecisions.push(notesDict[d.forum]);
      } else if (d.content.recommendation === 'Reject') {
        submittedPapers.push(notesDict[d.forum]);
      }
    }
  });

  oralDecisions = _.sortBy(oralDecisions, function(o) { return o.id; });
  posterDecisions = _.sortBy(posterDecisions, function(o) { return o.id; });
  submittedPapers = _.sortBy(submittedPapers, function(o) { return o.id; });

  var papers = {
    'accepted-oral-papers': oralDecisions,
    'accepted-poster-papers': posterDecisions,
    'rejected-papers': submittedPapers
  }
  
  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true
  };

  var activeTab = 0;
  var loadingContent = Handlebars.templates.spinner({ extraClasses: 'spinner-inline' });
  var sections = [
    {
      heading: 'Oral Presentations',
      id: 'accepted-oral-papers',
      content: null
    },
    {
      heading: 'Poster Presentations',
      id: 'accepted-poster-papers',
      content: loadingContent
    },
    {
      heading: 'Submitted Papers',
      id: 'rejected-papers',
      content: loadingContent
    }
  ];

  sections[activeTab].active = true;

  $('#notes .tabs-container').remove();

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });

  $('#group-container').on('shown.bs.tab', 'ul.nav-tabs li a', function(e) {
    activeTab = $(e.target).data('tabIndex');
    var containerId = sections[activeTab].id;

    setTimeout(function() {
      Webfield.ui.searchResults(
        papers[containerId],
        _.assign({}, paperDisplayOptions, {showTags: false, container: '#' + containerId})
      );
    }, 100);
  });

  $('#group-container').on('hidden.bs.tab', 'ul.nav-tabs li a', function(e) {
    var containerId = $(e.target).attr('href');
    Webfield.ui.spinner(containerId, {inline: true});
  });  

  Webfield.ui.searchResults(
    oralDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#accepted-oral-papers'})
  );

  $('#notes > .spinner-container').remove();
  $('.tabs-container').show();

}

// Go!
main();
