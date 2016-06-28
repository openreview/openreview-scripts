var or3client = require('../../../or3/client');
var fs = require('fs');
var _ = require('lodash');

var headers = { 'User-Agent': 'test-create-script' }; //what are these?

var rootUser = {
  id:'OpenReview.net',
  password:'12345678'
}

//PCs
var u1 = {
    'id': 'u1@host.com',
    'needsPassword': true
};

var u2 = {
    'id': 'u2@host.com',
    'needsPassword': true
};

var u3 = {
    'id': 'u3@host.com',
    'needsPassword': true
};

var pcs = {'u1':u1, 'u2':u2, 'u3':u3};

var iclr = {
  'id': 'ICLR.cc',
  'signatures': [rootUser.id],
  'writers': ['ICLR.cc', rootUser.id],
  'members': [rootUser.id],
  'readers': ['everyone'],
  'signatories': ['ICLR.cc']
};

var iclr16 = {
  'id': 'ICLR.cc/2016',
  'signatures': [rootUser.id],
  'writers': ['ICLR.cc/2016'],
  'readers': ['everyone'],
  'members': ['u1@host.com','u2@host.com', 'u3@host.com'],
  'signatories': ['ICLR.cc/2016']
};

var workshop = {
  'id': 'ICLR.cc/2016/workshop',
  'signatures': [rootUser.id],
  'writers': ['ICLR.cc/2016'],
  'readers': ['everyone'],
  'members': ['ICLR.cc/2016'],
  'signatories': ['ICLR.cc/2016', 'ICLR.cc/2016/workshop'],
  'web': fs.readFileSync('./iclr2016_webfield.html', "utf8")
};

var conference = {
  'id': 'ICLR.cc/2016/conference',
  'signatures': [rootUser.id],
  'writers': ['ICLR.cc/2016'],
  'readers': ['everyone'],
  'members': ['ICLR.cc/2016'],
  'signatories': ['ICLR.cc/2016']
};

var paper = {
  'id': 'ICLR.cc/2016/workshop/paper',
  'signatures': [rootUser.id],
  'writers': [workshop.id],
  'readers': ['everyone'],
  'members': [workshop.id],
  'signatories': ['ICLR.cc/2016/workshop/paper', 'ICLR.cc/2016/workshop']
};

module.exports = {
  'headers':headers,
  'rootUser':rootUser,
  'pcs':pcs,
  'iclr':iclr,
  'iclr16':iclr16,
  'workshop':workshop,
  'conference':conference,
  'paper':paper
};