// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'ACM.org/SIGIR/Badging';
var SUBMISSION_ID = CONFERENCE_ID + '/-/Submission';

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};

var initialPageLoad = true;

HEADER_TEXT = 'ACM SIGIR Author Console';

INSTRUCTIONS = '<p><strong>Questions or Concerns</strong></p>\
    <p>Please contact the OpenReview support team at \
    <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform.<br/>\
    </p>';

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

  // Show first available tab
  if (initialPageLoad) {
    $('.tabs-container ul.nav-tabs li a:visible').eq(0).click();
    initialPageLoad = false;
  }

  Webfield.ui.done();
}

// Go!
main();
