var GROUP_ID = 'swsa.semanticweb.org/ISWC';
var HEADER = {
  title: 'Decentralizing the Semantic Web Workshop at the International Semantic Web Conference',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=swsa.semanticweb.org/ISWC/2018/DeSemWeb', name: 'DeSemWeb 2018' },
  { url: '/group?id=swsa.semanticweb.org/ISWC/2017/DeSemWeb', name: 'DeSemWeb 2017' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
