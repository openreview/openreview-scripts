// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE = 'MIDL.io/2019/Conference';
var FULL_SUBMISSION = CONFERENCE + '/-/Full_Submission';
var ABSTRACT_SUBMISSION = CONFERENCE + '/Abstract/-/Submission'
var REVIEWERS_NAME = 'Reviewers';
var REVIEWERS_ID = CONFERENCE + '/Reviewers'
var AREA_CHAIRS_NAME = 'Area_Chairs'
var AREA_CHAIRS_ID = CONFERENCE + '/'+AREA_CHAIRS_NAME;
var PROGRAM_CHAIRS_ID = CONFERENCE+'/Program_Chairs';
var AUTHORS_ID = CONFERENCE+'/Authors';
var initialPageLoad = true;

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();
  renderSubmissionButton();
  renderConferenceTabs();

  load().then(renderContent).then(Webfield.ui.done);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var authorNotesP;
  var userGroupsP;

  var notesP = Webfield.getAll('/notes', { invitation: FULL_SUBMISSION, details: 'replyCount' });

  var decisionNotesP = Webfield.getAll('/notes', { invitation: CONFERENCE+'/-/Paper.*/Decision', noDetails: true });

  var abstractsP = Webfield.getAll('/notes', { invitation: ABSTRACT_SUBMISSION, details: 'replyCount' });

  userGroupsP = $.Deferred().resolve([]);
  authorNotesP = $.Deferred().resolve([]);


  return $.when(notesP, decisionNotesP, userGroupsP, authorNotesP, abstractsP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'Medical Imaging with Deep Learning',
    subtitle: 'MIDL 2019 Conference',
    location: 'London',
    date: ' 8-10 July 2019',
    website: 'http://2019.midl.io',
    instructions: '<p>Extended abstracts are up to 3 pages (excluding references and acknowledgements) and can, for example, focus on preliminary novel methodological ideas without extensive validation. We also specifically accept extended abstracts of recently published or submitted journal contributions to give authors the opportunity to present their work and obtain feedback from the community. Selection of abstracts is performed via a lightweight single-blind review process via OpenReview. All accepted abstracts will be presented as posters at the conference.</p><br/> <p><strong>Questions or Concerns</strong></p><p>Please contact the OpenReview support team at <a href=\"mailto:info@openreview.net\">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>    Please contact the MIDL 2019 Program Chairs at <a href=\"mailto:program-chairs@midl.io\">program-chairs@midl.io</a> with any questions or concerns about conference administration or policy.</p><p>We are aware that some email providers inadequately filter emails coming from openreview.net as spam so please check your spam folder regularly.</p>'
   });

  Webfield.ui.spinner('#notes');
}

function renderSubmissionButton() {
  $('#invitation').append([
    '<h4>',
      '<a href="/group?id=MIDL.io/2019/Conference/Abstract">MIDL 2019 Conference Abstract Submisison</a>',
    '</h4>'
  ].join(''));
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Your Consoles',
      id: 'your-consoles',
    },
    {
      heading: 'Abstract Submissions',
      id: 'abstract-papers',
    },
    {
      heading: 'Full - Accept (Oral)',
      id: 'accepted-oral-papers',
    },
    {
      heading: 'Full - Accept (Poster)',
      id: 'accepted-poster-papers',
    },
    {
      heading: 'Full Submissions',
      id: 'all-papers',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, decisionsNotes, userGroups, authorNotes, abstracts) {

  // Your Consoles tab
  if (userGroups.length || authorNotes.length) {

    var $container = $('#your-consoles').empty();
    $container.append('<ul class="list-unstyled submissions-list">');

    if (_.includes(userGroups, PROGRAM_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + PROGRAM_CHAIRS_ID + '">Program Chair Console</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, AREA_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AREA_CHAIRS_ID + '" >',
          AREA_CHAIRS_NAME.replace(/_/g, ' ') + ' Console',
          '</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, REVIEWERS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + REVIEWERS_ID + '" >',
          REVIEWERS_NAME.replace(/_/g, ' ') + ' Console',
          '</a>',
        '</li>'
      ].join(''));
    }

    if (authorNotes.length) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AUTHORS_ID + '">Author Console</a>',
        '</li>'
      ].join(''));
    }

    $('.tabs-container a[href="#your-consoles"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-consoles"]').parent().hide();
  }

  var notesDict = {};
  _.forEach(notes, function(n) {
    notesDict[n.id] = n;
  });

  var abstractsDict = {};
  _.forEach(abstracts, function(n) {
    abstractsDict[n.id] = n;
  });

  var oralDecisions = [];
  var posterDecisions = [];
  var submittedPapers = [];
  var abstractPapers = [];

  _.forEach(decisionsNotes, function(d) {

    if (_.has(notesDict, d.forum)) {
      if (d.content.decision === 'Accept') {
        if (d.content.presentation === 'Oral') {
            oralDecisions.push(notesDict[d.forum]);
        } else if (d.content.presentation === 'Poster'){
            posterDecisions.push(notesDict[d.forum]);
        }
      }
      submittedPapers.push(notesDict[d.forum]);
    }
  });

  _.forEach(abstracts, function(d) {
      if (_.has(abstractsDict, d.forum)) {
        abstractPapers.push(abstractsDict[d.forum]);
      }
  });

  oralDecisions = _.sortBy(oralDecisions, function(o) { return o.id; });
  posterDecisions = _.sortBy(posterDecisions, function(o) { return o.id; });
  submittedPapers = _.sortBy(submittedPapers, function(o) { return o.id; });
  abstractPapers = _.sortBy(abstractPapers, function(o) { return o.id; });

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true,
    showTags: false
  };

 Webfield.ui.searchResults(
    abstractPapers,
    _.assign({}, paperDisplayOptions, {container: '#abstract-papers'})
  );

  Webfield.ui.searchResults(
    oralDecisions,
    _.assign({}, paperDisplayOptions, {container: '#accepted-oral-papers'})
  );

  Webfield.ui.searchResults(
    posterDecisions,
    _.assign({}, paperDisplayOptions, {container: '#accepted-poster-papers'})
  );

  Webfield.ui.searchResults(
    submittedPapers,
    _.assign({}, paperDisplayOptions, {container: '#all-papers'})
  );

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

}

// Go!
main();
