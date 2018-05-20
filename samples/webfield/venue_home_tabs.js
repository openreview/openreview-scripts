// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE = 'auai.org/UAI/2017';
var INVITATION = CONFERENCE + '/-/submission';
var BLIND_INVITATION = CONFERENCE + '/-/blind-submission';
var WILDCARD_INVITATION = CONFERENCE + '/-/.*';
var AC_GROUPS = [
  CONFERENCE + '/Program_Committee',
  CONFERENCE + '/Senior_Program_Committee',
  CONFERENCE + '/Program_Co-Chairs'
];
var SUBJECT_AREAS_LIST = [
  'All',
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
  "Applications: Diagnosis and Reliability",
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

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();

  renderSubmissionButton();

  renderConferenceTabs();

  load().then(renderContent);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {pageSize: PAGE_SIZE});
  var submittedNotesP = Webfield.api.getSubmissions(WILDCARD_INVITATION, {pageSize: PAGE_SIZE, tauthor: true});
  var userGroupsP;
  if (!user || _.startsWith(user.id, 'guest_')) {
    userGroupsP = Promise.resolve([]);
  } else {
    userGroupsP = Webfield.get('/groups', {member: user.id}).then(function(result) {
      return _.filter(
        _.map(result.groups, function(g) { return g.id; }),
        function(id) { return _.startsWith(id, CONFERENCE); }
      );
    });
  }

  return $.when(notesP, submittedNotesP, userGroupsP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'UAI 2017 Conference',
    subtitle: 'International Conference on Uncertainty in Artificial Intelligence',
    location: 'Sydney, Australia',
    date: 'August 11 - 15, 2017',
    website: 'http://auai.org/uai2017/',
    instructions: null,
    deadline: 'Submission Deadline: March 31st, 2017, 11:59 pm SST (Samoa Standard Time)'
  });

  Webfield.ui.spinner('#notes');
}

function renderSubmissionButton() {
  Webfield.api.getSubmissionInvitation(INVITATION, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          load().then(renderContent);
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'All Submitted Papers',
      id: 'all-submitted-papers',
    },
    {
      heading: 'My Submitted Papers',
      id: 'my-submitted-papers',
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
    overwrite: true
  });
}

function renderContent(notes, submittedNotes, userGroups) {
  var data, commentNotes;

  if (_.isEmpty(userGroups)) {
    // If the user isn't part of the conference don't render tabs
    $('.tabs-container').hide();
    return;
  }

  commentNotes = [];
  _.forEach(submittedNotes, function(note) {
    if (_.startsWith(note.invitation, CONFERENCE) && note.invitation !== INVITATION && _.isNil(note.ddate)) {
      // TODO: remove this client side filtering when DB query is fixed
      commentNotes.push(note);
    }
  });

  var assignedPaperNumbers = getPaperNumbersfromGroups(userGroups);
  assignedNotes = _.filter(notes, function(n) { return _.includes(assignedPaperNumbers, n.number); });

  var authorPaperNumbers = getAuthorPaperNumbersfromGroups(userGroups);
  submittedNotes = _.filter(notes, function(n) { return _.includes(authorPaperNumbers, n.number); });

  // All Submitted Papers tab (only show for admins)
  if (_.intersection(userGroups, AC_GROUPS).length) {
    var submissionListOptions = _.assign(
      {}, paperDisplayOptions, {container: '#all-submitted-papers'}
    );
    Webfield.ui.submissionList(notes, {
      heading: null,
      container: '#all-submitted-papers',
      search: {
        enabled: true,
        subjectAreas: SUBJECT_AREAS_LIST,
        onResults: function(searchResults) {
          Webfield.ui.searchResults(searchResults, submissionListOptions);
          Webfield.disableAutoLoading();
        },
        onReset: function() {
          Webfield.ui.searchResults(notes, submissionListOptions);
          if (notes.length === PAGE_SIZE) {
            Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
          }
        }
      },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    if (notes.length === PAGE_SIZE) {
      Webfield.setupAutoLoading(BLIND_INVITATION, PAGE_SIZE, submissionListOptions);
    }
    $('.tabs-container a[href="#all-submitted-papers"]').parent().show();
  } else {
    $('.tabs-container a[href="#all-submitted-papers"]').parent().hide();
  }

  // My Submitted Papers tab
  Webfield.ui.searchResults(submittedNotes, _.assign(
    {}, paperDisplayOptions, {container: '#my-submitted-papers'}
  ));

  // My Assigned Papers tab (only show if not empty)
  if (assignedNotes.length) {
    Webfield.ui.searchResults(assignedNotes, _.assign(
      {}, paperDisplayOptions, {container: '#my-assigned-papers'}
    ));
    $('.tabs-container a[href="#my-assigned-papers"]').parent().show();
  } else {
    $('.tabs-container a[href="#my-assigned-papers"]').parent().hide();
  }

  // My Comments & Reviews tab (only show if not empty)
  if (commentNotes.length) {
    Webfield.ui.searchResults(commentNotes, _.assign(
      {}, commentDisplayOptions, {container: '#my-comments-reviews', emptyMessage: 'No comments or reviews to display'}
    ));
    $('.tabs-container a[href="#my-comments-reviews"]').parent().show();
  } else {
    $('.tabs-container a[href="#my-comments-reviews"]').parent().hide();
  }

  // Show first available tab
  $('.tabs-container ul.nav-tabs li a').eq(0).click();
}


// Helper functions
function getPaperNumbersfromGroups(groups) {
  // Should be customized for the conference
  var re = /^auai\.org\/UAI\/2017\/Paper(\d+)\/(AnonReviewer\d+|Area_Chair)/;
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

function getAuthorPaperNumbersfromGroups(groups) {
  // Should be customized for the conference
  var re = /^auai\.org\/UAI\/2017\/Paper(\d+)\/Authors/;
  return _.map(
    _.filter(groups, function(gid) { return re.test(gid); }),
    function(fgid) { return parseInt(fgid.match(re)[1], 10); }
  );
}

// Go!
main();
