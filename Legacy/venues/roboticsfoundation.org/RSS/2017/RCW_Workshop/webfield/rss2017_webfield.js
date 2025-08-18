var GROUP_ID = 'roboticsfoundation.org/RSS';
var HEADER = {
  title: 'Robot Communication in the Wild: Meeting the Challenges of Real-world Systems',
  description: 'Welcome to OpenReview for RSS 2017 RCW Workshop. Please select a track below.'
};
var VENUE_LINKS = [
  { url: '/group?id=roboticsfoundation.org/RSS/2017/RCW_Workshop/-_Poster', name: 'RSS 2017 RCW - Poster Track' },
  { url: '/group?id=roboticsfoundation.org/RSS/2017/RCW_Workshop/-_Proceedings', name: 'RSS 2017 RCW - Proceedings Track' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
