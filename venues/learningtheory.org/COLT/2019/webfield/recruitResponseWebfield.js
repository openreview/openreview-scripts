// Constants
var CONFERENCE_ID = 'learningtheory.org/COLT/2019/Conference';
var HEADER = {
  'title': 'COLT 2019',
  'subtitle': 'Computational Learning Theory',
  'deadline': 'Submission Deadline: 11:00pm Eastern Standard Time, February 1, 2019',
  'date': 'June 25 - June 28, 2019',
  'website': 'http://learningtheory.org/colt2019/',
  'location': 'Phoenix, Arizona, United States'
}

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#invitation-container', CONFERENCE_ID);  // required

  Webfield.ui.venueHeader(HEADER);

  OpenBanner.venueHomepageLink(CONFERENCE_ID);

  render();
}

function render() {
  var $response = $('#notes');
  $response.empty();

  if (args.response) {
    var accepted = (args.response === 'Yes');

    if (accepted) {
      // Display response text
      var message = 'Thank you for accepting the invitation to review. It will appear a task to write the official review in the Tasks view shortly.';
      $response.append('<div class="panel"><div class="row"><strong>' + message + '</strong></div></div>');
      $response.append([
        '<div class="panel">',
          '<div class="row">',
            '<p>If you do not already have an OpenReview account, please sign up using the address you received this email.</p>',
            '<p>If you have an existing OpenReview account, please ensure that the email address that received this invitation is linked to your <a href="/profile?mode=edit">profile page</a> and has been confirmed.</p>',
            '<p>If you have any questions contact us at info@opereview.net.</p>',
          '</div>',
        '</div>'
      ].join('\n'));
    } else {
      var message = 'You have declined the invitation.';
      $response.append('<div class="panel"><div class="row"><strong>' + message + '</strong></div></div>');
    }
  } else {
    promptError('Response parameter missing');
  }
  Webfield.ui.done();
}

// Go!
main();
