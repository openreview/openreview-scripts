// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

var HEADER = {
  title: 'NAMPI: Neural Abstract Machines & Program Induction',
  subtitle: 'A Federated Artificial Intelligence Meeting (FAIM) workshop (ICML, IJCAI/ECAI, AAMAS)',
  location: 'Stockholm, Sweden',
  date: '2018',
  website: 'https://uclmr.github.io/nampi/',
  instructions: '<p><strong>Important Information about Anonymity:</strong><br>\
    When you post a submission to NAMPI 2018, please provide the real names and email addresses of authors in the submission form below.\
    An anonymous record of your paper will appear in the "All Papers Under Review" and "My Papers Under Review" tabs. \
    All discussion will take place on the anonymous versions of your paper(s).\
    The <em>original</em> record of your submission will be private, and will contain your real name(s); \
    originals can be found in the "My Submitted Papers" tab.\
    Please do not include the author names in the PDF for your submission. </p>\
    <p><strong>Editing or Revising your submission:</strong><br>\
    Anonymous versions of papers are not directly editable. To make a change to your paper, go to the \
    original, non-anonymous version and edit it (if editing is enabled). Changes will propagate to the \
    anonymous version. Edit and revision policy is determined by the specific policy of this conference. \
    <p><strong>Questions or Concerns:</strong><br> \
    Please contact the OpenReview support team at \
    <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform. \</br> \
    Please contact the NAMPI 2018 Program Chairs at \
    <a href="mailto:nampi@googlegroups.com">nampi@googlegroups.com</a> with any questions or concerns about conference administration or policy. \</p>',
  deadline: 'June 1, 2018'
}

// Constants
var CONFERENCE_ID = 'ICML.cc/2018/Workshop/NAMPI';
var SUBMISSION_ID = CONFERENCE_ID + '/-/Submission';
var BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var RECRUIT_REVIEWERS = CONFERENCE_ID + '/-/Recruit_Reviewers';
var WILDCARD_INVITATION = CONFERENCE_ID + '/-/.*';

var ANON_SIGNATORY_REGEX = /^ICML\.cc\/2018\/Workshop\/NAMPI\/Paper(\d+)\/(AnonReviewer\d+|Area_Chair\d+)/;
var AUTHORS_SIGNATORY_REGEX = /^ICML\.cc\/2018\/Workshop\/NAMPI\/Paper(\d+)\/Authors/;

var AREA_CHAIRS_ID = CONFERENCE_ID + '/Area_Chairs';
var PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs';


var COMMENT_EXCLUSION = [
  SUBMISSION_ID,
  RECRUIT_REVIEWERS
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

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required

  renderConferenceHeader();

  renderSubmissionButton();

  renderConferenceTabs();

  load().then(renderContent);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_SUBMISSION_ID, {
    pageSize: PAGE_SIZE
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
      invitation: BLIND_INVITATION
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
      authorNotesP, tagInvitationsP
    );
  });

}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  Webfield.ui.spinner('#notes');
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(SUBMISSION_ID, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission is complete. The list of all current submissions is shown below.');

          load().then(renderContent).then(function() {
            $('.tabs-container a[href="#all-papers-under-review"]').click();
          });
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'All Papers Under Review',
      id: 'all-papers-under-review',
    },
    {
      heading: 'My Papers Under Review',
      id: 'my-papers-under-review',
    },
    {
      heading: 'My Submitted Papers',
      id: 'my-submitted-papers',
    },
    {
      heading: 'My Tasks',
      id: 'my-tasks',
    },
    {
      heading: 'My Assigned Papers',
      id: 'my-assigned-papers',
    },
    {
      heading: 'My Comments & Reviews',
      id: 'my-comments-reviews',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, submittedNotes, assignedNotePairs, assignedNotes, userGroups, authorNotes, tagInvitations) {
  var data, commentNotes;

  // if (_.isEmpty(userGroups)) {
  //   // If the user isn't part of the conference don't render tabs
  //   $('.tabs-container').hide();
  //   return;
  // }

  commentNotes = [];

  _.forEach(submittedNotes, function(note) {
    if (!_.isNil(note.ddate)) {
      return;
    }
    if (!_.includes([SUBMISSION_ID, RECRUIT_REVIEWERS], note.invitation)) {
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

  // My Tasks tab
  if (userGroups.length) {
    var tasksOptions = {
      container: '#my-tasks',
      emptyMessage: 'No outstanding tasks for this conference'
    }
    Webfield.ui.taskList(assignedNotePairs, tagInvitations, tasksOptions)

    if (_.includes(userGroups, AREA_CHAIRS_ID)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AREA_CHAIRS_ID + '">Area Chair Console</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, PROGRAM_CHAIRS_ID)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/assignments?venue=' + CONFERENCE_ID,
            'Assignments Browser',
          '</a>',
        '</li>'
      ].join(''));

      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + PROGRAM_CHAIRS_ID + '">Program Chair Console</a>',
        '</li>'
      ].join(''));
    }

    $('.tabs-container a[href="#my-tasks"]').parent().show();
  } else {
    $('.tabs-container a[href="#my-tasks"]').parent().hide();
  }

  // All Submitted Papers tab
  var submissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: true,
    tagInvitations: tagInvitations,
    container: '#all-papers-under-review'
  });

  Webfield.ui.submissionList(notes, {
    heading: null,
    container: '#all-papers-under-review',
    search: {
      enabled: true,
      onResults: function(searchResults) {
        var blindedSearchResults = searchResults.filter(function(note) {
          return note.invitation === BLIND_SUBMISSION_ID;
        });
        Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
        Webfield.disableAutoLoading();
      },
      onReset: function() {
        Webfield.ui.searchResults(notes, submissionListOptions);
        if (notes.length === PAGE_SIZE) {
          Webfield.setupAutoLoading(BLIND_SUBMISSION_ID, PAGE_SIZE, submissionListOptions);
        }
      }
    },
    displayOptions: submissionListOptions,
    fadeIn: false
  });

  if (notes.length === PAGE_SIZE) {
    Webfield.setupAutoLoading(BLIND_SUBMISSION_ID, PAGE_SIZE, submissionListOptions);
  }


  // My Submitted Papers tab
  if (authorNotes.length) {
    Webfield.ui.searchResults(
      authorNotes,
      _.assign({}, paperDisplayOptions, {container: '#my-submitted-papers'})
    );
    console.log('authorNotes', authorNotes);
    var authorNoteIds = _.map(authorNotes, function(original){
      return original.id;
    });

    console.log('authorNoteIds', authorNoteIds);
    // get blind papers that are authored by this user
    var myPapersUnderReview = _.filter(notes, function(note){
      return _.includes(authorNoteIds, note.original);
    });

    console.log('myPapersUnderReview',myPapersUnderReview);

    // My Papers Under Review tab
    Webfield.ui.searchResults(
      myPapersUnderReview,
      _.assign({}, paperDisplayOptions, {
        container: '#my-papers-under-review',
        emptyMessage: 'You have no papers currently under review.'
      })
    );
    $('.tabs-container a[href="#my-submitted-papers"]').parent().show();
    $('.tabs-container a[href="#my-papers-under-review"]').parent().show();
  } else {
    $('.tabs-container a[href="#my-submitted-papers"]').parent().hide();
    $('.tabs-container a[href="#my-papers-under-review"]').parent().hide();
  }



  // My Assigned Papers tab (only show if not empty)
  if (assignedNotes.length) {
    Webfield.ui.searchResults(
      assignedNotes,
      _.assign({}, paperDisplayOptions, {container: '#my-assigned-papers'})
    );
    $('.tabs-container a[href="#my-comments-reviews"]').parent().show();
  } else {
    $('.tabs-container a[href="#my-assigned-papers"]').parent().hide();
  }

  // My Comments & Reviews tab (only show if not empty)
  if (commentNotes.length) {
    Webfield.ui.searchResults(
      commentNotes,
      _.assign({}, commentDisplayOptions, {
        container: '#my-comments-reviews',
        emptyMessage: 'No comments or reviews to display'
      })
    );
    $('.tabs-container a[href="#my-comments-reviews"]').parent().show();
  } else {
    $('.tabs-container a[href="#my-comments-reviews"]').parent().hide();
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





