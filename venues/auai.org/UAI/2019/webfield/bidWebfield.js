// ------------------------------------
// Add Bid Interface
// ------------------------------------

//<CONFERENCE>
//<AREA_CHAIRS>
//<SUBTITLE>
//<TITLE>
//<RECRUIT_REVIEWERS>
//<PROGRAM_CHAIRS>
//<DEADLINE>
//<DATE>
//<BLIND_INVITATION>
//<METADATA_INVITATION>
//<INSTRUCTIONS>
//<WEBSITE>
//<REVIEWERS>
//<LOCATION>
//<SUBMISSION_INVITATION>
//<CONFERENCE_REGEX>
//<WILDCARD_INVITATION>
//<SUBJECT_AREAS>

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
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {pageSize: PAGE_SIZE}).then(function(allNotes) {
    return allNotes.filter(function(note) {
      return !note.content.hasOwnProperty('withdrawal');
    });
  });

  var tagInvitationsP = Webfield.get('/invitations', {id: ADD_BID}).then(function(result) {
    return _.filter(result.invitations, function(invitation) {
      return invitation.invitees.length;
    });
  });

  var metadataNotesP = Webfield.get('/notes', {invitation: METADATA_INVITATION}).then(function(result) {
    if (_.isEmpty(result.notes)) {
      return {};
    }

    var metadataMap = {};
    for (var i = 0; i < result.notes.length; i++) {
      var note = result.notes[i];
      metadataMap[note.forum] = note.content.groups;
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
    var sortOptionsList = [{
      label: 'Affinity Score',
      compareProp: function(n) {
        // Sort in descending order
        return -1 * n.metadata.affinityScore;
      },
      default: true
    }];
    Webfield.ui.submissionList(notes, {
      heading: null,
      container: '#allPapers',
      search: {
        enabled: true,
        subjectAreas: SUBJECT_AREAS,
        sort: sortOptionsList,
        onResults: function(searchResults) {
          var blindedSearchResults = searchResults.filter(function(note) {
            return note.invitation === BLIND_INVITATION;
          });
          addMetadataToNotes(blindedSearchResults, metadataNotesMap);

          // Only include this code if there is a sort dropdown in the search form
          var selectedVal = $('.notes-search-form .sort-dropdown').val();
          if (selectedVal !== 'Default') {
            var sortOption = _.find(sortOptionsList, ['label', selectedVal]);
            if (sortOption) {
              blindedSearchResults = _.sortBy(blindedSearchResults, sortOption.compareProp);
            }
          }
          Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
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
  var userEmail = user.profile.email;

  for (var i = 0; i < validNotes.length; i++) {
    var note = validNotes[i];
    var metadataNoteGroups = metadataNotesMap[note.id];
    if (_.isEmpty(metadataNoteGroups)) {
      continue;
    }

    var groups = Object.keys(metadataNoteGroups);
    var affinityScore = 0;
    var hasConflict = false;
    for (var j = 0; j < groups.length; j++) {
      if (metadataNoteGroups[groups[j]][userEmail]) {
        affinityScore = _.get(metadataNoteGroups, [groups[j], userEmail, 'affinity_score'], 0);
        hasConflict = _.has(metadataNoteGroups, [groups[j], userEmail, 'conflict_score']);
        break;
      }
    }

    note.metadata = {
      affinityScore: affinityScore,
      conflict: hasConflict
    };
  }
}

// Go!
main();
