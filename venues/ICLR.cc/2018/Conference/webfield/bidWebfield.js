// ------------------------------------
// Add Bid Interface
// ------------------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2018/Conference';
var BLIND_INVITATION = CONFERENCE + '/-/Blind_Submission';
var ADD_BID = CONFERENCE + '/-/Add_Bid'
var SUBJECT_AREAS_LIST = [];
var PAGE_SIZE = 1000;

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#invitation-container', CONFERENCE);  // required

  Webfield.ui.header('ICLR 2018 Paper Bidding');  // ICLR specific

  Webfield.ui.spinner('#notes');

  OpenBanner.breadcrumbs([
    { link: '/', text: 'Venues' },
    { link: '/group?id=' + CONFERENCE, text: view.prettyId(CONFERENCE) }
  ]);

  load().then(renderContent);
}

function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, {
    pageSize: PAGE_SIZE
  });

  var tagInvitationsP = Webfield.get('/invitations', {id: ADD_BID}).then(function(result) {
    return _.filter(result.invitations, function(invitation) {
      return invitation.invitees.length;
    });
  });

  return $.when(notesP, tagInvitationsP);
}

function renderContent(allNotes, tagInvitations) {
  var activeTab = 0;

  var validNotes = allNotes.filter(function(note) {
    return !note.content.hasOwnProperty('withdrawal');
  });

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

  $('#invitation-container').on('bidUpdated', '.tag-widget', function(e, tagObj) {
    var updatedNote = _.find(validNotes, ['id', tagObj.forum]);
    if (!updatedNote) {
      return;
    }
    updatedNote.tags[0] = tagObj;
    updateNotes(validNotes);
  });

  function updateNotes(notes) {
    // Sort notes by bid
    var wantToReview = [];
    var canReview = [];
    var probablyReview = [];
    var canNotReview = [];
    var noBid = [];
    _.forEach(notes, function(n) {
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
      },
      {
        heading: 'All Papers &nbsp;<span class="glyphicon glyphicon-search"></span>',
        id: 'allPapers',
        content: null
      }
    ];
    sections[activeTab].active = true;
    $('#notes .tabs-container').remove();
    Webfield.ui.tabPanel(sections, {
      container: '#notes',
      hidden: true
    });

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

  updateNotes(validNotes);
}

// Go!
main();
