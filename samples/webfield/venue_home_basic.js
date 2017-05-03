// -----------------------------
// Basic venue homepage template
//
// This webfield displays the conference header and a list of all submitted papers.
// -----------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2017/conference';
var INVITATION = CONFERENCE + '/-/submission';

// Main is the entry point to the code and starts everything off
function main() {
  renderConferenceHeader();
  load().then(render);
}

// RenderConferenceHeader just renders the static info at the top of the page
function renderConferenceHeader() {
  Webfield.ui.setup('#group-container');
  Webfield.ui.venueHeader({
    title: 'ICLR 2017 - Conference Track',
    subtitle: 'International Conference on Learning Representations',
    location: 'Toulon, France',
    date: 'April 24 - 26, 2017',
    website: 'http://www.iclr.cc',
    instructions: 'Submission Deadline Extended: Saturday, November 5th, 2016, at 5:00pm Eastern Daylight Time (EDT)'
  });
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var invitationP = Webfield.get('invitations', {id: INVITATION})
    .then(function(result) {
      var valid_invitations = _.filter(result.invitations, function(inv) {
        return inv.duedate > Date.now();
      });
      return valid_invitations[0];
    });

  var notesP = Webfield.get('notes', {invitation: INVITATION})
    .then(function(result) {
      return result.notes;
    });

  return $.when(invitationP, notesP);
}

// Render is called when all the data is finished being loaded from the server
// It also can be called when the page needs to be refreshed, for example when a user
// submits a new paper.
function render(invitation, notes) {
  // Display submission button and form
  $('#invitation').empty();
  Webfield.ui.invitationButton(invitation, onInvitationButtonClicked, { largeLabel: true });
  Webfield.ui.noteEditor(invitation, function() {
    // Callback funtion to be run when a paper has successfully been submitted
    load().then(render);
  });

  // Display the list of all submitted papers
  $('#notes').empty().append(
    '<h2>Submitted Papers</h2>',
    '<hr>'
  );
  Webfield.ui.notesList(notes, { titleLink: true, replyCount: true });
}

// Go!
main();
