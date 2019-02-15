
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------


var instructionsHtml = '\
<h3>Getting Started</h3>\
<p class="dark">\
If you would like to use OpenReview for your upcoming Journal, Conference, or Workshop, please fill out and submit the form below. \
Please see the sections below for more details.\
</p>\
<h3>Frequently Asked Questions</h3>\
<h4><em>How much does all this cost?</em></h4>\
<p class="dark">\
OpenReview is free, and will remain free for the foreseeable future. \
</p>\
<h4><em>Can I request features not listed here?</em></h4>\
<p class="dark">\
The options provided in the form describe the most common set of variables that are requested. \
That being said, OpenReview is built for flexibility, and it may be possible for us to accommodate special requests. \
If you have a special request, please describe it in the text box at the end of the request form. \
We are more likely to honor requests that are useful to many conferences, and that we can incorporate into our regular offerings.\
</p>\
<h3>Peer Review Management Options</h3>\
<p class="dark">\
OpenReview offers a suite of peer review management tools and features for conference organizers. \
The set of most commonly requested features is listed below, but \
if you have a specific request, please describe it in the free text field at the end of the form. \
<ul>\
<li><strong>Reviewer Recruitment by Email</strong>: OpenReview can deploy custom recruitment emails to potential reviewers and track which have accepted or declined the invitation.</li>\
<li><strong>Reviewer Bidding for Papers</strong>: OpenReview supports reviewer bidding (i.e. reviewers indicate their preference to review papers).</li>\
<li><strong>Reviewer Recommendations</strong>: OpenReview supports specific reviewer recommendations by members of the conference (e.g. recommendations made by Area Chairs, Program Chairs, or even other Reviewers).</li>\
</ul>\
</p>\
<h3>The OpenReview Paper Matching System</h3>\
<p class="dark">\
OpenReview offers automated paper-reviewer assignment optimization and conflict of interest detection, \
as well as a web interface for browsing, viewing statistics, and modifying the resulting assignments. \
The OpenReview Matching System supports multiple optimization objectives and arbitrary numerical inputs as features for the match. \
If you would like to use the OpenReview Paper Matching System for your conference, please indicate which features you would like to use in the form below. \
Our most commonly used features are described in the following list: \
<ul>\
<li><strong>OpenReview Affinity</strong>: our in-house paper-reviewer affinity model based on TF-IDF vector similarity. </li>\
<li><strong>TPMS</strong>: <a href="http://torontopapermatching.org/webapp/profileBrowser/about_us/">The Toronto Paper Matching System</a>, a third-party affinity model (if selected, conferences are responsible for coordinating with TPMS)</li>\
<li><strong>Reviewer Bid Scores</strong>: Reviewers indicate their preference to review papers, which are then converted to scores.</li>\
<li><strong>Reviewer Recommendation Scores</strong>: Reviewers, Area Chairs, and/or Program Chairs recommend specific reviewers to review papers. These recommendations are then converted to scores according to your specifications.</li>\
</ul>\
</p>\
<h3>Public vs. Private content</h3>\
<p class="dark">\
In terms of the openness of submissions, reviews, and comments, OpenReview offers pre-configured settings \
that describe our most commonly requested permissions. We refer to them below as "Public" and "Private." \
<ul>\
<li><strong>Public</strong> content is visible to anyone who visits OpenReview.</li> \
<li><strong>Private</strong> content is visible only to applicable conference officials. For example, \
Private Reviews and Comments are visible only to the Program Chairs, to the Reviewers (and Area Chairs if applicable) assigned to the reviewed paper, \
and to the paper\'s authors. Private Submissions are visible only to the Program Chairs, all Reviewers, and all Area Chairs.</li>\
</ul>\
If you would like a different set of permissions, please describe the permissions in the free text box at the end of the form.\
</p>\
<h3>Questions or Concerns?</h3> \
<p class="dark">\
Please contact the OpenReview support team at \
<a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns.</p>'

// Constants
var CONFERENCE = "OpenReview.net/Service";
var SUBMISSION = CONFERENCE + '/-/Request_Form';

var SUBJECT_AREAS = [
  // Add conference specific subject areas here
];
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
    Webfield.setupAutoLoading(SUBMISSION, PAGE_SIZE, paperDisplayOptions);
  });
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: "Service Requests",
    subtitle: "Submit requests for conference or workshop management",
    location: "Amherst, MA",
    date: "Ongoing",
    website: "https://openreview.net",
    instructions: instructionsHtml
  });

  Webfield.ui.spinner('#notes');
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.api.getSubmissionInvitation(SUBMISSION, {noDueDate: true});
  var notesP = Webfield.api.getSubmissions(SUBMISSION, {pageSize: PAGE_SIZE});
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
          Webfield.setupAutoLoading(SUBMISSION, PAGE_SIZE, paperDisplayOptions);
        });
      }
    });
  }

  // Display the list of all submitted papers
  $('#notes').empty();
  Webfield.ui.submissionList(notes, {
    heading: 'Submitted Requests',
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
        Webfield.setupAutoLoading(SUBMISSION, PAGE_SIZE, paperDisplayOptions);
      }
    }
  });
}

// Go!
main();

