var GROUP_ID = 'BNMW_Workshop';
var HEADER = {
  title: 'Brave New Motion Representations',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=cv-foundation.org/CVPR/2017/BNMW', name: 'CVPR 2017 BNMW' },
  { url: '/group?id=ECCV2016.org/BNMW', name: 'ECCV 2018 BNMW' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
