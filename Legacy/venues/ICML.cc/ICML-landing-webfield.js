var GROUP_ID = 'ICML.cc';
var HEADER = {
  title: 'International Conference on Machine Learning',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=ICML.cc/2018/ECA', name: 'ICML 2018 ECA' },
  { url: '/group?id=ICML.cc/2018/Workshop/NAMPI', name: 'ICML 2018 NAMPI' },
  { url: '/group?id=ICML.cc/2018/RML', name: 'ICML 2018 RML' },
  { type: 'divider' },
  { url: '/group?id=ICML.cc/2017/MLAV', name: 'ICML 2017 MLAV' },
  { url: '/group?id=ICML.cc/2017/RML', name: 'ICML 2017 RML' },
  { url: '/group?id=ICML.cc/2017/WHI', name: 'ICML 2017 WHI' },
  { type: 'divider' },
  { url: '/group?id=ICML.cc/2013/Inferning', name: 'ICML 2013 Inferning' },
  { url: '/group?id=ICML.cc/2013/PeerReview', name: 'ICML 2013 PeerReview' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
