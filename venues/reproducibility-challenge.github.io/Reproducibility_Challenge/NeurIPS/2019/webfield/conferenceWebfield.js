// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019';
var BLIND_SUBMISSION_ID = '';
var WITHDRAWN_INVITATION = '';
var DECISION_INVITATION_REGEX = '';
var DECISION_HEADING_MAP = {};
var NEURIPS_SUBMISSION_ID = CONFERENCE_ID + '/-/NeurIPS_Submission'
var CLAIM_ID = CONFERENCE_ID + '/-/Claim_Hold'
var REPORT_SUBMISSION_ID = CONFERENCE_ID+'/-/Report_Submission'

var HEADER = {
  title: 'NeurIPS 2019 Reproducibility Challenge',
  deadline: 'Submission Claims Start: August 7, 2019 GMT, End: November 1, 2019 GMT',
  date: 'December 13/14, 2019',
  website: 'https://reproducibility-challenge.github.io/neurips2019/dates/',
  location: 'Vancouver, Canada'
};


// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  renderConferenceHeader();
  renderReportButton();
  load().then(renderContent).then(Webfield.ui.done);
}

// Load makes all the API calls needed to get the data to render the page
function load() {
  var neuripsNotesP = Webfield.getAll('/notes', { invitation: NEURIPS_SUBMISSION_ID, details: 'replyCount,original' });
  var claimNotesP = Webfield.getAll('/notes', { invitation: CLAIM_ID, noDetails: true });
  var reportNotesP = Webfield.getAll('/notes', { invitation: REPORT_SUBMISSION_ID, noDetails: true });
  return $.when(neuripsNotesP, claimNotesP, reportNotesP);
}

function renderConferenceHeader() {
    Webfield.ui.venueHeader(HEADER);

    Webfield.ui.spinner('#notes', { inline: true });
 }

 function getElementId(decision) {
   return decision.replace(' ', '-')
    .replace('(', '')
    .replace(')', '')
    .toLowerCase();
 }

function renderReportButton() {
  Webfield.api.getSubmissionInvitation(REPORT_SUBMISSION_ID)
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your artifact submission is complete. Check your inbox for a confirmation email.');
          load().then(renderContent).then(Webfield.ui.done);
        }
      });
    });
}

function renderContent(neuripsNotes, claimNotes, reportNotes) {

  var claimsDict = {};
  _.forEach(claimNotes, function(n) {
    claimsDict[n.forum] = n;
  });

  var paperByDecision = {};
  var paperByClaim = {
    claimed: [],
    unclaimed: []
  };

  for (var decision in DECISION_HEADING_MAP) {
    paperByDecision[decision] = [];
  }

  _.forEach(neuripsNotes, function(n) {
    if (_.has(claimsDict, n.forum)) {
      paperByClaim['claimed'].push(n);
    }
    else {
      paperByClaim['unclaimed'].push(n);
    }
  });

  console.log('paperByClaim', paperByClaim);

  for (var decision in DECISION_HEADING_MAP) {
    paperByDecision[getElementId(decision)] = _.sortBy(paperByDecision[decision], function(o) { return o.id; });
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
      heading: 'Unclaimed',
      id: 'unclaimed',
      content: loadingContent
    },
    {
      heading: 'Claimed',
      id: 'claimed',
      content: loadingContent
    },
    {
      heading: 'Reports',
      id: 'reports',
      content: loadingContent
    }
  ];

  for (var decision in DECISION_HEADING_MAP) {
    sections.push({
      heading: DECISION_HEADING_MAP[decision],
      id: getElementId(decision),
      content: loadingContent
    });
  }

  sections[activeTab].active = true;
  sections[activeTab].content = null;

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
        paperByClaim[containerId],
        _.assign({}, paperDisplayOptions, {showTags: false, container: '#' + containerId})
      );
    }, 100);
  });

  $('#group-container').on('hidden.bs.tab', 'ul.nav-tabs li a', function(e) {
    var containerId = $(e.target).attr('href');
    Webfield.ui.spinner(containerId, {inline: true});
  });

  if (activeTab == 'claimed' || activeTab == 'unclaimed') {
      Webfield.ui.searchResults(
        paperByClaim[sections[activeTab].id],
        _.assign({}, paperDisplayOptions, {showTags: false, container: '#' + sections[activeTab].id})
      );
  }
  else if (activeTab == 'reports') {
       Webfield.ui.searchResults(
        reportNotes,
        _.assign({}, paperDisplayOptions, {showTags: false, container: '#' + sections[activeTab].id}));
  }

  $('#notes > .spinner-container').remove();
  $('.tabs-container').show();

}

// Go!
main();
