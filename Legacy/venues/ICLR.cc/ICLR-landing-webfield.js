var GROUP_ID = 'ICLR.cc';
var HEADER = {
  title: 'International Conference on Learning Representations',
  description: ''
};
var VENUE_LINKS = [
  { url: '/group?id=ICLR.cc/2019/Conference', name: 'ICLR 2019 Conference Track' },
  { url: '/group?id=ICLR.cc/2018/Conference', name: 'ICLR 2018 Conference Track' },
  { url: '/group?id=ICLR.cc/2018/Workshop', name: 'ICLR 2018 Workshop Track' },
  { url: '/group?id=ICLR.cc/2017/conference', name: 'ICLR 2017 Conference Track' },
  { url: '/group?id=ICLR.cc/2017/workshop', name: 'ICLR 2017 Workshop Track' },
  { url: '/group?id=ICLR.cc/2016/workshop', name: 'ICLR 2016 Workshop Track' },
  { url: '/group?id=ICLR.cc/2014', name: 'ICLR 2014 Workshop Track' },
  { url: '/group?id=ICLR.cc/2013', name: 'ICLR 2013 Conference Track' }
];

Webfield.ui.setup('#group-container', GROUP_ID);

Webfield.ui.header(HEADER.title, HEADER.description, { underline: true });

Webfield.ui.linksList(VENUE_LINKS);

OpenBanner.welcome();
