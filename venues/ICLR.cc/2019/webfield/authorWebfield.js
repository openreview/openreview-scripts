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
    <strong>Why are there two versions of my paper?</strong>\
    <br>\
    <p>\
      OpenReview maintains both anonymity and attributability of papers by storing an "original" \
      version of the paper, complete with full author names and email addresses, as well as an anonymous \
      version of the paper, which protects the authors\' identities during the review process.\
      All reviewing takes place in the discussion page of the anonymous version.\
    </p>\
    <strong>How do I revise my paper after submitting it?</strong>\
    <p>\
      To post a revision to your paper, navigate to the original (non-anonymous) version. If revisions are enabled,\
      an "Add Revision" button will appear, where you can submit your revised paper information.\
      Revisions are not allowed during the formal review process.\
      Revisions on original versions will update anonymous versions, but will not reveal author identities.\
    </p>\
    <strong>Do you automatically anonymize PDFs?</strong>\
    <p>\
      No! PDFs are not automatically anonymized. Authors should submit PDFs without author identities.\
    </p> \
    '

var SCHEDULE_HTML = '<h4>Submission Phase</h4>\
    <p>\
      <em><strong>Submission deadline: Monday, August 3</strong></em>:\
      <ul>\
        <li>You may edit your submissions without edit history any time until the submission deadline.</li>\
        <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>\
      </ul>\
    </p>\
    <p>\
      <em><strong>Please do the following by Friday, August 10</strong></em>:\
      <ul>\
        <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
        <li>Complete the ICLR registration form (found in your Tasks view).</li>\
      </ul>\
    </p>\
  <br>\
  <h4>Reviewing Phase</h4>\
    <p>\
      <em><strong>Reviews can be expected by Friday, August 17</strong></em>:\
      <ul>\
        <li>Once all first-round reviews on your paper have been submitted, you will have the opportunity to respond to them.</li>\
        <li>Reviews and all discussion take place on the Anonymous Versions of your submitted papers.</li>\
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
      <h4><a href="/group?id=ICLR.cc/2019/Conference">\< Back to ICLR 2019 Homepage</a><h4><br>\
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
      authorNotesP, tagInvitationsP, activityNotesP
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
      heading: 'Your Anonymous Versions',
      id: 'your-anonymous-submissions',
    },
    {
      heading: 'Your Private Versions',
      id: 'your-private-versions',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, submittedNotes, assignedNotePairs, assignedNotes, userGroups, authorNotes, tagInvitations, activityNotes) {
  var data, commentNotes;

  console.log('userGroups',userGroups);

  commentNotes = [];

  _.forEach(submittedNotes, function(note) {
    if (!_.isNil(note.ddate)) {
      return;
    }
    if (!_.includes(COMMENT_EXCLUSION, note.invitation)) {
      commentNotes.push(note);
    }
  });

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

  // My Submitted Papers tab
  if (authorNotes.length) {
    Webfield.ui.searchResults(
      authorNotes,
      _.assign({}, paperDisplayOptions, {container: '#your-private-versions'})
    );
    console.log('authorNotes', authorNotes);
    var authorNoteIds = _.map(authorNotes, function(original){
      return original.id;
    });

    console.log('authorNoteIds', authorNoteIds);
    // get blind papers that are authored by this user
    var myPapersUnderReview = _.filter(notes, function(note){
      console.log('note.original', note.original);
      return _.includes(authorNoteIds, note.original);
    });
    //var myPapersUnderReview = notes;
    console.log('myPapersUnderReview',myPapersUnderReview);

    // My Papers Under Review tab
    Webfield.ui.searchResults(
      myPapersUnderReview,
      _.assign({}, paperDisplayOptions, {
        container: '#your-anonymous-submissions',
        emptyMessage: 'You have no papers currently under review.'
      })
    );
    $('.tabs-container a[href="#your-private-versions"]').parent().show();
    $('.tabs-container a[href="#your-anonymous-submissions"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-private-versions"]').parent().hide();
    $('.tabs-container a[href="#your-anonymous-submissions"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

  // Show first available tab
  if (initialPageLoad) {
    $('.tabs-container ul.nav-tabs li a:visible').eq(0).click();
    initialPageLoad = false;
  }
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
