var GROUP_ID = 'NIPS.cc';
var HEADER = {
  title: 'Neural Information Processing Systems',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=NIPS.cc/2018/Workshop/Spatiotemporal', name: 'NIPS 2018 Spatiotemporal Workshop' },
  { url: '/group?id=NIPS.cc/2018/Workshop/IRASL', name: 'NIPS 2018 IRASL Workshop' },
  { url: '/group?id=NIPS.cc/2018/Workshop/MLITS', name: 'NIPS 2018 MLITS Workshop' },
  { url: '/group?id=NIPS.cc/2018/Workshop/MLOSS', name: 'NIPS 2018 MLOSS Workshop' },
  { type: 'divider' },
  { url: '/group?id=NIPS.cc/2017/Workshop/Autodiff', name: 'NIPS 2017 Autodiff Workshop' },
  { url: '/group?id=NIPS.cc/2017/Workshop/MLITS', name: 'NIPS 2017 MLITS Workshop' },
  { type: 'divider' },
  { url: '/group?id=NIPS.cc/2016/Deep_Learning_Symposium', name: 'NIPS 2016 Deep Learning Symposium' },
  { url: '/group?id=NIPS.cc/2016/workshop/MLITS', name: 'NIPS 2016 MLITS Workshop' },
  { url: '/group?id=NIPS.cc/2016/workshop/NAMPI', name: 'NIPS 2016 NAMPI Workshop' },
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
