// ------------------------------------
// Add Bid Interface
// ------------------------------------

var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
var SHORT_PHRASE = 'ICLR 2019';
var BLIND_INVITATION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var USER_SCORES_INVITATION_ID = CONFERENCE_ID + '/-/User_Scores';
var ADD_BID = CONFERENCE_ID + '/-/Add_Bid';
var PAGE_SIZE = 1000;
var SEARCH_KEYWORDS = [
'adversarial', 'adversarial attacks', 'adversarial examples', 'adversarial learning', 'adversarial training', 'attention', 'classification', 'cnn', 'computer vision', 'convolutional neural network', 'convolutional neural networks', 'deep generative models', 'deep learning', 'deep neural networks', 'deep reinforcement learning', 'domain adaptation', 'exploration', 'few-shot learning', 'gan', 'gans', 'generalization', 'generative adversarial network', 'generative adversarial networks', 'generative models', 'graph neural networks', 'imitation learning', 'information theory', 'interpretability', 'machine learning', 'machine translation', 'meta-learning', 'model compression', 'natural language processing', 'neural network', 'neural networks', 'non-convex optimization', 'optimization', 'quantization', 'recurrent neural networks', 'regularization', 'reinforcement learning', 'representation learning', 'robustness', 'semi-supervised learning', 'sgd', 'stochastic gradient descent', 'theory', 'transfer learning', 'unsupervised learning', 'vae', 'variational autoencoder', 'variational inference'
];

var INSTRUCTIONS = '<p class="dark">Please indicate your level of interest in reviewing \
  the submitted papers below, on a scale from "Very Low" to "Very High".</p>\
  <p class="dark"><strong>Please note:</strong></p>\
  <ul>\
    <li><strong>Conflict of interest will be taken into account at the next stage. So, please do not worry about that while bidding.</strong></li>\
    <li>Please update your Conflict of Interest details on your profile page, specifically "Emails", "Education and Career History" & "Advisors and Other Relations" fields.</li>\
  </ul>\
  <p class="dark"><strong>A few tips:</strong></p>\
  <ul>\
    <li>We expect <strong>approximately 50 bids per user</strong>. Please bid on as many papers as possible to ensure that your preferences are taken into account.</li>\
    <li>For the best bidding experience, <strong>it is recommended that you filter papers by Subject Area</strong> and search for key phrases in paper metadata using the search form.</li>\
    <li>Don\'t worry about suspected conflicts of interest during the bidding process. These will be accounted for during the paper matching process.</li>\
    <li>Default bid on each paper is \"No Bid\".</li>\
  </ul><br>'

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#invitation-container', CONFERENCE_ID);  // required

  Webfield.ui.header(SHORT_PHRASE + ' Bidding Console', INSTRUCTIONS);

  Webfield.ui.spinner('#notes', { inline: true });

  load().then(renderContent);
}


// Perform all the required API calls
function load() {
  var notesP = Webfield.getAll('/notes', {invitation: BLIND_INVITATION_ID, details: 'tags'}).then(function(allNotes) {
    return allNotes.filter(function(note) {
      return !note.content.hasOwnProperty('withdrawal');
    });
  });

  var tagInvitationsP = Webfield.getAll('/invitations', {id: ADD_BID}).then(function(invitations) {
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

  return $.when(notesP, tagInvitationsP, userScoresP);
}


// Display the bid interface populated with loaded data
function renderContent(validNotes, tagInvitations, metadataNotesMap) {

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

    // If the current tab is not the All Papers tab remove the note from the DOM
    if (activeTab) {
      var $elem = $(e.target).closest('.note');
      $elem.fadeOut('normal', function() {
        $elem.remove();

        var $container = $('#' + tagToContainerId[prevVal] + ' .submissions-list');
        if (!$container.children().length) {
          $container.append('<li><p class="empty-message">No papers to display at this time</p></li>');
        }
      });
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
        return t.invitation === ADD_BID;
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
    Webfield.ui.submissionList(notes, {
      heading: null,
      container: '#allPapers',
      search: {
        enabled: true,
        localSearch: true,
        subjectAreas: SEARCH_KEYWORDS,
        subjectAreaDropdown: 'basic',
        sort: false,
        onResults: function(searchResults) {
          Webfield.ui.searchResults(searchResults, searchResultsOptions);
        },
        onReset: function() {
          Webfield.ui.searchResults(notes, searchResultsOptions);
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
      tpmsScore: paperMetadataObj.hasOwnProperty('tpmsScore') ? paperMetadataObj['tpmsScore'] : 0,
      conflict: paperMetadataObj.hasOwnProperty('conflict')
    };

    note.content['TPMS Score'] = note.metadata.tpmsScore.toFixed(3);
  }

  return _.orderBy(validNotes, ['metadata.tpmsScore'], ['desc']);
}

// Go!
main();
