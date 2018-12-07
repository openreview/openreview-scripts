// ------------------------------------
// Add Bid Interface
// ------------------------------------

// Constants
var CONFERENCE = 'ACM.org/SIGIR/Badging';
var BLIND_INVITATION = CONFERENCE + '/-/Submission';
var ADD_BID = CONFERENCE + '/-/Decision'
var SUBJECT_AREAS_LIST = [];
var PAGE_SIZE = 1000;

// Main is the entry point to the webfield code and runs everything
function main() {

  Webfield.ui.setup('#invitation-container', CONFERENCE);  // required

  Webfield.ui.header('ACM SIGIR Decision');

  Webfield.ui.spinner('#notes', { inline: true });

  OpenBanner.breadcrumbs([
    { link: '/', text: 'Venues' },
    { link: '/group?id=' + CONFERENCE, text: view.prettyId(CONFERENCE) }
  ]);

  load().then(renderContent).then(Webfield.ui.done);
}

function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {
    pageSize: PAGE_SIZE,
    details: 'tags'
  });

  var tagInvitationsP = Webfield.get('/invitations', {id: ADD_BID}).then(function(result) {
    return result.invitations;
  });

  return $.when(notesP, tagInvitationsP);
}

function renderContent(allNotes, tagInvitations) {
  var activeTab = 0;

  var validNotes = allNotes;

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true,
    showTags: true,
    tagInvitations: tagInvitations
  };

  $('#invitation-container').on('shown.bs.tab', 'ul.nav-tabs li a', function(e) {
    activeTab = $(e.target).data('tabIndex');
  });

  $('#invitation-container').on('tagUpdated', '.tag-widget', function(e, tagObj) {
    console.log('tagObj', tagObj);
    var updatedNote = _.find(validNotes, ['id', tagObj.forum]);
    if (!updatedNote) {
      return;
    }

    if (tagObj.ddate) {
      var index = updatedNote.details.tags.findIndex(function(t) {
        return t.id == tagObj.id;
      });

      if (index >= 0) {
        updatedNote.details.tags.splice(index, 1);
      }

    } else {
      updatedNote.details.tags.push(tagObj);
    }

    updateNotes(validNotes);

  });

  function updateNotes(notes) {
    // Sort notes by bid
    var available = [];
    var evaluated = [];
    var replicated = [];
    var reproduced = [];
    var noBadges = [];
    notes.forEach(function(n) {
      if (n.details && n.details.tags && n.details.tags.length) {

        n.details.tags.forEach(function(t) {

          if (t.tag === 'Artifacts Available') {
            available.push(n);
          };

          if (t.tag === 'Artifacts Evaluated – Functional and Reusable') {
            evaluated.push(n);
          }

          if (t.tag === 'Results Replicated') {
            replicated.push(n);
          }

          if (t.tag === 'Results Reproduced') {
            reproduced.push(n);
          }

          if (t.tag === 'No Badges') {
            noBadges.push(n);
          }
        });

      } else {
        noBadges.push(n);
      }
    });


    var sections = [
      {
        heading: 'All Papers &nbsp;<span class="glyphicon glyphicon-search"></span>',
        id: 'allPapers',
        content: null
      },
      {
        heading: 'No badges',
        headingCount: noBadges.length,
        id: 'noBadges',
        content: null
      },
      {
        heading: 'Artifacts Available',
        headingCount: available.length,
        id: 'available',
        content: null
      },
      {
        heading: 'Artifacts Evaluated',
        headingCount: evaluated.length,
        id: 'evaluated',
        content: null
      },
      {
        heading: 'Results Replicated',
        headingCount: replicated.length,
        id: 'replicated',
        content: null
      },
      {
        heading: 'Results Reproduced',
        headingCount: reproduced.length,
        id: 'reproduced',
        content: null
      }
    ];

    sections[activeTab].active = true;

    $('#notes .tabs-container').remove();
    Webfield.ui.tabPanel(sections, {
      container: '#notes',
      hidden: true
    });

    Webfield.ui.submissionList(available, {
      heading: null,
      container: '#available',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(evaluated, {
      heading: null,
      container: '#evaluated',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(replicated, {
      heading: null,
      container: '#replicated',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(reproduced, {
      heading: null,
      container: '#reproduced',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    Webfield.ui.submissionList(noBadges, {
      heading: null,
      container: '#noBadges',
      search: { enabled: false },
      displayOptions: paperDisplayOptions,
      fadeIn: false
    });

    var submissionListOptions = _.assign({}, paperDisplayOptions, {container: '#allPapers'});
    Webfield.ui.submissionList(notes, {
      heading: null,
      container: '#allPapers',
      search: {
        enabled: true,
        subjectAreas: SUBJECT_AREAS_LIST,
        onResults: function(searchResults) {
          var blindedSearchResults = searchResults.filter(function(note) {
            return note.invitation === BLIND_INVITATION;
          });
          Webfield.ui.searchResults(blindedSearchResults, submissionListOptions);
        },
        onReset: function() {
          Webfield.ui.searchResults(notes, submissionListOptions);
        }
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

// Go!
main();
