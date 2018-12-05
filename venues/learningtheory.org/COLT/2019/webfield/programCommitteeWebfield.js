// Constants
var HEADER_TEXT = 'Program Committee Console';

var CONFERENCE = 'learningtheory.org/COLT/2019/Conference';

var INSTRUCTIONS = '<p class="dark">This page provides information and status \
  updates for the COLT 2019 Program Committee. It will be regularly updated as the conference \
  progresses, so please check back frequently for news and other updates.</p>';

var SCHEDULE_HTML = '<h4>Coming Soon</h4>\
  <p>\
    <em><strong>Please check back later for updates.</strong></em>\
  </p>';

// Main function is the entry point to the webfield code
var main = function() {
  OpenBanner.venueHomepageLink(CONFERENCE);

  renderHeader();

};

// Render functions
var renderHeader = function() {
  Webfield.ui.setup('#group-container', CONFERENCE);
  Webfield.ui.header(HEADER_TEXT, INSTRUCTIONS);

  var loadingMessage = '<p class="empty-message">Loading...</p>';
  Webfield.ui.tabPanel([
    {
      heading: 'Program Committee Schedule',
      id: 'areachair-schedule',
      content: SCHEDULE_HTML,
      active: true
    }
  ]);
};


main();
