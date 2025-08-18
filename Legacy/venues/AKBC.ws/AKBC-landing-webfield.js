var GROUP_ID = 'AKBC.ws';
var HEADER = {
  title: 'Automated Knowledge Base Construction',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=AKBC.ws/2019/Conference', name: 'AKBC 2019 Conference Track' },
  { url: '/group?id=AKBC.ws/2013', name: 'AKBC 2013 Workshop Track' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
