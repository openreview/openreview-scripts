// ------------------------------------
// Venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019';
var SUBMISSION_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/-/Report';
var BLIND_SUBMISSION_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/-/Report';
var REVIEWERS_NAME = 'Reviewers';
var AREA_CHAIRS_NAME = 'Area_Chairs';
var AREA_CHAIRS_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Area_Chairs';
var REVIEWERS_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Reviewers';
var PROGRAM_CHAIRS_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Program_Chairs';
var AUTHORS_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Authors';

var NEURIPS_SUBMISSION_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/-/NeurIPS_Submission'
var CLAIM_HOLD_ID = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/-/Claim_Hold'
var CLAIM_ID = CONFERENCE_ID+'/-/Claim'

var HEADER = {"title": "NeurIPS 2019 Reproducibility Challenge", "subtitle": null, "location": "Vancouver, Canada", "date": "December 13-14, 2019", "website": "https://reproducibility-challenge.github.io/neurips2019/dates/", "instructions": "<strong>Here are some instructions</strong>", "deadline": "Submission Claims accepted from 2019 Aug 7 to 2019 Nov 1 (GMT)", "reviewers_name": "Reviewers", "area_chairs_name": "Area_Chairs", "reviewers_id": "reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Reviewers", "authors_id": "reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Authors", "program_chairs_id": "reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Program_Chairs", "area_chairs_id": "reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/Area_Chairs", "submission_id": "reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/-/Report", "blind_submission_id": "reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019/-/Report"};

var WILDCARD_INVITATION = CONFERENCE_ID + '/.*';
var BUFFER = 0;  // deprecated
var PAGE_SIZE = 50;

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true,
  showTags: false
};
var commentDisplayOptions = {
  pdfLink: false,
  replyCount: true,
  showContents: false,
  showParent: true
};

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  renderConferenceHeader();

  renderSubmissionButton();

  renderConferenceTabs();

  load().then(renderContent).then(Webfield.ui.done);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {

  var activityNotesP;
  var authorNotesP;
  var userGroupsP;

  var notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
    pageSize: PAGE_SIZE,
    details: 'replyCount,original',
    includeCount: true
  });

  if (!user || _.startsWith(user.id, 'guest_')) {
    activityNotesP = $.Deferred().resolve([]);
    userGroupsP = $.Deferred().resolve([]);
  } else {
    activityNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
      pageSize: PAGE_SIZE,
      details: 'forumContent,writable'
    });

    userGroupsP = Webfield.getAll('/groups', { member: user.id, web: true })
      .then(function(groups) {
        return _.filter(
          _.map(groups, function(g) { return g.id; }),
          function(id) { return _.startsWith(id, CONFERENCE_ID); }
        );
      });
  }

  var neuripsNotesP = Webfield.getAll('/notes', { invitation: NEURIPS_SUBMISSION_ID, details: 'replyCount,original' });
  var claimNotesP = Webfield.getAll('/notes', { invitation: CLAIM_HOLD_ID, noDetails: true });
  var myClaimsP = Webfield.getAll('/notes', { invitation: CLAIM_ID, noDetails: true });
  return $.when(notesP, userGroupsP, activityNotesP, neuripsNotesP, claimNotesP, myClaimsP);
}

// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  Webfield.ui.spinner('#notes', { inline: true });
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(SUBMISSION_ID, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission is complete. Check your inbox for a confirmation email. ' +
            'A list of all submissions will be available after the deadline');

          load().then(renderContent).then(function() {
            $('.tabs-container a[href="#your-consoles"]').click();
          });
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Your Consoles',
      id: 'your-consoles',
    },
    {
      heading: 'Unclaimed',
      id: 'unclaimed',
    },
    {
      heading: 'Claimed',
      id: 'claimed',
    },
    {
      heading: 'All Reports',
      id: 'all-submissions',
    },
    {
      heading: 'Recent Activity',
      id: 'recent-activity',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notesResponse, userGroups, activityNotes, neuripsNotes, claimNotes, myClaims) {

  console.log('userGroups', userGroups);

  // Your Consoles tab
  if (userGroups.length || myClaims.length) {

    var $container = $('#your-consoles').empty();
    $container.append('<ul class="list-unstyled submissions-list">');

    if (_.includes(userGroups, PROGRAM_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + PROGRAM_CHAIRS_ID + '">Program Chair Console</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, AREA_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AREA_CHAIRS_ID + '" >',
          AREA_CHAIRS_NAME.replace(/_/g, ' ') + ' Console',
          '</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, REVIEWERS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + REVIEWERS_ID + '" >',
          REVIEWERS_NAME.replace(/_/g, ' ') + ' Console',
          '</a>',
        '</li>'
      ].join(''));
    }

    console.log('claimNotes', claimNotes);
    if (myClaims.length) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AUTHORS_ID + '">Author Console</a>',
        '</li>'
      ].join(''));
    }

    $('.tabs-container a[href="#your-consoles"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-consoles"]').parent().hide();
  }

  // Unclaimed NeurIPS papers tab
  if (neuripsNotes.length) {
    console.log('neuripsNotes.length', neuripsNotes.length);
    var $unclaimedContainer = $('#unclaimed').empty();
    $unclaimedContainer.append('<ul class="list-unstyled submissions-list">');

    var $claimedContainer = $('#claimed').empty();
    $claimedContainer.append('<ul class="list-unstyled submissions-list">');

    var claimsDict = {};
    _.forEach(claimNotes, function(n) {
      claimsDict[n.forum] = n;
    });

    var paperByClaim = {
      claimed: [],
      unclaimed: []
    };

    _.forEach(neuripsNotes, function(n) {
      if (_.has(claimsDict, n.forum)) {
        paperByClaim['claimed'].push(n);
      }
      else {
        paperByClaim['unclaimed'].push(n);
      }
    });

    console.log('paperByClaim', paperByClaim);

    var unclaimedResultListOptions = _.assign({}, paperDisplayOptions, {
      container: '#unclaimed',
      autoLoad: false
    });

    Webfield.ui.submissionList(paperByClaim['unclaimed'], {
      heading: null,
      container: '#unclaimed',
      search: {
        enabled: true,
        localSearch: false,
        invitation: NEURIPS_SUBMISSION_ID,
        onResults: function(searchResults) {
          Webfield.ui.searchResults(_.filter(searchResults, note=>!_.has(claimsDict, note.forum)), unclaimedResultListOptions);
        },
        onReset: function() {
          Webfield.ui.searchResults(paperByClaim['unclaimed'], unclaimedResultListOptions);
          $('#unclaimed').append(view.paginationLinks(paperByClaim['unclaimed'].length, PAGE_SIZE, 1));
        }
      },
      displayOptions: paperDisplayOptions,
      autoLoad: false,
      noteCount: paperByClaim['unclaimed'].length,
      pageSize: PAGE_SIZE,
      onPageClick: function(offset) {
        return Webfield.api.getSubmissions(NEURIPS_SUBMISSION_ID, {
          details: 'replyCount,original',
          pageSize: PAGE_SIZE,
          offset: offset
        });
      },
      fadeIn: false
    });

    var claimedResultListOptions = _.assign({}, paperDisplayOptions, {
      container: '#claimed',
      autoLoad: false
    });

    Webfield.ui.submissionList(paperByClaim['claimed'], {
      heading: null,
      container: '#claimed',
      search: {
        enabled: true,
        localSearch: false,
        invitation: NEURIPS_SUBMISSION_ID,
        onResults: function(searchResults) {
          Webfield.ui.searchResults(_.filter(searchResults, note=>_.has(claimsDict, note.forum)), claimedResultListOptions);
        },
        onReset: function() {
          Webfield.ui.searchResults(paperByClaim['claimed'], claimedResultListOptions);
          $('#claimed').append(view.paginationLinks(paperByClaim['claimed'].length, PAGE_SIZE, 1));
        }
      },
      displayOptions: paperDisplayOptions,
      autoLoad: false,
      noteCount: paperByClaim['claimed'].length,
      pageSize: PAGE_SIZE,
      onPageClick: function(offset) {
        return Webfield.api.getSubmissions(NEURIPS_SUBMISSION_ID, {
          details: 'replyCount,original',
          pageSize: PAGE_SIZE,
          offset: offset
        });
      },
      fadeIn: false
    });

    $('.tabs-container a[href="#unclaimed"]').parent().show();
    $('.tabs-container a[href="#claimed"]').parent().show();

  } else {
    $('.tabs-container a[href="#unclaimed"]').parent().hide();
    $('.tabs-container a[href="#claimed"]').parent().hide();
  }


  // All Submitted Papers tab
  var notes = notesResponse.notes || [];
  var noteCount = notesResponse.count || 0;

  $('#all-submissions').empty();

  if (noteCount && _.includes(userGroups, PROGRAM_CHAIRS_ID)) {
    var searchResultsListOptions = _.assign({}, paperDisplayOptions, {
      container: '#all-submissions',
      autoLoad: false
    });

    Webfield.ui.submissionList(notes, {
      heading: null,
      container: '#all-submissions',
      search: {
        enabled: true,
        localSearch: false,
        invitation: BLIND_SUBMISSION_ID,
        onResults: function(searchResults) {
          Webfield.ui.searchResults(searchResults, searchResultsListOptions);
        },
        onReset: function() {
          Webfield.ui.searchResults(notes, searchResultsListOptions);
          $('#all-submissions').append(view.paginationLinks(noteCount, PAGE_SIZE, 1));
        }
      },
      displayOptions: paperDisplayOptions,
      autoLoad: false,
      noteCount: noteCount,
      pageSize: PAGE_SIZE,
      onPageClick: function(offset) {
        return Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
          details: 'replyCount,original',
          pageSize: PAGE_SIZE,
          offset: offset
        });
      },
      fadeIn: false
    });
  } else {
    $('.tabs-container a[href="#all-submissions"]').parent().hide();
  }

  // Activity Tab
  if (activityNotes.length) {
    var displayOptions = {
      container: '#recent-activity',
      user: user && user.profile,
      showActionButtons: true
    };

    $(displayOptions.container).empty();

    Webfield.ui.activityList(activityNotes, displayOptions);

    $('.tabs-container a[href="#recent-activity"]').parent().show();
  } else {
    $('.tabs-container a[href="#recent-activity"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();
}

// Go!
main();
