
// ------------------------------------
// Basic venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a list of all submitted papers (#notes).
// ------------------------------------

// Constants
var CONFERENCE_ID = 'auai.org/UAI/2018';

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#invitation-container', CONFERENCE_ID);  // required

  renderConferenceHeader();

  // Webfield.get('/notes', {id: args.noteId}).then(render);
  render();
}

// RenderConferenceHeader renders the static info at the top of the page. Since that content
// never changes, put it in its own function
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'UAI 2018 Conference',
    subtitle: 'Uncertainty in Artificial Intelligence',
    location: 'San Francisco, USA',
    date: 'August 2018',
    website: 'http://auai.org',
    instructions: null,
  });

  Webfield.ui.spinner('#notes');
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
}

// Go!
main();
