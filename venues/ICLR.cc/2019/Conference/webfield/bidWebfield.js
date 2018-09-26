// ------------------------------------
// Add Bid Interface
// ------------------------------------

var CONFERENCE_ID = 'ICLR.cc/2019/Conference';
var SHORT_PHRASE = 'ICLR 2019';
var BLIND_INVITATION_ID = CONFERENCE_ID + '/-/Blind_Submission';
var USER_SCORES_INVITATION_ID = CONFERENCE_ID + '/-/User_Scores';
var ADD_BID = CONFERENCE_ID + '/-/Add_Bid';
var PAGE_SIZE = 1000;

var INSTRUCTIONS = '<p class="dark">Please indicate your level of interest in reviewing \
  the submitted papers below, on a scale from "Very Low" to "Very High".</p>\
  <p class="dark"><strong>A few tips:</strong></p>\
  <ul>\
    <li>We expect <strong>approximately 50 bids per user</strong>. Please bid on as many papers as possible to ensure that your preferences are taken into account.</li>\
    <li>You may search for papers by keywords</li>\
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
    return _.sortBy(
      allNotes.filter(function(note) { return !note.content.hasOwnProperty('withdrawal'); }),
      function(n) { return n.content.title.toLowerCase(); }
    );
  });

  var tagInvitationsP = Webfield.getAll('/invitations', {id: ADD_BID}).then(function(invitations) {
    return _.filter(invitations, function(invitation) {
      return invitation.invitees.length;
    });
  });

  var userScoresP = Webfield.getAll('/notes', {invitation: USER_SCORES_INVITATION_ID}).then(function(scoreNotes) {
    // should be keyed on forum, with an object with the user's tpms (and conflict) scores

    userScoreNotes = _.filter(scoreNotes, function(n){
      if(n.content.user === user.profile.id){
        return n;
      }
    })

    var metadataNotesMap = {};

    if (userScoreNotes.length){
      userScores = userScoreNotes[0].content.scores;
    }

    for (var i = 0; i < userScores.length; i++) {
      metadataNotesMap[userScores[i].forum] = userScores[i];
    }
    return metadataNotesMap;
  });

  return $.when(notesP, tagInvitationsP, userScoresP);
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
    var prevVal = _.has(updatedNote.details, 'tags[0].tag') ? updatedNote.details.tags[0].tag : 'No Bid';
    updatedNote.details.tags[0] = tagObj;

    var tagToElemId = {
      'Very High': '#veryHigh',
      'High': '#high',
      'Neutral': '#neutral',
      'Low': '#low',
      'Very Low': '#veryLow',
      'No Bid': '#noBid'
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
      var newVal = updatedNote.details.tags[0].tag;

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
    var veryHigh = [];
    var high = [];
    var neutral = [];
    var low = [];
    var veryLow = [];
    var noBid = [];
    notes.forEach(function(n) {
      var bids = _.filter(n.details.tags, function(t){
        if(t.invitation === ADD_BID){ return t; }
      });

      if (bids.length) {
        if (bids[0].tag === 'Very High') {
          veryHigh.push(n);
        } else if (bids[0].tag === 'High') {
          high.push(n);
        } else if (bids[0].tag === 'Neutral') {
          neutral.push(n);
        } else if (bids[0].tag === 'Low') {
          low.push(n);
        } else if (bids[0].tag === 'Very Low') {
          veryLow.push(n);
        } else {
          noBid.push(n);
        }
      } else {
        noBid.push(n);
      }
    });

    var bidCount = veryHigh.length + high.length + neutral.length + low.length + veryLow.length;

    $('#bidcount').remove();
    $('#header').append('<h4 id="bidcount">You have completed ' + bidCount + ' bids</h4>');

    var sections = [
      {
        heading: 'All Papers  <span class="glyphicon glyphicon-search"></span>',
        id: 'allPapers',
        content: null
      },
      {
        heading: 'No Bid',
        headingCount: noBid.length,
        id: 'noBid',
        content: null
      },
      {
        heading: 'Very High',
        headingCount: veryHigh.length,
        id: 'veryHigh',
        content: null
      },
      {
        heading: 'High',
        headingCount: high.length,
        id: 'high',
        content: null
      },
      {
        heading: 'Neutral',
        headingCount: neutral.length,
        id: 'neutral',
        content: null
      },
      {
        heading: 'Low',
        headingCount: low.length,
        id: 'low',
        content: null
      },
      {
        heading: 'Very Low',
        headingCount: veryLow.length,
        id: 'veryLow',
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

    Webfield.ui.submissionList(veryHigh, {
      heading: null,
      container: '#veryHigh',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(high, {
      heading: null,
      container: '#high',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(neutral, {
      heading: null,
      container: '#neutral',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(low, {
      heading: null,
      container: '#low',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(veryLow, {
      heading: null,
      container: '#veryLow',
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
        label: 'TPMS Score',
        compareProp: function(n) {
          return -1 * n.metadata.tpmsScore;
        },
        default: true
      }
    ];
    Webfield.ui.submissionList(notes, {
      heading: null,
      container: '#allPapers',
      search: {
        enabled: true,
        localSearch: true,
        sort: sortOptionsList,
        onResults: function(searchResults) {
          addMetadataToNotes(searchResults, metadataNotesMap);
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
          addMetadataToNotes(notes, metadataNotesMap);

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

    Webfield.ui.done();
  }

  function updateCounts() {
    var containers = [
      '#noBid',
      '#veryHigh',
      '#high',
      '#neutral',
      '#low',
      '#veryLow'
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

    $('#bidcount').remove();
    $('#header').append('<h4 id="bidcount">You have completed ' + totalCount + ' bids</h4>');
  }

  updateNotes(validNotes);
}


// Add affinity data from metadata notes to note objects
function addMetadataToNotes(validNotes, metadataNotesMap) {
  var currUserId = user.profile.id;

  for (var i = 0; i < validNotes.length; i++) {
    var note = validNotes[i];
    var paperMetadataObj = _.get(metadataNotesMap, note.id, {});

    note.metadata = {
      tpmsScore: _.get(paperMetadataObj, 'tpmsScore', 0),
      conflict: _.has(paperMetadataObj, 'conflict')
    };
  }
}

// Go!
main();
