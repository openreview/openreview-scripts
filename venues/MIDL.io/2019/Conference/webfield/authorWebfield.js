// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'MIDL.io/2019/Conference';
var SUBMISSION_ID = CONFERENCE_ID + '/-/Full_Submission';

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};

HEADER_TEXT = 'MIDL 2019 Author Console';

INSTRUCTIONS = ' ';

var SCHEDULE_HTML = '<h4>Submission Period</h4>\
  <p>\
    <ul>\
      <li><strong>Submission deadline: December 13</strong></li>\
      <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>\
      <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>\
      <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
    </ul>\
  </p>\
  <br>\
  <h4>Reviewing Period</h4>\
  <p>\
    <ul>\
      <li><strong>Reviews can be expected on January 28, 2019 </strong></li>\
      <li>During the review period, authors will not be allowed to revise their paper. </li>\
    </ul>\
  </p>\
  <br>\
  <h4>Rebuttal Period</h4>\
  <p>\
    <ul>\
      <li><strong>Rebuttal period ends on February 10, 2019</strong></li>\
      <li>Authors may revise their paper, but revision history will be available to reviewers.</li>\
      <li>Area chairs and reviewers reserve the right to ignore changes which are significant from the original scope of the paper.</li>\
    </ul>\
  </p>\
  <br>'

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required
  Webfield.ui.header(HEADER_TEXT, INSTRUCTIONS);

  renderConferenceTabs();

  load().then(renderContent);

  OpenBanner.venueHomepageLink(CONFERENCE_ID);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {

  var authorNotesP;
  var invitationsP;
  var tagInvitationsP;

  if (!user || _.startsWith(user.id, 'guest_')) {
    authorNotesP = $.Deferred().resolve([]);
    invitationsP = $.Deferred().resolve([]);
    tagInvitationsP = $.Deferred().resolve([]);
  } else {
    authorNotesP = Webfield.get('/notes', {
      'content.authorids': user.profile.id,
      invitation: SUBMISSION_ID
    }).then(function(result) {
      return result.notes;
    });

    invitationsP = Webfield.get('/invitations', {
      invitation: CONFERENCE_ID + '/-/.*',
      invitee: true,
      duedate: true,
      replyto: true,
      details:'replytoNote,repliedNotes'
    }).then(function(result) {return result.invitations;});

    tagInvitationsP = Webfield.get('/invitations', {
      invitation: CONFERENCE_ID + '/-/.*',
      invitee: true,
      duedate: true,
      tags: true,
      details:'repliedTags'
    }).then(function(result) {return result.invitations;});

  }
  return $.when(authorNotesP, invitationsP, tagInvitationsP);
}


// Render functions
function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Author Schedule',
      id: 'author-schedule',
      content: SCHEDULE_HTML
    },
    {
      heading: 'Author Tasks',
      id: 'author-tasks'
    },
    {
      heading: 'Your Submissions',
      id: 'your-submissions',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

var displayTasks = function(invitations, tagInvitations){
  //  My Tasks tab
  var tasksOptions = {
    container: '#author-tasks',
    emptyMessage: 'No outstanding tasks for this conference'
  }
  $(tasksOptions.container).empty();

  // Filter out non-areachair tasks
  var filterFunc = function(inv) {
    return _.some(inv.invitees, function(invitee) { return invitee.indexOf('Authors') !== -1; });
  };

  var authorInvitations = _.filter(invitations, filterFunc);
  var authorTagInvitations = _.filter(tagInvitations, filterFunc);

  Webfield.ui.newTaskList(authorInvitations, authorTagInvitations, tasksOptions)
  $('.tabs-container a[href="#author-tasks"]').parent().show();
}

function renderContent(authorNotes, invitations, tagInvitations) {

  // Author Tasks tab
  displayTasks(invitations, tagInvitations);

  // Your Private Versions and Your Anonymous Versions tabs
  if (authorNotes.length) {
    Webfield.ui.searchResults(
      authorNotes,
      _.assign({}, paperDisplayOptions, {container: '#your-submissions'})
    );
    $('.tabs-container a[href="#your-submissions"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-submissions"]').parent().hide();
  }

  // Toggle various UI elements
  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

  Webfield.ui.done();
}

// Go!
main();
