var CONFERENCE_ID = 'auai.org/UAI/2019/Conference';
var SUBMISSION_ID = CONFERENCE_ID + '/-/Submission';
var BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var REVIEWERS_NAME = 'Reviewers';
var AREA_CHAIRS_NAME = 'Program_Committee';
var AREA_CHAIRS_ID = CONFERENCE_ID + '/Program_Committee';
var REVIEWERS_ID = CONFERENCE_ID + '/Reviewers';
var PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs';
var AUTHORS_ID = CONFERENCE_ID + '/Authors';

var instructions = '<p><strong>Important Information about Anonymity:</strong><br>\
 When you post a submission to UAI 2018, please provide the real names and email addresses of authors in the submission form below (but NOT in the manuscript). The <em>original</em> record of your submission will be private, and will contain your real name(s). \
 Originals can be found in the "My Submitted Papers" tab below. You can also access the original record of your paper by clicking the "Modifiable Original" link in the discussion forum page of your paper. Discussion forum pages for the anonymous versions of your paper can be found in the "My Papers Under Review" tab. The PDF in your submission should not contain the names of the authors. </p>  \
 <p><strong>Conflict of Interest:</strong><br> Please make sure that your current and previous affiliations listed on your OpenReview <a href="/profile">profile page</a> is up-to-date to avoid conflict of interest.</p>  \
 <p><strong>Bidding on Papers (for reviewers)</strong><br> If you are serving as a member of the Program Committee (as a reviewer), you can bid on papers in the list below. You can also use the  <a href="invitation?id=auai.org/UAI/2018/-/Bid">Bidding Console</a> for better navigational features. These features will be made available once the bidding period starts. </p>  \
 <p><strong>Questions or Concerns:</strong><br> Please contact the OpenReview support team at <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns. </p>'

var HEADER = {
  'title': "UAI 2019",
  'subtitle': "Conference on Uncertainty in Artificial Intelligence",
  'deadline': 'Submission Deadline: 11:59 pm Samoa Standard Time, March 4, 2019',
  'date': 'June 22 - June 26, 2019',
  'website': 'http://auai.org/uai2019/',
  'location': 'Tel Aviv, Israel',
  "instructions": instructions,
};

var instructions = '<strong>Authors: Please see the <a href="http://learningtheory.org/colt2019/call.html">call for papers</a> for detailed submission instructions.</strong><br>\
When you have successfully submitted a paper, a link to your "Author Console" should appear below, in the "Your Consoles" tab.<br>\
Please contact <a href="mailto:info@openreview.net">info@openreview.net</a> for any questions about the platform. For policy-specific questions, please contact the COLT program chairs at <a href="colt2019pc@gmail.com">colt2019pc@gmail.com</a>.\
<br><br>\
<strong>Important Notes about Submitting a Paper:</strong>\
<ul>\
  <li>Unlike at some of the other conferences that have used OpenReview, neither submissions nor the reviewing process will be public.</li>\
  <li>When submitting your paper, you can safely ignore the "readers" field in the submission form (it will be set automatically).</li>\
  <li>In the "signatures" field, most users will have just one valid identity, which will be set automatically. If you have more than one valid identity, you may select the one that you wish to use. Your identity will be revealed only to the Program Committee and Program Chairs. Please contact OpenReview support if you have any questions.</li>\
</ul>\
<strong>Frequently Asked Questions:</strong>\
<ul>\
  <strong>Q: </strong><em>My paper has "COLT 2019 Conference" in its list of readers -- what does that mean?</em>\
  <br>\
  <strong>A: </strong>This is related to the way that OpenReview\'s permission system works. It means that the <em>conference entity itself</em> has permission to see your paper, which it needs in order to perform automated checks and analyses during the course of the reviewing process.\
  <br>\
  <strong>Q: </strong><em>Something I read on OpenReview is different from what I see on the COLT Call for Papers -- what should I do?</em>\
  <br>\
  <strong>A: </strong>The official COLT website should be considered correct at all times. If you notice a discrepancy, please contact OpenReview support.\
  <br>\
</ul>\
<br>'

var SUBJECT_AREAS_LIST = [];
var BUFFER = 1000 * 60 * 1;  // 30 minutes
var PAGE_SIZE = 400;
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

// var CONFERENCE_REGEX = CONFERENCE.replace('.', '\\.').replace('/','\\/')
// var WILDCARD_INVITATION = CONFERENCE + '/-/.*';


// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE_ID);  // required
  renderConferenceHeader();
  // renderSubmissionButton();
  // renderConferenceTabs();
  // load()
  // .then(renderContent)
  // .then(Webfield.ui.done);
  // Webfield.ui.done
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {
    pageSize: PAGE_SIZE,
    details: 'all'
  });

  var submittedNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: PAGE_SIZE,
    tauthor: true,
    details: 'all'
  });

  var assignedNotePairsP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {
    pageSize: 100,
    invitee: true,
    duedate: true,
    details: 'all'
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
        function(id) { return _.startsWith(id, CONFERENCE); }
      );
    });

    authorNotesP = Webfield.get('/notes', {
      'content.authorids': user.profile.id,
      invitation: BLIND_INVITATION
    }).then(function(result) {
      return result.notes;
    });
  }

  var tagInvitationsP = Webfield.api.getTagInvitations(BLIND_INVITATION);

  return userGroupsP
  .then(function(userGroups) {

    var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
    var assignedNotesP = $.Deferred().resolve([]);

    if (assignedPaperNumbers.length) {
        assignedNotesP = Webfield.api.getSubmissions(BLIND_INVITATION, {
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

  // Webfield.ui.spinner('#notes', { inline: true });
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(SUBMISSION_INVITATION, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission to ' + TITLE + ' is complete.');

          load().then(renderContent).then(function() {
            $('.tabs-container a[href="#my-submitted-papers"]').click();
          });
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'My Tasks',
      id: 'my-tasks',
    },
    {
      heading: 'My Submitted Papers',
      id: 'my-submitted-papers',
    },
    {
      heading: 'My Papers Under Review',
      id: 'my-papers-under-review',
    },
    {
      heading: 'My Assigned Papers',
      id: 'my-assigned-papers',
    },
    {
      heading: 'My Comments & Reviews',
      id: 'my-comments-reviews',
    },
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, submittedNotes, assignedNotePairs, assignedNotes, userGroups, authorNotes, tagInvitations) {
  console.log('userGroups', userGroups);

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
    if (!_.includes([SUBMISSION_INVITATION, RECRUIT_REVIEWERS], note.invitation)) {
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

  var authorNoteIds = _.map(authorNotes, function(n){
    return n.id;
  });
  console.log('authorNoteIds', authorNoteIds);

  var blindNotes = _.filter(notes, function(n){
    return authorNoteIds.includes(n.original)
  });

  console.log('blindNotes', blindNotes);

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

  var submissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: true,
    tagInvitations: tagInvitations,
    container: '#my-submitted-papers'
  });

  // MLS: Removing this because there won't be any users that submit more than a couple papers.
  // if (notes.length === PAGE_SIZE) {
  //   Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
  // }

  // My Tasks tab
  if (userGroups.length) {
    var tasksOptions = {
      container: '#my-tasks',
      emptyMessage: 'No outstanding tasks for ' + TITLE
    }
    Webfield.ui.taskList(assignedNotePairs, tagInvitations, tasksOptions)

    // Custom links for UAI
    var acId = CONFERENCE + '/Senior_Program_Committee';
    if (_.includes(userGroups, acId)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + acId + '">UAI 2019 Senior Program Committee Member Console</a>',
        '</li>'
      ].join(''));
    }

     // Custom links for UAI
    var pcId = 'auai.org/UAI/2019/Program_Chairs';
    if (_.includes(userGroups, pcId)) {
      $('#my-tasks .submissions-list').prepend([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + pcId + '">UAI 2019 Program Chairs Console</a>',
        '</li>'
      ].join(''));
    }

  } else {
    $('.tabs-container a[href="#my-tasks"]').parent().hide();
  }

  // All Submitted Papers tab
  // Webfield.ui.submissionList(notes, {
  //   heading: null,
  //   container: '#my-papers-under-review',
  //   search: {
  //     enabled: false,
  //     subjectAreas: SUBJECT_AREAS_LIST,
  //     onResults: function(searchResults) {
  //       var blindedSearchResults = searchResults.filter(function(note) {
  //         return note.invitation === BLIND_INVITATION;
  //       });
  //       Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
  //       Webfield.disableAutoLoading();
  //     },
  //     onReset: function() {
  //       Webfield.ui.searchResults(notes, submissionListOptions);
  //       if (notes.length === PAGE_SIZE) {
  //         Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
  //       }
  //     }
  //   },
  //   displayOptions: submissionListOptions,
  //   fadeIn: false
  // });

  // My Papers Under Review tab
  Webfield.ui.searchResults(
    blindNotes,
    _.assign({}, paperDisplayOptions, {
      container: '#my-papers-under-review',
      emptyMessage: 'You have no papers currently under review.'
    })
  );

  // My Submitted Papers tab

  Webfield.ui.searchResults(
    authorNotes,
    _.assign({}, paperDisplayOptions, {
      container: '#my-submitted-papers',
      emptyMessage: 'You have not submitted any papers.'
    })
  );


  // My Assigned Papers tab (only show if not empty)
  if (assignedNotes.length) {
    Webfield.ui.searchResults(
      assignedNotes,
      _.assign({}, paperDisplayOptions, {container: '#my-assigned-papers'})
    );
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
  } else {
    $('.tabs-container a[href="#my-comments-reviews"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();
}

// Helper functions
function getPaperNumbersfromGroups(groups) {
  var re = new RegExp('^' + CONFERENCE_REGEX + '\/Paper([0-9]+)\/(AnonReviewer[0-9]+|Area_Chair)');
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

function getAuthorPaperNumbersfromGroups(groups) {
  var re = new RegExp('^' + CONFERENCE_REGEX + '\/Paper(\d+)\/Authors');
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
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
  return ;
}

// Go!
main();
