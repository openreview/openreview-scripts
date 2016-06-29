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



var hugo = {
  id:'hugo@openreview.net',
  password: '12345678'
}
var programChair_1 = {
  'id': 'ICLR.cc/2017/workshop/programChairs/1',
  'members': [hugo.id],
  'signatories':['ICLR.cc/2017/workshop/programChairs/1',hugo.id]
}
module.exports.hugo = hugo;
module.exports.programChair_1 = programChair_1;



var oriol = {
  id:'oriol@openreview.net',
  password: '12345678'
}
var programChair_2 = {
  'id': 'ICLR.cc/2017/workshop/programChairs/2',
  'members': [oriol.id],
  'signatories':['ICLR.cc/2017/workshop/programChairs/2',oriol.id]
}
module.exports.oriol = oriol;
module.exports.programChair_2 = programChair_2;



var marcAurelio = {
  id:'marcAurelio@openreview.net',
  password: '12345678'
}
var programChair_3 = {
  'id': 'ICLR.cc/2017/workshop/programChairs/3',
  'members': [marcAurelio.id],
  'signatories':['ICLR.cc/2017/workshop/programChairs/3',marcAurelio.id]
}
module.exports.marcAurelio = marcAurelio;
module.exports.programChair_3 = programChair_3;



var tara = {
  id:'tara@openreview.net',
  password: '12345678'
}
var programChair_4 = {
  'id': 'ICLR.cc/2017/workshop/programChairs/4',
  'members': [tara.id],
  'signatories':['ICLR.cc/2017/workshop/programChairs/4',tara.id]
}
module.exports.tara = tara;
module.exports.programChair_4 = programChair_4;



var michael = {
  id: 'spector@cs.umass.edu',
  password: '12345678'
};
var areaChair_1 = {
  'id':'ICLR.cc/2017/workshop/areaChairs/1',
  'members':[michael.id],
  'signatories':['Area_Chair_1',michael.id]
};
module.exports.michael = michael;
module.exports.areaChair_1 = areaChair_1



//ICLR.cc aready exists; may want to overwrite, though
var iclr = {
  'id': 'ICLR.cc',
  'signatures': [rootUser.id],
  'writers': [rootUser.id],
  'members': [],
  'readers': ['everyone'],
  'signatories': ['ICLR.cc']
};
module.exports.iclr = iclr;

var iclr17 = {
  'id': 'ICLR.cc/2017',
  'signatures': ['ICLR.cc'],
  'writers': ['ICLR.cc'],
  'readers': ['everyone'],
  'members': programChairs,
  'signatories': ['ICLR.cc/2017']
};
module.exports.iclr17 = iclr17;

var workshop = {
  'id': 'ICLR.cc/2017/workshop',
  'signatures': ['ICLR.cc/2017'],
  'writers': ['ICLR.cc/2017'],
  'readers': ['everyone'],
  'members': ['Program_Chair_1', 'Area_Chair_1'],
  'signatories': ['ICLR.cc/2017', 'ICLR.cc/2017/workshop'],
  'web': fs.readFileSync('./iclr2017_webfield.html', "utf8")
};
module.exports.workshop = workshop

var areaChairs = {
  'id':'ICLR.cc/2017/workshop/areaChairs',
  'signatures':['ICLR.cc/2017/workshop'],
  'writers':['ICLR.cc/2017/workshop'],
  'readers':['everyone'],
  'members':[areaChair_1.id],
  'signatories':[]
}

var programChairs = {
  'id': workshop.id+'/programChairs',
  'signatures': [workshop.id],
  'writers': [workshop.id],
  'readers': ['everyone'],
  'members': [programChair_1.id, programChair_2.id, programChair_3.id, programChair_4.id],
  'signatories':[workshop.id]
};


