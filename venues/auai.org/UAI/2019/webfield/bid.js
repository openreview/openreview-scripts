// ------------------------------------
// Add Bid Interface
// ------------------------------------

var CONFERENCE_ID = 'auai.org/UAI/2019/Conference';
var HEADER = {"title": "UAI 2019 Bidding Console", "instructions": "<p class=\"dark\">Please indicate your level of interest in reviewing                 the submitted papers below, on a scale from \"Very Low\" to \"Very High\".</p>                <p class=\"dark\"><strong>Please note:</strong></p>                <ul>                    <li>Please update your Conflict of Interest details on your profile page, specifically \"Emails\", \"Education and Career History\" & \"Advisors and Other Relations\" fields.</li>                    <li>The default bid on each paper is \"No Bid\".</li>                </ul>                <p class=\"dark\"><strong>A few tips:</strong></p>                <ul>                    <li>Please bid on as many papers as possible to ensure that your preferences are taken into account.</li>                    <li>For the best bidding experience, <strong>it is recommended that you filter papers by Subject Area</strong> and search for key phrases in paper metadata using the search form.</li>                </ul>                <p class=\"dark\"><strong>Bid Score Value Mapping:</strong></p>                <ul>                    <li>Very high (+1.0)</li>                    <li>High (+0.5)</li>                    <li>Neutral, No Bid (0.0)</li>                    <li>Low (-0.5) </li>                    <li>Very Low (-1.0)</li>                </ul><br>"};
var SHORT_PHRASE = '';
var BLIND_SUBMISSION_ID = 'auai.org/UAI/2019/Conference/-/Blind_Submission';
var BID_ID = 'auai.org/UAI/2019/Conference/-/Bid';
var SUBJECT_AREAS = ['Algorithms: Approximate Inference', 'Algorithms: Belief Propagation', 'Algorithms: Distributed and Parallel', 'Algorithms: Exact Inference', 'Algorithms: Graph Theory', 'Algorithms: Heuristics', 'Algorithms: MCMC methods', 'Algorithms: Optimization', 'Algorithms: Other', 'Algorithms: Software and Tools', 'Applications: Biology', 'Applications: Databases', 'Applications: Decision Support', 'Applications: Diagnosis and Reliability', 'Applications: Economics', 'Applications: Education', 'Applications: General', 'Applications: Medicine', 'Applications: Other', 'Applications: Planning and Control', 'Applications: Privacy and Security', 'Applications: Robotics', 'Applications: Sensor Data', 'Applications: Social Network Analysis', 'Applications: Speech', 'Applications: Sustainability and Climate', 'Applications: Text and Web Data', 'Applications: User Models', 'Applications: Vision', 'Data: Big Data', 'Data: Multivariate', 'Data: Other', 'Data: Relational', 'Data: Spatial', 'Data: Temporal or Sequential', 'Learning: Active Learning', 'Learning: Classification', 'Learning: Clustering', 'Learning: Deep Learning', 'Learning: General', 'Learning: Nonparametric Bayes', 'Learning: Online and Anytime Learning', 'Learning: Other', 'Learning: Parameter Estimation', 'Learning: Probabilistic Generative Models', 'Learning: Ranking', 'Learning: Recommender Systems', 'Learning: Regression', 'Learning: Reinforcement Learning', 'Learning: Relational Learning', 'Learning: Relational Models', 'Learning: Scalability', 'Learning: Semi-Supervised Learning', 'Learning: Structure Learning', 'Learning: Structured Prediction', 'Learning: Theory', 'Learning: Unsupervised', 'Methodology: Bayesian Methods', 'Methodology: Calibration', 'Methodology: Elicitation', 'Methodology: Evaluation', 'Methodology: Human Expertise and Judgement', 'Methodology: Other', 'Methodology: Probabilistic Programming', 'Models: Bayesian Networks', 'Models: Directed Graphical Models', 'Models: Dynamic Bayesian Networks', 'Models: Markov Decision Processes', 'Models: Mixed Graphical Models', 'Models: Other', 'Models: Relational Models', 'Models: Topic Models', 'Models: Undirected Graphical Models', 'None of the above', 'Principles: Causality', 'Principles: Cognitive Models', 'Principles: Decision Theory', 'Principles: Game Theory', 'Principles: Information Theory', 'Principles: Other', 'Principles: Probability Theory', 'Principles: Statistical Theory', 'Representation: Constraints', 'Representation: Dempster-Shafer', 'Representation: Fuzzy Logic', 'Representation: Influence Diagrams', 'Representation: Non-Probabilistic Frameworks', 'Representation: Probabilistic', 'Representation: Other'];

var USER_SCORES_INVITATION_ID = CONFERENCE_ID + '/-/User_Scores';

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#invitation-container', CONFERENCE_ID);  // required

  Webfield.ui.header(HEADER.title, HEADER.instructions);

  Webfield.ui.spinner('#notes', { inline: true });

  load().then(renderContent).then(Webfield.ui.done);
}


// Perform all the required API calls
function load() {
  var notesP = Webfield.getAll('/notes', {invitation: BLIND_SUBMISSION_ID, details: 'tags'}).then(function(allNotes) {
    return allNotes.map(function(note) {
      note.details.tags = note.details.tags.filter(function(tag) {
        return tag.tauthor;
      });
      return note;
    });
  });

  var authoredNotesP = Webfield.getAll('/notes', {'content.authorids': user.profile.id, invitation: BLIND_SUBMISSION_ID});

  var tagInvitationsP = Webfield.getAll('/invitations', {id: BID_ID}).then(function(invitations) {
    return invitations.filter(function(invitation) {
      return invitation.invitees.length;
    });
  });

  var userScoresP = Webfield.getAll('/notes', {invitation: USER_SCORES_INVITATION_ID}).then(function(scoreNotes) {
    // Build mapping from forum id to an object with the user's scores
    // (tpms and conflict if available)
    var metadataNotesMap = {};
    var userScores = _.find(scoreNotes, ['content.user', user.profile.id]);
    if (!userScores) {
      return metadataNotesMap;
    }

    userScores = userScores.content.scores;
    for (var i = 0; i < userScores.length; i++) {
      metadataNotesMap[userScores[i].forum] = _.omit(userScores[i], ['forum']);
    }
    return metadataNotesMap;
  });

  return $.when(notesP, authoredNotesP, tagInvitationsP, userScoresP);
}


// Display the bid interface populated with loaded data
function renderContent(validNotes, authoredNotes, tagInvitations, metadataNotesMap) {
  var authoredNoteIds = _.map(authoredNotes, function(note){
    return note.id;
  });

  validNotes = _.filter(validNotes, function(note){
    return !_.includes(authoredNoteIds, note.original);
  })
  validNotes = addMetadataToNotes(validNotes, metadataNotesMap);

  var activeTab = 0;
  var sections;
  var binnedNotes;

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true,
    showTags: true,
    tagInvitations: tagInvitations
  };

  $('#invitation-container').on('shown.bs.tab', 'ul.nav-tabs li a', function(e) {
    activeTab = $(e.target).data('tabIndex');
    var containerId = sections[activeTab].id;

    if (containerId !== 'allPapers') {
      setTimeout(function() {
        Webfield.ui.submissionList(binnedNotes[containerId], {
          heading: null,
          container: '#' + containerId,
          search: { enabled: false },
          displayOptions: paperDisplayOptions,
          fadeIn: false
          //pageSize: 50
        });
      }, 100);
    }
  });

  $('#invitation-container').on('hidden.bs.tab', 'ul.nav-tabs li a', function(e) {
    var containerId = $(e.target).attr('href');
    if (containerId !== '#allPapers') {
      Webfield.ui.spinner(containerId, {inline: true});
    }
  });

  $('#invitation-container').on('bidUpdated', '.tag-widget', function(e, tagObj) {
    var updatedNote = _.find(validNotes, ['id', tagObj.forum]);
    if (!updatedNote) {
      return;
    }
    var prevVal = _.has(updatedNote.details, 'tags[0].tag') ? updatedNote.details.tags[0].tag : 'No Bid';

    if (tagObj.ddate) {
      tagObj.tag = 'No Bid';
    }
    updatedNote.details.tags[0] = tagObj;

    var tagToContainerId = {
      'Very High': 'veryHigh',
      'High': 'high',
      'Neutral': 'neutral',
      'Low': 'low',
      'Very Low': 'veryLow',
      'No Bid': 'noBid'
    };

    var previousNoteList = binnedNotes[tagToContainerId[prevVal]];
    var currentNoteList = binnedNotes[tagToContainerId[tagObj.tag]];

    var currentIndex = _.findIndex(previousNoteList, ['id', tagObj.forum]);
    if (currentIndex !== -1) {
      var currentNote = previousNoteList[currentIndex];
      currentNote.details.tags[0] = tagObj;
      previousNoteList.splice(currentIndex, 1);
      currentNoteList.push(currentNote);
    } else {
      console.warn('Note not found!');
    }

    // If the current tab is not the All Papers tab remove the note from the DOM and
    // update the state of tag widget in the All Papers tab
    if (activeTab) {
      var $elem = $(e.target).closest('.note');
      $elem.fadeOut('normal', function() {
        $elem.remove();

        var $container = $('#' + tagToContainerId[prevVal] + ' .submissions-list');
        if (!$container.children().length) {
          $container.append('<li><p class="empty-message">No papers to display at this time</p></li>');
        }
      });

      var $noteToChange = $('#allPapers .submissions-list .note[data-id="' + updatedNote.id + '"]');
      $noteToChange.find('label[data-value="' + prevVal + '"]').removeClass('active')
        .children('input').prop('checked', false);
      $noteToChange.find('label[data-value="' + tagObj.tag + '"]').button('toggle');
    }

    updateCounts();
  });

  function updateNotes(notes) {
    // Sort notes into bins by bid
    binnedNotes = {
      noBid: [],
      veryHigh: [],
      high: [],
      neutral: [],
      low: [],
      veryLow: []
    };

    var bids, n;
    for (var i = 0; i < notes.length; i++) {
      n = notes[i];
      bids = _.filter(n.details.tags, function(t) {
        return t.invitation === BID_ID;
      });

      if (bids.length) {
        if (bids[0].tag === 'Very High') {
          binnedNotes.veryHigh.push(n);
        } else if (bids[0].tag === 'High') {
          binnedNotes.high.push(n);
        } else if (bids[0].tag === 'Neutral') {
          binnedNotes.neutral.push(n);
        } else if (bids[0].tag === 'Low') {
          binnedNotes.low.push(n);
        } else if (bids[0].tag === 'Very Low') {
          binnedNotes.veryLow.push(n);
        } else {
          binnedNotes.noBid.push(n);
        }
      } else {
        binnedNotes.noBid.push(n);
      }
    }

    var bidCount = binnedNotes.veryHigh.length + binnedNotes.high.length +
      binnedNotes.neutral.length + binnedNotes.low.length + binnedNotes.veryLow.length;

    $('#bidcount').remove();
    $('#header').append('<h4 id="bidcount">You have completed ' + bidCount + ' bids</h4>');

    var loadingContent = Handlebars.templates.spinner({ extraClasses: 'spinner-inline' });
    sections = [
      {
        heading: 'All Papers  <span class="glyphicon glyphicon-search"></span>',
        id: 'allPapers',
        content: null
      },
      {
        heading: 'No Bid',
        headingCount: binnedNotes.noBid.length,
        id: 'noBid',
        content: loadingContent
      },
      {
        heading: 'Very High',
        headingCount: binnedNotes.veryHigh.length,
        id: 'veryHigh',
        content: loadingContent
      },
      {
        heading: 'High',
        headingCount: binnedNotes.high.length,
        id: 'high',
        content: loadingContent
      },
      {
        heading: 'Neutral',
        headingCount: binnedNotes.neutral.length,
        id: 'neutral',
        content: loadingContent
      },
      {
        heading: 'Low',
        headingCount: binnedNotes.low.length,
        id: 'low',
        content: loadingContent
      },
      {
        heading: 'Very Low',
        headingCount: binnedNotes.veryLow.length,
        id: 'veryLow',
        content: loadingContent
      }
    ];
    sections[activeTab].active = true;

    $('#notes .tabs-container').remove();

    Webfield.ui.tabPanel(sections, {
      container: '#notes',
      hidden: true
    });

    // Render the contents of the All Papers tab
    var searchResultsOptions = _.assign({}, paperDisplayOptions, { container: '#allPapers' });
    var sortOptionsList = [
      {
        label: 'Affinity Score (TF-IDF)',
        compareProp: function(n) {
          return -1 * n.metadata.tfidfScore;
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
        subjectAreaDropdown: 'basic',
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

          Webfield.ui.searchResults(searchResults, searchResultsOptions);
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
            Webfield.ui.searchResults(sortedNotes, searchResultsOptions);
          } else {
            Webfield.ui.searchResults(notes, searchResultsOptions);
          }
        },
      },
      displayOptions: paperDisplayOptions,
      //pageSize: 50,
      fadeIn: false
    });

    $('#notes > .spinner-container').remove();
    $('#notes .tabs-container').show();

    Webfield.ui.done();
  }

  function updateCounts() {
    var containers = [
      'noBid',
      'veryHigh',
      'high',
      'neutral',
      'low',
      'veryLow'
    ];
    var totalCount = 0;

    containers.forEach(function(containerId) {
      var $tab = $('ul.nav-tabs li a[href="#' + containerId + '"]');
      var numPapers = binnedNotes[containerId].length;

      $tab.find('span.badge').remove();
      if (numPapers) {
        $tab.append('<span class="badge">' + numPapers + '</span>');
      }

      if (containerId != 'noBid') {
        totalCount += numPapers;
      }
    });

    $('#bidcount').remove();
    $('#header').append('<h4 id="bidcount">You have completed ' + totalCount + ' bids</h4>');
  }

  updateNotes(validNotes);
}


// Add affinity data from metadata notes to note objects
function addMetadataToNotes(validNotes, metadataNotesMap) {
  for (var i = 0; i < validNotes.length; i++) {
    var note = validNotes[i];
    var paperMetadataObj = metadataNotesMap.hasOwnProperty(note.id) ? metadataNotesMap[note.id] : {};

    note.metadata = {
      tfidfScore: paperMetadataObj.hasOwnProperty('tfidfScore') ? paperMetadataObj['tfidfScore'] : 0,
      conflict: paperMetadataObj.hasOwnProperty('conflict')
    };

    note.content['TFIDF Score'] = note.metadata.tfidfScore.toFixed(3);
  }

  return validNotes; //_.orderBy(validNotes, ['metadata.tfidfScore'], ['desc']);
}

// Go!
main();
