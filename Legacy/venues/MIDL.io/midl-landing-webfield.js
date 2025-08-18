var GROUP_ID = 'MIDL.io';
var HEADER = {
  title: 'Medical Imaging with Deep Learning',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=MIDL.io/2019/Conference/Full', name: 'MIDL 2019 Full Paper' },
  { type: 'divider' },
  { url: '/group?id=MIDL.amsterdam/2018/Conference', name: 'MIDL 2018 Conference Track' },
  { url: '/group?id=MIDL.amsterdam/2018/Abstract', name: 'MIDL 2018 Abstract Track' },
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();