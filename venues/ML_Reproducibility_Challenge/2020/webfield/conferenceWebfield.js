// ------------------------------------
// Venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020';
var SUBMISSION_ID = 'ML_Reproducibility_Challenge/2020/-/Submission';
var BLIND_SUBMISSION_ID = 'ML_Reproducibility_Challenge/2020/-/Blind_Submission';
var WITHDRAWN_SUBMISSION_ID = 'ML_Reproducibility_Challenge/2020/-/Withdrawn_Submission';
var DESK_REJECTED_SUBMISSION_ID = 'ML_Reproducibility_Challenge/2020/-/Desk_Rejected_Submission';
var REVIEWERS_NAME = 'Reviewers';
var AREA_CHAIRS_NAME = 'Area_Chairs';
var AREA_CHAIRS_ID = 'ML_Reproducibility_Challenge/2020/Area_Chairs';
var REVIEWERS_ID = 'ML_Reproducibility_Challenge/2020/Reviewers';
var PROGRAM_CHAIRS_ID = 'ML_Reproducibility_Challenge/2020/Program_Chairs';
var AUTHORS_ID = 'ML_Reproducibility_Challenge/2020/Authors';
var HEADER = {"title": "ML Reproducibility Challenge 2020", "subtitle": "RC2020", "location": null, "date": "Mar 12 2021", "website": "https://paperswithcode.com/rc2020", "instructions": null, "deadline": "Submission Start: Oct 05 2020 12:00AM UTC-0, End: Dec 04 2020 12:00AM UTC-0", "contact": "reproducibility.challenge@gmail.com", "reviewers_name": "Reviewers", "area_chairs_name": "Area_Chairs", "reviewers_id": "ML_Reproducibility_Challenge/2020/Reviewers", "authors_id": "ML_Reproducibility_Challenge/2020/Authors", "program_chairs_id": "ML_Reproducibility_Challenge/2020/Program_Chairs", "area_chairs_id": "ML_Reproducibility_Challenge/2020/Area_Chairs", "submission_id": "ML_Reproducibility_Challenge/2020/-/Submission", "blind_submission_id": "ML_Reproducibility_Challenge/2020/-/Blind_Submission", "withdrawn_submission_id": "ML_Reproducibility_Challenge/2020/-/Withdrawn_Submission", "desk_rejected_submission_id": "ML_Reproducibility_Challenge/2020/-/Desk_Rejected_Submission", "public": false};
var PUBLIC = false;

var CLAIM_HOLD_ID = CONFERENCE_ID + '/-/Claim_Hold';
var CLAIM_ID = CONFERENCE_ID + '/-/Claim';
var ACCEPTED_PAPER_ID = CONFERENCE_ID + '/-/Accepted_Papers';


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

  var notesP = $.Deferred().resolve([]);
  var activityNotesP = $.Deferred().resolve([]);
  var authorNotesP = $.Deferred().resolve([]);
  var userGroupsP = $.Deferred().resolve([]);
  var withdrawnNotesP = $.Deferred().resolve([]);
  var deskRejectedNotesP = $.Deferred().resolve([]);

  if (PUBLIC) {
    notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
      pageSize: PAGE_SIZE,
      details: 'replyCount,invitation,original',
      includeCount: true
    });

    if (WITHDRAWN_SUBMISSION_ID) {
      withdrawnNotesP = Webfield.api.getSubmissions(WITHDRAWN_SUBMISSION_ID, {
        pageSize: PAGE_SIZE,
        details: 'replyCount,invitation,original',
        includeCount: true
      });
    }

    if (DESK_REJECTED_SUBMISSION_ID) {
      deskRejectedNotesP = Webfield.api.getSubmissions(DESK_REJECTED_SUBMISSION_ID, {
        pageSize: PAGE_SIZE,
        details: 'replyCount,invitation,original',
        includeCount: true
      });
    }
  }

  if (user && !_.startsWith(user.id, 'guest_')) {
    activityNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
      pageSize: PAGE_SIZE,
      details: 'forumContent,invitation,writable'
    });

    userGroupsP = Webfield.getAll('/groups', { regex: CONFERENCE_ID + '/.*', member: user.id, web: true });

    authorNotesP = Webfield.api.getSubmissions(CLAIM_ID, {
      pageSize: PAGE_SIZE,
      'content.authorids': user.profile.id
    });
  }

  var allNotesP = Webfield.getAll('/notes', { invitation: ACCEPTED_PAPER_ID, details: 'replyCount,original' });
  var claimNotesP = Webfield.getAll('/notes', { invitation: CLAIM_HOLD_ID, details: 'replyCount,original,forumContent' });
  var myClaimsP = Webfield.getAll('/notes', { invitation: CLAIM_ID, noDetails: true, tauthor: true });


  return $.when(notesP, userGroupsP, activityNotesP, authorNotesP, withdrawnNotesP, deskRejectedNotesP, allNotesP, claimNotesP, myClaimsP);
}

// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  Webfield.ui.spinner('#notes', { inline: true });
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(ACCEPTED_PAPER_ID, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          if (PUBLIC) {
            promptMessage('Your submission is complete. Check your inbox for a confirmation email. ' +
            'A list of all submissions will be available after the deadline.');
          } else {
            promptMessage('Your submission is complete. Check your inbox for a confirmation email. ' +
            'The author console page for managing your submissions will be available soon.');
          }

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
      heading: 'All Papers',
      id: 'all-submissions',
    },
    {
      heading: 'Claimed',
      id: 'claimed',
    },
    {
      heading: 'Recent Activity',
      id: 'recent-activity',
    }
  ];

  if (PUBLIC) {
    sections.push({
      heading: 'All Submissions',
      id: 'all-submissions',
    });
    if (WITHDRAWN_SUBMISSION_ID) {
      sections.push({
        heading: 'Withdrawn Submissions',
        id: 'withdrawn-submissions',
      })
    }
    if (DESK_REJECTED_SUBMISSION_ID) {
      sections.push({
        heading: 'Desk Rejected Submissions',
        id: 'desk-rejected-submissions',
      })
    }
  }

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function createConsoleLinks(allGroups) {
  var uniqueGroups = _.sortBy(_.uniq(allGroups));
  var links = [];
  uniqueGroups.forEach(function(group) {
    var groupName = group.split('/').pop();
    if (groupName.slice(-1) === 's') {
      groupName = groupName.slice(0, -1);
    }
    links.push(
      [
        '<li class="note invitation-link">',
        '<a href="/group?id=' + group + '">' + groupName.replace(/_/g, ' ') + ' Console</a>',
        '</li>'
      ].join('')
    );
  });

  $('#your-consoles .submissions-list').append(links);

}

function renderContent(notesResponse, userGroups, activityNotes, authorNotes, withdrawnNotes, deskRejectedNotes, allNotesP, claimNotesP, myClaimsP) {

  // Your Consoles tab
  console.log('authorNotes', authorNotes);
  console.log('myClaimsP', myClaimsP);
  console.log('userGroups', userGroups);
  if (userGroups.length || authorNotes.length || myClaimsP.length) {

    var $container = $('#your-consoles').empty();
    $container.append('<ul class="list-unstyled submissions-list">');

    var allConsoles = [];
    if (authorNotes.length) {
      allConsoles.push(AUTHORS_ID);
    }
    userGroups.forEach(function(group) {
      allConsoles.push(group.id);
    });

    if (myClaimsP.length) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AUTHORS_ID + '">Author Console</a>',
        '</li>'
      ].join(''));
    }

    // Render all console links for the user
    createConsoleLinks(allConsoles);

    $('.tabs-container a[href="#your-consoles"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-consoles"]').parent().hide();
  }

  console.log('claimNotesP.length', claimNotesP.length);
  if (allNotesP.length) {
    console.log('allNotesP.length', allNotesP.length);
    var $unclaimedContainer = $('#all-submissions').empty();
    $unclaimedContainer.append('<ul class="list-unstyled submissions-list">');

    var unclaimedResultListOptions = _.assign({}, paperDisplayOptions, {
        container: '#all-submissions',
        autoLoad: false
    });

    Webfield.ui.submissionList(allNotesP, {
        heading: null,
        container: '#all-submissions',
        search: {
          enabled: true,
          localSearch: false,
          invitation: ACCEPTED_PAPER_ID,
          onResults: function(searchResults) {
            Webfield.ui.searchResults(searchResults, unclaimedResultListOptions);
          },
          onReset: function() {
            Webfield.ui.searchResults(allNotesP, unclaimedResultListOptions);
            $('#all-submissions').append(view.paginationLinks(allNotesP.length, PAGE_SIZE, 1));
          }
        },
        displayOptions: paperDisplayOptions,
        autoLoad: false,
        noteCount: allNotesP.length,
        pageSize: PAGE_SIZE,
        onPageClick: function(offset) {
          return Webfield.api.getSubmissions(ACCEPTED_PAPER_ID, {
            details: 'replyCount,original',
            pageSize: PAGE_SIZE,
            offset: offset
          });
        },
        fadeIn: false
    });
    $('.tabs-container a[href="#all-submissions"]').parent().show();

  } else {
    $('.tabs-container a[href="#all-submissions"]').parent().hide();
  }

  if (claimNotesP.length) {
    var $claimedContainer = $('#claimed').empty();
    $claimedContainer.append('<ul class="list-unstyled submissions-list">');

      var claimedResultListOptions = _.assign({}, paperDisplayOptions, {
        container: '#claimed',
        autoLoad: false
      });

      Webfield.ui.submissionList(claimNotesP, {
        heading: null,
        container: '#claimed',
        search: {
          enabled: true,
          localSearch: false,
          invitation: CLAIM_HOLD_ID,
          onResults: function(searchResults) {
            Webfield.ui.searchResults(searchResults, claimedResultListOptions);
          },
          onReset: function() {
            Webfield.ui.searchResults(claimNotesP, claimedResultListOptions);
            $('#claimed').append(view.paginationLinks(claimNotesP.length, PAGE_SIZE, 1));
          }
        },
        displayOptions: paperDisplayOptions,
        autoLoad: false,
        noteCount: claimNotesP.length,
        pageSize: PAGE_SIZE,
        onPageClick: function(offset) {
          return Webfield.api.getSubmissions(CLAIM_HOLD_ID, {
            details: 'replyCount,original,forumContent',
            pageSize: PAGE_SIZE,
            offset: offset
          });
        },
        fadeIn: false
      });

    $('.tabs-container a[href="#claimed"]').parent().show();

  }  else {
    $('.tabs-container a[href="#claimed"]').parent().hide();
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

  var withdrawnNotesCount = withdrawnNotes.count || 0;
  if (withdrawnNotesCount) {
    $('#withdrawn-submissions').empty();

    var withdrawnNotesArray = withdrawnNotes.notes || [];
    Webfield.ui.submissionList(withdrawnNotesArray, {
      heading: null,
      container: '#withdrawn-submissions',
      search: {
        enabled: false
      },
      displayOptions: paperDisplayOptions,
      autoLoad: false,
      noteCount: withdrawnNotesCount,
      pageSize: PAGE_SIZE,
      onPageClick: function(offset) {
        return Webfield.api.getSubmissions(WITHDRAWN_SUBMISSION_ID, {
          details: 'replyCount,invitation,original',
          pageSize: PAGE_SIZE,
          offset: offset
        });
      },
      fadeIn: false
    });
  } else {
    $('.tabs-container a[href="#withdrawn-submissions"]').parent().hide();
  }

  var deskRejectedNotesCount = deskRejectedNotes.count || 0;
  if (deskRejectedNotesCount) {
    $('#desk-rejected-submissions').empty();

    var deskRejectedNotesArray = deskRejectedNotes.notes || [];
    Webfield.ui.submissionList(deskRejectedNotesArray, {
      heading: null,
      container: '#desk-rejected-submissions',
      search: {
        enabled: false
      },
      displayOptions: paperDisplayOptions,
      autoLoad: false,
      noteCount: deskRejectedNotesCount,
      pageSize: PAGE_SIZE,
      onPageClick: function(offset) {
        return Webfield.api.getSubmissions(DESK_REJECTED_SUBMISSION_ID, {
          details: 'replyCount,invitation,original',
          pageSize: PAGE_SIZE,
          offset: offset
        });
      },
      fadeIn: false
    });
  } else {
    $('.tabs-container a[href="#desk-rejected-submissions"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();
}

// Go!
main();
