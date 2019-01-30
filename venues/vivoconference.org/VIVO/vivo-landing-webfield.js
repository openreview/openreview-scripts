var GROUP_ID = 'VIVOCONFERENCE.org';
var HEADER = {
  title: 'VIVO Conference',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=VIVOConference.org/2019/Conference', name: 'VIVO 2019 Conference' },
  { type: 'divider' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();