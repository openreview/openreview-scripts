
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE = 'NIPS.cc/2018/Workshop/CDNNRIA';
var TITLE = 'NIPS 2018 CDNNRIA Workshop';
var SUBTITLE = 'Compact Deep Neural Network Representation with Industrial Applications';
var DEADLINE_STRING = 'October 31, 2018, 11:59 pm UTC';
var CONF_DATE_STRING = 'December 3-8, 2018';
var WEBSITE = 'https://nips.cc/Conferences/2018/Schedule?showEvent=10941';
var LOCATION = 'Montreal, Canada';
var SUBMISSION_INVITATION = 'NIPS.cc/2018/Workshop/CDNNRIA/-/Submission';
var BLIND_INVITATION = 'NIPS.cc/2018/Workshop/CDNNRIA/-/Blind_Submission';
var INSTRUCTIONS = 'This workshop aims to bring together researchers, educators,\
 practitioners who are interested in techniques as well as applications of making \
 compact and efficient neural network representations. <br/>\
One main theme of the workshop discussion is to build up consensus in this rapidly \
developed field, and in particular, to establish close connection between \
researchers in machine learning community and engineers in industry. \
We believe the workshop is beneficial to both academic researchers as well \
as industrial practitioners.\
<br/><br/>\
Call for submissions: We invite you to submit original work in, but not limited to, \
following areas:<br/>\
<ul><li>Neural network compression techniques</li>\
<li>Neural network representation exchange formats</li>\
<li>Industrial standardization and performance evaluation methods</li>\
<li>Video & media compression methods using DNNs</li></ul>\
Important dates:<br/>\
<ul><li>Extended abstract submission deadline: October 20, 2018</li>\
<li>Acceptance notification: October 29, 2018</li>\
<li>Camera ready submission: November 12, 2018</li>\
<li>Workshop: December 7, 2018</li></ul>\
<br/>\
Submission: Please see workshop homepage at \
<a href="https://nips.cc/Conferences/2018/Schedule?showEvent=10941">\
https://nips.cc/Conferences/2018/Schedule?showEvent=10941</a><br/>';



var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 50;

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();

  load().then(render).then(function() {
    Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, paperDisplayOptions);
  });
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: TITLE,
    subtitle: SUBTITLE,
    location: LOCATION,
    date: CONF_DATE_STRING,
    website: WEBSITE,
    instructions: INSTRUCTIONS,
    deadline: "Submission Deadline: "+DEADLINE_STRING
  });
  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(SUBMISSION_INVITATION, {deadlineBuffer: BUFFER});
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {pageSize: PAGE_SIZE});

  return $.when(invitationP, notesP);
}

// Render is called when all the data is finished being loaded from the server
// It should also be called when the page needs to be refreshed, for example after a user
// submits a new paper.
function render(invitation, notes) {
  // Display submission button and form (if invitation is readable)
  $('#invitation').empty();
  if (invitation) {
    Webfield.ui.submissionButton(invitation, user, {
      onNoteCreated: function() {
        // Callback funtion to be run when a paper has successfully been submitted (required)
        load().then(render).then(function() {
          Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, paperDisplayOptions);
        });
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
      onResults: function(searchResults) {
        Webfield.ui.searchResults(searchResults, paperDisplayOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, paperDisplayOptions);
        Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });
}

// Go!
main();