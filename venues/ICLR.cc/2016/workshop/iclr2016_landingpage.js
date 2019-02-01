var GROUP_ID = 'ICLR.cc/2016';
var HEADER = {
  title: 'International Conference on Learning Representations 2016',
  description: 'Welcome to OpenReview for ICLR 2016. Please select a track below.'
};
var VENUE_LINKS = [
  { url: '/group?id=ICLR.cc/2016/workshop', name: 'ICLR 2016 Workshop Track' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
