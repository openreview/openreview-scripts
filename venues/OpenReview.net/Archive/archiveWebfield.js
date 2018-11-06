// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header),
// important instructions for this phase of the conference,
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE_ID = 'OpenReview.net/Archive';
var DIRECT_UPLOAD_ID = CONFERENCE_ID + '/-/Direct_Upload';
// var HOMEPAGE_UPLOAD_ID = CONFERENCE_ID + '/-/Homepage_Upload';

var HEADER = {
  title: 'OpenReview Archive',
  subtitle: 'Publication Upload Portal for Paper-Reviewer Matching',
  location: 'Global',
  date: 'Ongoing',
  website: 'https://openreview.net',
  instructions: '<p><strong>Instructions</strong><br>\
    The OpenReview paper-reviewer matching system uses the text from your submitted papers to match you with papers that are relevant to you.\
    Listed below are your authored papers that we currently have on record.\
    </p><p>\
    There are two ways to add papers:\n\
    <ul>\
    <li><strong>Upload a paper</strong>: provide either a URL to a pdf file, <strong>or</strong> upload the PDF from your hard drive.</li>\
    <li><strong>Enter a publications page</strong>: Go to your <strong><a href=/profile>profile</a></strong> and ensure that the \"homepage\" field contains the URL of a page containing PDF links to your publications. If you have already done this and your publications do not appear in the list below, please contact us at <a href="mailto:info@openreview.net">info@openreview.net</a></li>\
    </ul><br>\
    <em>A few important tips:</em>\
    <ul>\
    <li>Direct Uploads are posted privately by default.</li>\
    <li>Direct Uploads <strong>only require a PDF or a URL to a PDF</strong>. The other fields are recommended, but optional.</li>\
    <li>OpenReview will attempt to fill in missing fields from the contents of the PDF.</li>\
    </ul>\
    </p> \
    <p><strong>Questions?</strong><br> \
    Please contact the OpenReview support team at \
    <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform. \</br> \
    </p>',
}

var BUFFER = 1000 * 60 * 30;  // 30 minutes
var PAGE_SIZE = 50;

var paperDisplayOptions = {
  pdfLink: true,
  replyCount: true,
  showContents: true,
  showDetails: true
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

  renderSubmissionButton(DIRECT_UPLOAD_ID);
  // renderSubmissionButton(HOMEPAGE_UPLOAD_ID);

  renderConferenceTabs();

  load().then(renderContent);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {

  var authorNotesP;
  var directUploadsP;
  if (!user || _.startsWith(user.id, 'guest_')) {
    authorNotesP = $.Deferred().resolve([]);
    directUploadsP = $.Deferred().resolve([]);
  } else {
    authorNotesP = Webfield.get('/notes', {
      'content.authorids': user.profile.id,
      // invitation: DIRECT_UPLOAD_ID,
      details: 'forumContent,writable'
    }).then(function(result) {
      return result.notes;
    });

    directUploadsP = Webfield.get('/notes', {
      invitation: DIRECT_UPLOAD_ID,
      details: 'writable'
    }).then(function(result) {
      return result.notes;
    });



  }
  return $.when(authorNotesP, directUploadsP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader(HEADER);

  Webfield.ui.spinner('#notes');
}

function renderSubmissionButton(INVITATION_ID) {
  Webfield.api.getSubmissionInvitation(INVITATION_ID, {deadlineBuffer: BUFFER})
    .then(function(invitation) {
      Webfield.ui.submissionButton(invitation, user, {
        onNoteCreated: function() {
          // Callback funtion to be run when a paper has successfully been submitted (required)
          promptMessage('Your submission is complete.');

          load().then(renderContent).then(function() {
            $('.tabs-container a[href="#user-uploaded-papers"]').click();
          });
        }
      });
    });
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Your Papers',
      id: 'user-uploaded-papers',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(authorNotes,directUploadNotes) {

  var allNotes = authorNotes.concat(directUploadNotes);

  if (allNotes.length) {
    var displayOptions = {
      container: '#user-uploaded-papers',
      user: user && user.profile,
      heading: null,
      showActionButtons: true
    };

    $(displayOptions.container).empty();

    Webfield.ui.submissionList(allNotes, displayOptions);

    $('.tabs-container a[href="#user-uploaded-papers"]').parent().show();
  } else {
    $('.tabs-container a[href="#user-uploaded-papers"]').parent().hide();
  }

  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

  // Show first available tab
  if (initialPageLoad) {
    $('.tabs-container ul.nav-tabs li a:visible').eq(0).click();
    initialPageLoad = false;
  }

  Webfield.ui.done();
}

// Go!
main();
