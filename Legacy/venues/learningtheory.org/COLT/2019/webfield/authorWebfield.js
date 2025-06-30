// ------------------------------------
// Author Console Webfield
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'learningtheory.org/COLT/2019/Conference';
var SUBMISSION_ID = 'learningtheory.org/COLT/2019/Conference/-/Submission';
var HEADER_TEXT = 'Author console';
var INSTRUCTIONS = '';

var SCHEDULE_HTML = '<h4>Submission Phase (Jan. 11 - Feb. 1)</h4>\
  <p>\
    <ul>\
      <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>\
      <li>Authors may edit their submissions until the end of the submission phase (i.e. the submission deadline).</li>\
    </ul>\
  </p>\
  <h4>Author Feedback (Mar. 22 - Mar. 27)</h4>\
  <p>\
    <ul>\
      <li>Check back later for updates.</li>\
    </ul>\
  </p>\
  <h4>Author Notification (Apr. 17)</h4>\
  <p>\
    <ul>\
      <li>Check back later for updates.</li>\
    </ul>\
  </p>\
  <br>';

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showActionButtons: true,
  showContents: true
};


// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  Webfield.ui.header(HEADER_TEXT, INSTRUCTIONS);

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

  if (!user) {
    authorNotesP = $.Deferred().resolve([]);
    invitationsP = $.Deferred().resolve([]);
    tagInvitationsP = $.Deferred().resolve([]);

  } else {
    authorNotesP = Webfield.get('/notes', {
      'content.authorids': user.profile.id,
      invitation: SUBMISSION_ID,
      details: 'replyCount,writable'
    }).then(function(result) {
      return result.notes;
    });

    invitationsP = Webfield.get('/invitations', {
      invitation: CONFERENCE_ID + '/-/.*',
      invitee: true,
      duedate: true,
      replyto: true,
      details:'replytoNote,repliedNotes'
    }).then(function(result) {
      return _.filter(result.invitations, function(i) {
        return i.id.startsWith(CONFERENCE_ID);
      });
    });

    tagInvitationsP = Webfield.get('/invitations', {
      invitation: CONFERENCE_ID + '/-/.*',
      invitee: true,
      duedate: true,
      tags: true,
      details:'repliedTags'
    }).then(function(result) {
      return result.invitations;
    });
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


function renderContent(authorNotes, invitations, tagInvitations) {
  // Author Tasks tab
  var tasksOptions = {
    container: '#author-tasks',
    emptyMessage: 'No outstanding tasks for this conference'
  }
  $(tasksOptions.container).empty();

  // Filter out non-author tasks
  var filterFunc = function(inv) {
    return _.some(inv.invitees, function(invitee) {
      return invitee.indexOf('Authors') !== -1;
    });
  };
  var authorInvitations = _.filter(invitations, filterFunc);
  var authorTagInvitations = _.filter(tagInvitations, filterFunc);

  Webfield.ui.newTaskList(authorInvitations, authorTagInvitations, tasksOptions)
  $('.tabs-container a[href="#author-tasks"]').parent().show();

  // Your Private Versions and Your Anonymous Versions tabs
  if (authorNotes.length) {
    Webfield.ui.submissionList(authorNotes, {
      heading: null,
      container: '#your-submissions',
      search: { enabled: false },
      displayOptions: paperDisplayOptions
    });

    $('.tabs-container a[href="#your-submissions"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-submissions"]').parent().hide();
  }

  // Remove spinner and show content
  $('#notes .spinner-container').remove();
  $('.tabs-container').show();
}

// Go!
main();
