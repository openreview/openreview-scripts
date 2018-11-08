var GROUP_ID = 'machineintelligence.cc/MIC';
var HEADER = {
  title: 'Machine Intelligence Conference 2018',
  description: 'Welcome to OpenReview for MIC 2018. Please select a track below.'
};
var VENUE_LINKS = [
  { url: '/group?id=machineintelligence.cc/MIC/2018/Conference', name: 'MIC 2018 Conference Track' },
  { url: '/group?id=machineintelligence.cc/MIC/2018/Abstract', name: 'MIC 2018 Abstract Track' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
