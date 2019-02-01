var GROUP_ID = 'NIPS.cc/2017';
var HEADER = {
  title: 'Neural Information Processing Systems 2017',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=NIPS.cc/2017/Workshop/Autodiff', name: 'NIPS 2017 Autodiff Workshop' },
  { url: '/group?id=NIPS.cc/2017/Workshop/MLITS', name: 'NIPS 2017 MLITS Workshop' },
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
