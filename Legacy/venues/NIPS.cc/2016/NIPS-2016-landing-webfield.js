var GROUP_ID = 'NIPS.cc/2016';
var HEADER = {
  title: 'Neural Information Processing Systems 2016',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=NIPS.cc/2016/Deep_Learning_Symposium', name: 'NIPS 2016 Deep Learning Symposium' },
  { url: '/group?id=NIPS.cc/2016/workshop/MLITS', name: 'NIPS 2016 MLITS Workshop' },
  { url: '/group?id=NIPS.cc/2016/workshop/NAMPI', name: 'NIPS 2016 NAMPI Workshop' },
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
