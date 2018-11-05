var GROUP_ID = 'ICLR.cc/2018';
var HEADER = {
  title: 'International Conference on Learning Representations 2018',
  description: 'Welcome to OpenReview for ICLR 2018. Please select a track below.'
};
var VENUE_LINKS = [
  { url: '/group?id=ICLR.cc/2018/Conference', name: 'ICLR 2018 Conference Track' },
  { url: '/group?id=ICLR.cc/2018/Workshop', name: 'ICLR 2018 Workshop Track' },
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
