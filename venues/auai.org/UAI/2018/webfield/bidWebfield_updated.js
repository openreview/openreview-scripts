// ------------------------------------
// Add Bid Interface
// ------------------------------------

var CONFERENCE = 'auai.org/UAI/2018';
var AREA_CHAIRS = 'auai.org/UAI/2018/Senior_Program_Committee';
var SUBTITLE = 'Conference on Uncertainty in Artificial Intelligence';
var TITLE = 'UAI 2018';
var RECRUIT_REVIEWERS = 'auai.org/UAI/2018/-/PC_Invitation';
var PROGRAM_CHAIRS = 'auai.org/UAI/2018/Program_Chairs';
var DEADLINE = 'Submission Deadline: March 9th, 2018, 11:59 pm SST (Samoa Standard Time)';
var DATE = 'August 6 - 10, 2018';
var BLIND_INVITATION = 'auai.org/UAI/2018/-/Blind_Submission';
var METADATA_INVITATION = 'auai.org/UAI/2018/-/Paper_Metadata';
//<INSTRUCTIONS>
var WEBSITE = 'http://auai.org/uai2018/index.php';
var REVIEWERS = 'auai.org/UAI/2018/Program_Committee';
var LOCATION = 'Monterey, California, USA';
var SUBMISSION_INVITATION = 'auai.org/UAI/2018/-/Submission';
//<CONFERENCE_REGEX>
//<WILDCARD_INVITATION>
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

var ADD_BID = CONFERENCE + '/-/Add_Bid';
var PAGE_SIZE = 1000;

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#invitation-container', CONFERENCE);  // required

  Webfield.ui.header(TITLE + ' Paper Bidding');

  Webfield.ui.spinner('#notes');

  OpenBanner.breadcrumbs([
    { link: '/', text: 'Venues' },
    { link: '/group?id=' + CONFERENCE, text: view.prettyId(CONFERENCE) }
  ]);

  load().then(renderContent);
}


// Perform all the required API calls
function load() {
  var notesP = Webfield.getAll('/notes', {invitation: BLIND_INVITATION}).then(function(allNotes) {
    return _.sortBy(
      allNotes.filter(function(note) { return !note.content.hasOwnProperty('withdrawal'); }),
      function(n) { return n.content.title.toLowerCase(); }
    );
  });

  var tagInvitationsP = Webfield.get('/invitations', {id: ADD_BID}).then(function(result) {
    return _.filter(result.invitations, function(invitation) {
      return invitation.invitees.length;
    });
  });

  var metadataNotesP = Webfield.getAll('/notes', {invitation: METADATA_INVITATION}).then(function(allNotes) {
    var metadataMap = {};
    for (var i = 0; i < allNotes.length; i++) {
      metadataMap[allNotes[i].forum] = allNotes[i].content.groups;
    }
    return metadataMap;
  });

  return $.when(notesP, tagInvitationsP, metadataNotesP);
}


// Display the page interface populated with loaded data
function renderContent(validNotes, tagInvitations, metadataNotesMap) {
  addMetadataToNotes(validNotes, metadataNotesMap);

  var activeTab = 0;

  $('#invitation-container').on('shown.bs.tab', 'ul.nav-tabs li a', function(e) {
    activeTab = $(e.target).data('tabIndex');
  });

  $('#invitation-container').on('bidUpdated', '.tag-widget', function(e, tagObj) {
    var updatedNote = _.find(validNotes, ['id', tagObj.forum]);
    if (!updatedNote) {
      return;
    }
    var prevVal = _.has(updatedNote, 'tags[0].tag') ? updatedNote.tags[0].tag : 'No bid';
    updatedNote.tags[0] = tagObj;

    var tagToElemId = {
      'I want to review': '#wantToReview',
      'I can review': '#canReview',
      'I can probably review but am not an expert': '#probablyReview',
      'I cannot review': '#canNotReview',
      'No bid': '#noBid'
    };

    var $sourceContainer = $(tagToElemId[prevVal] + ' .submissions-list');
    var $note = $sourceContainer.find('li.note[data-id="' + tagObj.forum + '"]').detach();
    if (!$sourceContainer.children().length) {
      $sourceContainer.append('<li><p class="empty-message">No papers to display at this time</p></li>');
    }

    var $destContainer = $(tagToElemId[tagObj.tag] + ' .submissions-list');
    if ($destContainer.find('p.empty-message').length) {
      $destContainer.empty();
    }
    $destContainer.prepend($note);

    // For radio button widgets, we need to update the selected value of the widget
    // that wasn't clicked (since there are 2 on the page)
    if ($(this).data('type') === 'radio') {
      var $noteToUpdate;
      var newVal = updatedNote.tags[0].tag;

      if ($(this).closest('.tab-pane').is('#allPapers')) {
        $noteToUpdate = $note;
      } else {
        $noteToUpdate = $('#allPapers').find('li.note[data-id="' + tagObj.forum + '"]');
      }
      $noteToUpdate.find('.tag-widget .radio-toggle[data-value="' + newVal + '"]').button('toggle');
    }

    updateCounts();
  });

  function updateNotes(notes) {
    // Sort notes by bid
    var wantToReview = [];
    var canReview = [];
    var probablyReview = [];
    var canNotReview = [];
    var noBid = [];
    notes.forEach(function(n) {
      if (n.tags.length) {
        if (n.tags[0].tag === 'I want to review') {
          wantToReview.push(n);
        } else if (n.tags[0].tag === 'I can review') {
          canReview.push(n);
        } else if (n.tags[0].tag === 'I can probably review but am not an expert') {
          probablyReview.push(n);
        } else if (n.tags[0].tag === 'I cannot review') {
          canNotReview.push(n);
        } else {
          noBid.push(n);
        }
      } else {
        noBid.push(n);
      }
    });

    var bidCount = wantToReview.length + canReview.length + probablyReview.length + canNotReview.length;

    $('#header h3').remove();
    $('#header').append('<h3>You have completed ' + bidCount + ' bids</h3>');

    var sections = [
      {
        heading: 'All Papers  <span class="glyphicon glyphicon-search"></span>',
        id: 'allPapers',
        content: null
      },
      {
        heading: 'No bid',
        headingCount: noBid.length,
        id: 'noBid',
        content: null
      },
      {
        heading: 'I want to review',
        headingCount: wantToReview.length,
        id: 'wantToReview',
        content: null
      },
      {
        heading: 'I can review',
        headingCount: canReview.length,
        id: 'canReview',
        content: null
      },
      {
        heading: 'I can probably review but am not an expert',
        headingCount: probablyReview.length,
        id: 'probablyReview',
        content: null
      },
      {
        heading: 'I cannot review',
        headingCount: canNotReview.length,
        id: 'canNotReview',
        content: null
      }
    ];
    sections[activeTab].active = true;

    $('#notes .tabs-container').remove();

    Webfield.ui.tabPanel(sections, {
      container: '#notes',
      hidden: true
    });

    var paperDisplayOptions = {
      pdfLink: true,
      replyCount: true,
      showContents: true,
      showTags: true,
      tagInvitations: tagInvitations
    };

    Webfield.ui.submissionList(wantToReview, {
      heading: null,
      container: '#wantToReview',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(canReview, {
      heading: null,
      container: '#canReview',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(probablyReview, {
      heading: null,
      container: '#probablyReview',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(canNotReview, {
      heading: null,
      container: '#canNotReview',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(noBid, {
      heading: null,
      container: '#noBid',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    var submissionListOptions = _.assign({}, paperDisplayOptions, {container: '#allPapers'});
    var sortOptionsList = [
      {
        label: 'Affinity Score',
        compareProp: function(n) {
          // Sort in descending order
          return -1 * n.metadata.affinityScore;
        },
        default: true
      },
      {
        label: 'TPMS Score',
        compareProp: function(n) {
          return -1 * n.metadata.tpmsScore;
        }
      }
    ];
    Webfield.ui.submissionList(notes, {
      heading: null,
      container: '#allPapers',
      search: {
        enabled: true,
        localSearch: true,
        subjectAreas: SUBJECT_AREAS,
        sort: sortOptionsList,
        onResults: function(searchResults) {
          addMetadataToNotes(searchResults, metadataNotesMap);

          // Only include this code if there is a sort dropdown in the search form
          var selectedVal = $('.notes-search-form .sort-dropdown').val();
          if (selectedVal !== 'Default') {
            var sortOption = _.find(sortOptionsList, ['label', selectedVal]);
            if (sortOption) {
              searchResults = _.sortBy(searchResults, sortOption.compareProp);
            }
          }
          Webfield.ui.searchResults(searchResults, submissionListOptions);
        },
        onReset: function() {
          // Only include this code if there is a sort dropdown in the search form
          var selectedVal = $('.notes-search-form .sort-dropdown').val();
          var sortedNotes;
          if (selectedVal !== 'Default') {
            var sortOption = _.find(sortOptionsList, ['label', selectedVal]);
            if (sortOption) {
              sortedNotes = _.sortBy(notes, sortOption.compareProp);
            }
            Webfield.ui.searchResults(sortedNotes, submissionListOptions);
          } else {
            Webfield.ui.searchResults(notes, submissionListOptions);
          }
        },
      },
      displayOptions: submissionListOptions,
      fadeIn: false
    });

    $('#notes .spinner-container').remove();
    $('#notes .tabs-container').show();
  }

  function updateCounts() {
    var containers = [
      '#noBid',
      '#wantToReview',
      '#canReview',
      '#probablyReview',
      '#canNotReview'
    ];
    var totalCount = 0;

    containers.forEach(function(containerId) {
      var numPapers = $(containerId).find('li.note').length;
      if (containerId !== '#noBid') {
        totalCount += numPapers;
      }

      $tab = $('ul.nav-tabs li a[href="' + containerId + '"]');
      $tab.find('span.badge').remove();
      if (numPapers) {
        $tab.append('<span class="badge">' + numPapers + '</span>');
      }
    });

    $('#header h3').remove();
    $('#header').append('<h3>You have completed ' + totalCount + ' bids</h3>');
  }

  updateNotes(validNotes);
}


// Add affinity data from metadata notes to note objects
function addMetadataToNotes(validNotes, metadataNotesMap) {
  var currUserId = user.profile.id;

  for (var i = 0; i < validNotes.length; i++) {
    var note = validNotes[i];
    var metadataNoteGroups = metadataNotesMap[note.id];
    if (_.isEmpty(metadataNoteGroups)) {
      continue;
    }

    var userMetadataObj;
    var groups = Object.keys(metadataNoteGroups);
    var affinityScore = 0;
    var tpmsScore = 0;
    var hasConflict = false;
    for (var j = 0; j < groups.length; j++) {
      userMetadataObj = _.find(metadataNoteGroups[groups[j]], ['userId', currUserId])
      if (userMetadataObj) {
        affinityScore = _.get(userMetadataObj, 'scores.affinity_score', 0);
        tpmsScore = _.get(userMetadataObj, 'scores.tpms_score', 0);
        hasConflict = _.has(userMetadataObj, 'scores.conflict_score');
        break;
      }
    }

    note.metadata = {
      affinityScore: affinityScore,
      tpmsScore: tpmsScore,
      conflict: hasConflict
    };
  }
}

// Go!
main();
