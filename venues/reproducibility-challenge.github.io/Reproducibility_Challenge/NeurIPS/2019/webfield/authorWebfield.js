// ------------------------------------
// Author Console Webfield
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019';
var SUBMISSION_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/-/Report';
var CLAIM_ID = CONFERENCE_ID+'/-/Claim'
var HEADER = {'title': 'Authors Console'};

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showActionButtons: true,
  showContents: true
};


// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  Webfield.ui.header(HEADER.title, HEADER.instructions);

  renderConferenceTabs();

  load().then(renderContent).then(Webfield.ui.done);

  OpenBanner.venueHomepageLink(CONFERENCE_ID);
}


// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {

  var authorNotesP;
  var invitationsP;
  var tagInvitationsP;
  var claimsP;

  if (!user || _.startsWith(user.id, 'guest_')) {
    authorNotesP = $.Deferred().resolve([]);
    invitationsP = $.Deferred().resolve([]);
    tagInvitationsP = $.Deferred().resolve([]);
    claimsP = $.Deferred().resolve([]);
  } else {
    authorNotesP = Webfield.get('/notes', {
      'content.authorids': user.profile.id,
      invitation: SUBMISSION_ID,
      details: 'replyCount,writable'
    }).then(function(result) {
      return result.notes;
    });

    invitationsP = Webfield.get('/invitations', {
      regex: CONFERENCE_ID + '.*',
      invitee: true,
      duedate: true,
      replyto: true,
      details:'replytoNote,repliedNotes'
    }).then(function(result) {
      return result.invitations;
    });

    tagInvitationsP = Webfield.get('/invitations', {
      regex: CONFERENCE_ID + '.*',
      invitee: true,
      duedate: true,
      tags: true,
      details:'repliedTags'
    }).then(function(result) {
      return result.invitations;
    });

    claimsP = Webfield.get('/notes', {
      'tauthor': user.profile.id,
      invitation: CLAIM_ID,
      details: 'replyCount,writable'
    }).then(function(result) {
      return result.notes;
    });

  }

  return $.when(authorNotesP, invitationsP, tagInvitationsP, claimsP);
}


// Render functions
function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Your Submissions',
      id: 'your-submissions',
      active: true
    },
    {
      heading: 'Author Tasks',
      id: 'author-tasks'
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}


function renderContent(authorNotes, invitations, tagInvitations, authorClaims) {
  // Author Tasks tab
  var tasksOptions = {
    container: '#author-tasks',
    emptyMessage: 'No outstanding tasks for this conference'
  }
  $(tasksOptions.container).empty();

  Webfield.ui.newTaskList(invitations, tagInvitations, tasksOptions);

  // Your Submissions
  // combine claims and reports
   _.forEach(authorNotes, function(n) {
      authorClaims.push(n);
   });

  Webfield.ui.submissionList(authorClaims, {
    heading: null,
    container: '#your-submissions',
    search: { enabled: false },
    displayOptions: paperDisplayOptions
  });

  // Remove spinner and show content
  $('#notes .spinner-container').remove();
  $('.tabs-container').show();
}

// Go!
main();
