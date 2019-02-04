var GROUP_ID = 'auai.org/UAI';
var HEADER = {
  title: 'Conference on Uncertainty in Artificial Intelligence',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=auai.org/UAI/2019', name: 'UAI 2019' },
  { url: '/group?id=auai.org/UAI/2018', name: 'UAI 2018' },
  { url: '/group?id=auai.org/UAI/2017', name: 'UAI 2017' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
