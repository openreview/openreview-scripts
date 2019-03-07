// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE = 'MIDL.io/2019/Conference';
var INVITATION = CONFERENCE + '/-/Full_Submission';
var SUBMISSION_ID = CONFERENCE + '/-/Abstract_Submission'
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

  renderConferenceTabs();

  load().then(renderContent).then(Webfield.ui.done);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var authorNotesP;
  var userGroupsP;

  var notesP = Webfield.getAll('/notes', { invitation: INVITATION, details: 'replyCount' });

  var decisionNotesP = Webfield.getAll('/notes', { invitation: CONFERENCE+'/-/Paper.*/Decision', noDetails: true });

  if (!user || _.startsWith(user.id, 'guest_')) {
    userGroupsP = $.Deferred().resolve([]);
    authorNotesP = $.Deferred().resolve([]);
  } else {
    userGroupsP = Webfield.get('/groups', { member: user.id, web: true }).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE); }
      );
    });

    authorNotesP = Webfield.api.getSubmissions(INVITATION, {
      'content.authorids': user.profile.id,
      details: 'noDetails'
    });
  }

  return $.when(notesP, decisionNotesP, userGroupsP, authorNotesP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'Medical Imaging with Deep Learning',
    subtitle: 'MIDL 2019 Conference',
    location: 'London',
    date: ' 8-10 July 2019',
    website: 'http://2019.midl.io',
    instructions: 'Full papers contain well-validated applications or methodological developments of deep learning algorithms in medical imaging. There is no strict limit on paper length. However, we strongly recommend keeping full papers at 8 pages (excluding references and acknowledgements). An appendix section can be added if needed with additional details but must be compiled into a single pdf. The appropriateness of using pages over the recommended page length will be judged by reviewers. All accepted papers will be presented as posters with a selection of these papers will also be invited for oral presentation.<br/><br/> <p><strong>Questions or Concerns</strong></p><p>Please contact the OpenReview support team at <a href=\"mailto:info@openreview.net\">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>    Please contact the MIDL 2019 Program Chairs at <a href=\"mailto:program-chairs@midl.io\">program-chairs@midl.io</a> with any questions or concerns about conference administration or policy.</p><p>We are aware that some email providers inadequately filter emails coming from openreview.net as spam so please check your spam folder regularly.</p>'
   });

  Webfield.ui.spinner('#notes');
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Your Consoles',
      id: 'your-consoles',
    },
    {
      heading: 'Full - Accept(Oral)',
      id: 'accepted-oral-papers',
    },
    {
      heading: 'Full - Accept(Poster)',
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

function renderContent(notes, decisionsNotes, userGroups, authorNotes) {

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

  var oralDecisions = [];
  var posterDecisions = [];
  var submittedPapers = [];

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

  oralDecisions = _.sortBy(oralDecisions, function(o) { return o.id; });
  posterDecisions = _.sortBy(posterDecisions, function(o) { return o.id; });
  submittedPapers = _.sortBy(submittedPapers, function(o) { return o.id; });

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
    submittedPapers,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#all-papers'})
  );

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

}

// Go!
main();
