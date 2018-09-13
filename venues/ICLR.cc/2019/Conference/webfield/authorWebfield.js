// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
var SUBMISSION_ID = CONFERENCE_ID + '/-/Submission';
var ADD_BID_ID = CONFERENCE_ID + '/-/Add_Bid';
var BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var RECRUIT_REVIEWERS = CONFERENCE_ID + '/-/Recruit_Reviewers';
var RECRUIT_AREA_CHAIRS = CONFERENCE_ID + '/-/Recruit_Area_Chairs';
var WILDCARD_INVITATION = CONFERENCE_ID + '/-/.*';

var ANON_SIGNATORY_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/(AnonReviewer\d+|Area_Chair\d+)/;
var AUTHORS_SIGNATORY_REGEX = /^ICLR\.cc\/2019\/Conference\/Paper(\d+)\/Authors/;

var AREA_CHAIRS_ID = CONFERENCE_ID + '/Area_Chairs';
var REVIEWERS_ID = CONFERENCE_ID + '/Reviewers';
var PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs';

var COMMENT_EXCLUSION = [
  SUBMISSION_ID,
  RECRUIT_REVIEWERS,
  RECRUIT_AREA_CHAIRS
];

var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 50;

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true
};
var commentDisplayOptions = {
  pdfLink: false,
  replyCount: true,
  showContents: false,
  showParent: true
};
var initialPageLoad = true;

HEADER_TEXT = 'ICLR 2019 Author Console';

INSTRUCTIONS_HTML = '\
    <h3>Frequently Asked Questions</h3>\
    <br>\
    <strong>Does OpenReview automatically anonymize PDFs?</strong>\
    <p>\
      No! PDFs are not automatically anonymized. Authors should submit PDFs without author identities.\
    </p> \
    '

var SCHEDULE_HTML = '<h4>Submission Period</h4>\
    <p>\
      <!--<em><strong>Submission deadline: Thursday, September 27</strong></em>:-->\
      <ul>\
        <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>\
        <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>\
      </ul>\
    </p>\
    <!--<p>\
      <em><strong>Please do the following by Monday, October 8</strong></em>:\
      <ul>\
        <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
        <li>Complete the ICLR registration form (found in your Tasks view).</li>\
      </ul>\
    </p>-->\
  <br>\
  <h4>Reviewing Period</h4>\
    <p>\
      <!--<em><strong>Reviews can be expected by Wednesday, October 17</strong></em>:-->\
      <ul>\
        <li>During the review period, authors will not be allowed to revise their paper. </li>\
        <li>Reviews and all discussion take place on the Anonymous Versions of your submitted papers.</li>\
      </ul>\
    </p>\
  <br>\
  <h4>Rebuttal Period</h4>\
    <p>\
      <!--<em><strong>Rebuttal period ends on Friday, October 26</strong></em>:-->\
      <ul>\
        <li>Authors may revise their paper, but revision history will be available to reviewers.</li>\
        <li>Area chairs and reviewers reserve the right to ignore changes which are significant from the original scope of the paper.</li>\
      </ul>\
    </p>\
  <br>'

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  var $panel = $('#group-container');
  $panel.prepend(
    '<div id="header" class="panel"> \
      <h1>' + HEADER_TEXT + '</h1> \
      <p>' + INSTRUCTIONS_HTML + '</p>\
    </div>'
  );

  renderConferenceTabs();

  load().then(renderContent);

  OpenBanner.venueHomepageLink(CONFERENCE_ID);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'all'
  });

  var submittedNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: PAGE_SIZE,
    tauthor: true
  });

  var assignedNotePairsP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: 100,
    invitee: true,
    duedate: true
  });

  var activityNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: PAGE_SIZE,
    details: 'forumContent'
  });

  var userGroupsP;
  var authorNotesP;

  if (!user || _.startsWith(user.id, 'guest_')) {
    userGroupsP = $.Deferred().resolve([]);
    authorNotesP = $.Deferred().resolve([]);

  } else {
    userGroupsP = Webfield.get('/groups', {member: user.id}).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE_ID); }
      );
    });
    authorNotesP = Webfield.get('/notes', {
      'content.authorids': user.profile.id,
      invitation: SUBMISSION_ID
    }).then(function(result) {
      return result.notes;
    });
  }

  var tagInvitationsP = Webfield.api.getTagInvitations(BLIND_SUBMISSION_ID);

  var invitationsP = Webfield.get('/invitations', {
    invitation: WILDCARD_INVITATION,
    pageSize: 100,
    invitee: true,
    duedate: true,
    replyto: true,
    details:'replytoNote,repliedNotes'
  }).then(function(result) {return result.invitations;})

  return userGroupsP
  .then(function(userGroups) {

    var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
    var assignedNotesP = $.Deferred().resolve([]);

    if (assignedPaperNumbers.length) {
        assignedNotesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
        pageSize: PAGE_SIZE,
        number: assignedPaperNumbers.join()
      });
    }


    return $.when(
      notesP, submittedNotesP, assignedNotePairsP, assignedNotesP, userGroups,
      authorNotesP, invitationsP, tagInvitationsP, activityNotesP
    );
  });

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
    // {
    //   heading: 'Your Anonymous Versions',
    //   id: 'your-anonymous-versions',
    // },
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

function renderContent(notes, submittedNotes, assignedNotePairs, assignedNotes, userGroups, authorNotes, invitations, tagInvitations, activityNotes) {
  var commentNotes = [];

  _.forEach(submittedNotes, function(note) {
    if (!_.isNil(note.ddate)) {
      return;
    }
    if (!_.includes(COMMENT_EXCLUSION, note.invitation)) {
      commentNotes.push(note);
    }
    if (note.invitation === SUBMISSION_ID &&
        !_.includes(_.map(authorNotes, function(n){return n.id;}), note.id)) {
      authorNotes.push(note);
    }
  });

  authorNotes = _.sortBy(authorNotes, function(n){return n.cdate;}).reverse();

  // Filter out all tags that belong to other users (important for bid tags)
  notes = _.map(notes, function(n) {
    n.tags = _.filter(n.tags, function(t) {
      return !_.includes(t.signatures, user.id);
    });
    return n;
  });

  var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
  if (assignedPaperNumbers.length !== assignedNotes.length) {
    console.warn('WARNING: The number of assigned notes returned by API does not ' +
      'match the number of assigned note groups the user is a member of.');
  }

  var authorPaperNumbers = getAuthorPaperNumbersfromGroups(userGroups);
  if (authorPaperNumbers.length !== authorNotes.length) {
    console.warn('WARNING: The number of submitted notes returned by API does not ' +
      'match the number of submitted note groups the user is a member of.');
  }

  // Author Tasks tab
  displayTasks(invitations, tagInvitations);

  // Your Private Versions and Your Anonymous Versions tabs
  if (authorNotes.length) {
    Webfield.ui.searchResults(
      authorNotes,
      _.assign({}, paperDisplayOptions, {container: '#your-submissions'})
    );
    // var authorNoteIds = _.map(authorNotes, function(original){
    //   return original.id;
    // });

    // // get blind papers that are authored by this user
    // var anonymousVersions = _.filter(notes, function(note){
    //   return _.includes(authorNoteIds, note.original);
    // });
    //var anonymousVersions = notes;

    // Anonymous Versions
    // Webfield.ui.searchResults(
    //   anonymousVersions,
    //   _.assign({}, paperDisplayOptions, {
    //     container: '#your-anonymous-versions',
    //     emptyMessage: 'You have no papers currently under review.'
    //   })
    // );
    $('.tabs-container a[href="#your-submissions"]').parent().show();
    // $('.tabs-container a[href="#your-anonymous-versions"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-submissions"]').parent().hide();
    // $('.tabs-container a[href="#your-anonymous-versions"]').parent().hide();
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

// Helper functions
function getPaperNumbersfromGroups(groups) {
  return _.map(
    _.filter(groups, function(gid) { return ANON_SIGNATORY_REGEX.test(gid); }),
    function(fgid) { return parseInt(fgid.match(ANON_SIGNATORY_REGEX)[1], 10); }
  );
}

function getAuthorPaperNumbersfromGroups(groups) {
  return _.map(
    _.filter(groups, function(gid) { return AUTHORS_SIGNATORY_REGEX.test(gid); }),
    function(fgid) { return parseInt(fgid.match(AUTHORS_SIGNATORY_REGEX)[1], 10); }
  );
}

function getDueDateStatus(date) {
  var day = 24 * 60 * 60 * 1000;
  var diff = Date.now() - date.getTime();

  if (diff > 0) {
    return 'expired';
  }
  if (diff > -3 * day) {
    return 'warning';
  }
  return '';
}

// Go!
main();
