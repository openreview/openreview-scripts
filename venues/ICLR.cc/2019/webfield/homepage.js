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
var AUTHORS_ID = CONFERENCE_ID + '/Authors';

var SUBJECT_AREAS = [
  'Algorithms: Approximate Inference',
  'Algorithms: Belief Propagation',
  'Algorithms: Distributed and Parallel',
  'Algorithms: Exact Inference',
  'Algorithms: Graph Theory',
  'Algorithms: Heuristics',
  'Algorithms: Lifted Inference',
  'Algorithms: MCMC methods',
  'Algorithms: Optimization',
  'Algorithms: Other',
  'Algorithms: Software and Tools',
  'Applications: Biology',
  'Applications: Databases',
  'Applications: Decision Support',
  'Applications: Diagnosis and Reliability',
  'Applications: Economics',
  'Applications: Education',
  'Applications: General',
  'Applications: Medicine',
  'Applications: Planning and Control',
  'Applications: Privacy and Security',
  'Applications: Robotics',
  'Applications: Sensor Data',
  'Applications: Social Network Analysis',
  'Applications: Speech',
  'Applications: Sustainability and Climate',
  'Applications: Text and Web Data',
  'Applications: User Models',
  'Applications: Vision',
  'Data: Big Data',
  'Data: Multivariate',
  'Data: Other',
  'Data: Relational',
  'Data: Spatial',
  'Data: Temporal or Sequential',
  'Learning: Active Learning',
  'Learning: Classification',
  'Learning: Clustering',
  'Learning: Deep Learning',
  'Learning: General',
  'Learning: Nonparametric Bayes',
  'Learning: Online and Anytime Learning',
  'Learning: Other',
  'Learning: Parameter Estimation',
  'Learning: Probabilistic Generative Models',
  'Learning: Ranking',
  'Learning: Recommender Systems',
  'Learning: Regression',
  'Learning: Reinforcement Learning',
  'Learning: Relational Learning',
  'Learning: Relational Models',
  'Learning: Scalability',
  'Learning: Semi-Supervised Learning',
  'Learning: Structure Learning',
  'Learning: Structured Prediction',
  'Learning: Theory',
  'Learning: Unsupervised',
  'Methodology: Bayesian Methods',
  'Methodology: Calibration',
  'Methodology: Elicitation',
  'Methodology: Evaluation',
  'Methodology: Human Expertise and Judgement',
  'Methodology: Other',
  'Methodology: Probabilistic Programming',
  'Models: Bayesian Networks',
  'Models: Directed Graphical Models',
  'Models: Dynamic Bayesian Networks',
  'Models: Markov Decision Processes',
  'Models: Mixed Graphical Models',
  'Models: Other',
  'Models: Relational Models',
  'Models: Topic Models',
  'Models: Undirected Graphical Models',
  'None of the above',
  'Principles: Causality',
  'Principles: Cognitive Models',
  'Principles: Decision Theory',
  'Principles: Game Theory',
  'Principles: Information Theory',
  'Principles: Other',
  'Principles: Probability Theory',
  'Principles: Statistical Theory',
  'Representation: Constraints',
  'Representation: Dempster-Shafer',
  'Representation: Fuzzy Logic',
  'Representation: Influence Diagrams',
  'Representation: Non-Probabilistic Frameworks',
  'Representation: Probabilistic'
];

var HEADER = {
  title: 'ICLR 2019',
  subtitle: 'International Conference on Machine Learning',
  location: 'Vancouver Convention Center, Vancouver, BC, Canada',
  date: 'April 30 - May 3, 2019',
  website: 'http://www.ICLR.cc',
  instructions: '<p><strong>Important Information about Anonymity</strong><br>\
    OpenReview maintains both anonymity and attributability of papers by storing an "original" \
    record of the paper, complete with full author names and email addresses, as well as an anonymizing \
    "mask" for the paper, which protects the authors\' identities. Specific policy regarding when \
    (and to whom) original records are revealed is determined by the conference organizers, but typically, \
    original records are visible only to the authors themselves and to the conference program chairs. \
    Contact the conference organizers with questions about conference-specific policy. (WARNING: PDFs \
    are not automatically masked. Authors should submit PDFs without author identities.)</p> \
    <p><strong>"Papers Under Review" vs. "Submitted Papers"</strong><br>\
    Original papers, complete with full author names and email addresses, are submitted to a conference,\
    and can be seen by the authors in the "My Submitted Papers" tab. Upon submission, a mask is created \
    and made available to reviewers and other discussion participants (these participants are determined by \
    conference-specific policy). Masks on your submitted papers appear in the "My Papers Under Review" tab. \
    Masks created for other submissions appear in the "All Papers Under Review" tab.</p> \
    <p><strong>Posting Revisions to Submissions</strong><br>\
    To post a revision to your paper, navigate to the original version, and click on the "Add Revision" button if available. \
    Revisions are not allowed during the formal review process.\
    Revisions on originals propagate all changes to anonymous copies, while maintaining anonymity.</p> \
    <p><strong>A Note to Reviewers about Bidding</strong><br> \
    To access the bidding interface, please ensure that your profile is linked to the email address where you received your initial reviewer invitation email. \
    To do this, click on your name at the top right corner of the page, go to your Profile, enter "edit mode," and add your email address. \
    You will also need to confirm your address by pressing the "Confirm" button. This will involve a round-trip email verification.</p>\
    <p><strong>Questions or Concerns</strong><br> \
    Please contact the OpenReview support team at \
    <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform. \</br> \
    Please contact the ICLR 2019 Program Chairs at \
    <a href="mailto:ICLR2019programchairs@gmail.com">ICLR2019programchairs@gmail.com</a> with any questions or concerns about conference administration or policy. \</p>',
  deadline: 'Submission Deadline: 5:00pm Eastern Standard Time, October 27, 2017'
}

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
            $('.tabs-container a[href="#all-submissions"]').click();
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
      heading: 'All Submissions',
      id: 'all-submissions',
    },
    // {
    //   heading: 'Your ICLR Tasks',
    //   id: 'your-iclr-tasks',
    // },
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

function renderContent(notes, submittedNotes, assignedNotePairs, assignedNotes, userGroups, authorNotes, tagInvitations, activityNotes) {
  var data, commentNotes;

  console.log('userGroups',userGroups);

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
  console.log('authorPaperNumbers',authorPaperNumbers);
  if (authorPaperNumbers.length !== authorNotes.length) {
    console.warn('WARNING: The number of submitted notes returned by API does not ' +
      'match the number of submitted note groups the user is a member of.');
  }

  console.log('userGroups', userGroups);

  // My Tasks tab
  // if (userGroups.length) {
  //   var tasksOptions = {
  //     container: '#your-iclr-tasks',
  //     emptyMessage: 'No outstanding tasks for this conference'
  //   }
  //   Webfield.ui.taskList(assignedNotePairs, tagInvitations, tasksOptions)

  //   if (_.includes(userGroups, AREA_CHAIRS_ID)) {
  //     $('#your-iclr-tasks .submissions-list').prepend([
  //       '<li class="note invitation-link">',
  //         '<a href="/group?id=' + AREA_CHAIRS_ID + '">Area Chair Console</a>',
  //       '</li>'
  //     ].join(''));
  //   }

  //   if (_.includes(userGroups, PROGRAM_CHAIRS_ID)) {
  //     $('#your-iclr-tasks .submissions-list').prepend([
  //       '<li class="note invitation-link">',
  //         '<a href="/assignments?venue=' + CONFERENCE_ID,
  //           'Assignments Browser',
  //         '</a>',
  //       '</li>'
  //     ].join(''));

  //     $('#your-iclr-tasks .submissions-list').prepend([
  //       '<li class="note invitation-link">',
  //         '<a href="/group?id=' + PROGRAM_CHAIRS_ID + '">Program Chair Console</a>',
  //       '</li>'
  //     ].join(''));
  //   }
  //   $('.tabs-container a[href="#your-iclr-tasks"]').parent().show();
  // } else {
  //   $('.tabs-container a[href="#your-iclr-tasks"]').parent().hide();
  // }

  // Your Consoles tab
  if (userGroups.length) {
    // var tasksOptions = {
    //   container: '#your-consoles',
    //   emptyMessage: 'This shouldn\'t be here',
    //   showTasks: false
    // }
    // Webfield.ui.taskList(assignedNotePairs, tagInvitations, tasksOptions)

    var $container = $('#your-consoles');
    $container.append('<ul class="list-unstyled submissions-list">');

    if (_.includes(userGroups, PROGRAM_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + PROGRAM_CHAIRS_ID + '" target="_blank">Program Chair Console</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, REVIEWERS_ID) || _.includes(userGroups, AREA_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/invitation?id=' + ADD_BID_ID + '" target="_blank">Bidding Console</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, AREA_CHAIRS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AREA_CHAIRS_ID + '" target="_blank">Area Chair Console</a>',
        '</li>'
      ].join(''));
    }

    if (_.includes(userGroups, REVIEWERS_ID)) {
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + REVIEWERS_ID + '" target="_blank" >Reviewer Console</a>',
        '</li>'
      ].join(''));
    }

    if (authorPaperNumbers.length) {
      console.log('attaching authors link');
      $('#your-consoles .submissions-list').append([
        '<li class="note invitation-link">',
          '<a href="/group?id=' + AUTHORS_ID + '" target="_blank">Author Console</a>',
        '</li>'
      ].join(''));
    }

    $('.tabs-container a[href="#your-consoles"]').parent().show();
  } else {
    $('.tabs-container a[href="#your-consoles"]').parent().hide();
  }

  // All Submitted Papers tab
  var submissionListOptions = _.assign({}, paperDisplayOptions, {
    showTags: false,
    tagInvitations: tagInvitations,
    container: '#all-submissions'
  });

  Webfield.ui.submissionList(notes, {
    heading: null,
    container: '#all-submissions',
    search: {
      enabled: true,
      subjectAreas: SUBJECT_AREAS,
      localSearch: false,
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
      console.log('note.original', note.original);
      return _.includes(authorNoteIds, note.original);
    });
    //var myPapersUnderReview = notes;
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

  // Activity Tab

  if (activityNotes.length) {
    // Webfield.ui.searchResults(
    //   activityNotes,
    //   _.assign({}, commentDisplayOptions, {
    //     container: '#recent-activity',
    //     emptyMessage: 'No comments or reviews to display',
    //     showActivity: true,
    //     forumContent: true,
    //     pdfLink: true,
    //     replyCount: false
    //   })
    // );

    var displayOptions = {
      container: '#recent-activity'
    };

    Webfield.ui.activityList(activityNotes, displayOptions);

    $('.tabs-container a[href="#recent-activity"]').parent().show();
  } else {
    $('.tabs-container a[href="#recent-activity"]').parent().hide();
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
