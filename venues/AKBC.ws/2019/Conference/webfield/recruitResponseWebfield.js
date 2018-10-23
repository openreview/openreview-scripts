// Constants
var CONFERENCE_ID = 'AKBC.ws/2019/Conference'
var HEADER = {
  title: 'AKBC 2019',
  subtitle: 'Automated Knowledge Base Construction',
  location: 'Amherst, Massachusetts, United States',
  date: 'May 20 - May 21, 2019',
  website: 'http://www.akbc.ws/2019/',
  instructions: '<p><strong>Questions or Concerns</strong><br> \
  Please contact the AKBC 2019 Program Chairs at \
  <a href="mailto:info@akbc.ws">info@akbc.ws</a> with any questions or concerns about conference administration or policy. </br>\
  Please contact the OpenReview support team at \
  <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform. </p>',
  deadline: 'Paper Submission Deadline: November 16, 2019'
}

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#invitation-container', CONFERENCE_ID);  // required
  renderConferenceHeader();
  render();
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  Webfield.ui.spinner('#notes', { inline: true });
}

function render() {
  var accepted = args.response === 'Yes';
  var message = accepted ?
    'Thank you for accepting the invitation!' :
    'You have declined the invitation.';

  var $response = $('#notes');
  $response.empty().append('<div class="panel"><div class="row"><strong>' + message + '</strong></div></div>');

  if (accepted) {
    // Display response text
    $response.append([
      '<div class="panel">',
        '<div class="row">',
          '<p>If you do not already have an OpenReview account, please sign up <a href="/signup">here</a>.</p>',
          '<p>If you have an existing OpenReview account, please ensure that the email address that received this invitation is linked to your <a href="/profile?mode=edit">profile page</a> and has been confirmed.</p>',
        '</div>',
      '</div>'
    ].join('\n'));
  }

  Webfield.ui.done();
}

// Go!
main();
