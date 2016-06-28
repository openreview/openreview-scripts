var or3client = require('../../../or3/client');
var fs = require('fs');
var _ = require('lodash');

var headers = { 'User-Agent': 'test-create-script' }; //what are these?

var rootUser = {
  id:'OpenReview.net',
  password:'12345678'
}

module.exports = {
  'headers':headers,
  'rootUser':rootUser
};

//ICLR.cc aready exists
var iclr = {
  'id': 'ICLR.cc',
  'signatures': [rootUser.id],
  'writers': ['ICLR.cc', rootUser.id],
  'members': [rootUser.id],
  'readers': ['everyone'],
  'signatories': ['ICLR.cc']
};
module.exports.iclr = iclr;

var iclr17 = {
  'id': 'ICLR.cc/2017',
  'signatures': [rootUser.id],
  'writers': ['ICLR.cc/2017'],
  'readers': ['everyone'],
  'members': pcs,
  'signatories': ['ICLR.cc/2017']
};
module.exports.iclr17 = iclr17;

var workshop = {
  'id': 'ICLR.cc/2017/workshop',
  'signatures': [rootUser.id],
  'writers': ['ICLR.cc/2017'],
  'readers': ['everyone'],
  'members': ['ICLR.cc/2017'],
  'signatories': ['ICLR.cc/2017', 'ICLR.cc/2017/workshop'],
  'web': fs.readFileSync('./iclr2017_webfield.html', "utf8")
};
module.exports.workshop = workshop

var michael = {
  id: 'spector@cs.umass.edu',
  password: 12345678
}

var hugo = {
  id: 'hugo@openreview.net'
};
var marcAurelio = {
  id:'marcAurelio@openreview.net'
};
var tara = {
  id:'tara@openreview.net'
};
var oriol = {
  id:'oriol@openreview.net'
};

var AC1 = {
  id:'Area_Chair-1'
}
module.exports.AC1 = AC1;

var AC2 = {
  id:'Area_Chair-2'
}
module.exports.AC2 = AC2;


var pcs = [michael.id];
module.exports.pcs = pcs;