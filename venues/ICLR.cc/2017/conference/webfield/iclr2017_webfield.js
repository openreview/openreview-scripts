var GROUP_ID = 'ICLR.cc/2017';
var HEADER = {
  title: 'International Conference on Learning Representations 2017',
  description: 'Welcome to OpenReview for ICLR 2017. Please select a track below.'
};
var VENUE_LINKS = [
  { url: '/group?id=ICLR.cc/2017/conference', name: 'ICLR 2017 Conference Track' },
  { url: '/group?id=ICLR.cc/2017/workshop', name: 'ICLR 2017 Workshop Track' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
