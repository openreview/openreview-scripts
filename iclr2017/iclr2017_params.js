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


/*

SCENARIO DETAILS:

*/


//ICLR.cc ALREADY EXISTS! In test, we can post this group, but make sure that you thoroughly test interactions with the old ICLR groups
var iclr = {
  'id': 'ICLR.cc',
  'signatures': [rootUser.id],
  'writers': [rootUser.id],
  'members': [],
  'readers': ['everyone'],
  'signatories': ['ICLR.cc']
};

var iclr2017 = {
  'id': iclr.id+'/2017',
  'signatures': [iclr.id],
  'writers': [iclr.id],
  'readers': ['everyone'],
  'members': [],
  'signatories': [iclr.id+'/2017']
};

var iclr2017workshop = {
  'id': iclr2017.id+'/workshop',
  'signatures': [iclr2017.id],
  'writers': [iclr2017.id],
  'readers': ['everyone'],
  'members': [], //members of the workshop group are set below
  'signatories': [],
  'web': fs.readFileSync('./iclr2017_webfield.html', "utf8")
};

var iclr2017workshopAreaChairs = {
  'id': iclr2017workshop.id+'/areaChairs',
  'signatures':[iclr2017workshop.id],
  'writers':[iclr2017workshop.id],
  'readers':['everyone'],
  'members':[], //members of the area chairs group are set below
  'signatories':[]
}

var iclr2017workshopProgramChairs = {
  'id': iclr2017workshop.id+'/programChairs',
  'signatures': [iclr2017workshop.id],
  'writers': [iclr2017workshop.id],
  'readers': ['everyone'],
  'members': [], //members of program chairs group are set below
  'signatories':[]
};



var hugo = {
  'id': 'hugo@openreview.net',
  'first':'Hugo',
  'last':'LaRochelle'
};
var programChair_1 = {
  'id': iclr2017workshopProgramChairs.id+'/1',
  'signatures':[iclr2017workshopProgramChairs.id],
  'writers':[iclr2017workshopProgramChairs.id],
  'readers':['everyone'],
  'members': [hugo.id],
  'signatories': [iclr2017workshopProgramChairs.id+'/1', hugo.id]
};



var oriol = {
  id: 'oriol@openreview.net',
  first: 'Oriol',
  last: 'Vinyals'
}
var programChair_2 = {
  'id': iclr2017workshopProgramChairs.id+'/2',
  'signatures':[iclr2017workshopProgramChairs.id],
  'writers':[iclr2017workshopProgramChairs.id],
  'readers':['everyone'],
  'members': [oriol.id],
  'signatories':[iclr2017workshopProgramChairs.id+'/2', oriol.id]
}


var marcAurelio = {
  id:'marcAurelio@openreview.net',
  first:'MarcAurelio',
  last:'Ranzato'
};
var programChair_3 = {
  'id': iclr2017workshopProgramChairs.id+'/3',
  'signatures':[iclr2017workshopProgramChairs.id],
  'writers':[iclr2017workshopProgramChairs.id],
  'readers':['everyone'],
  'members': [marcAurelio.id],
  'signatories':[iclr2017workshopProgramChairs.id+'/3', marcAurelio.id]
};


var tara = {
  id:'tara@openreview.net',
  first:'Tara',
  last:'Sainath'
};
var programChair_4 = {
  'id': iclr2017workshopProgramChairs.id+'/4',
  'signatures':[iclr2017workshopProgramChairs.id],
  'writers':[iclr2017workshopProgramChairs.id],
  'readers':['everyone'],
  'members': [tara.id],
  'signatories':[iclr2017workshopProgramChairs.id+'/4',tara.id]
};


var michael = {
  id: 'spector@cs.umass.edu',
  first:'Michael',
  last:'Spector'
};
var areaChair_1 = {
  'id': iclr2017workshopAreaChairs.id+'/1',
  'signatures':[iclr2017workshopAreaChairs.id],
  'writers':[iclr2017workshopAreaChairs.id],
  'readers':['everyone'],
  'members': [michael.id],
  'signatories': [iclr2017workshopAreaChairs.id+'/1', michael.id]
};

iclr2017workshopProgramChairs.members = [programChair_1.id, programChair_2.id, programChair_3.id, programChair_4.id];
iclr2017workshopAreaChairs.members = [areaChair_1.id];
iclr2017workshop.members = [].concat(iclr2017workshopProgramChairs.members, iclr2017workshopAreaChairs.members);

module.exports.iclr = iclr;
module.exports.iclr2017 = iclr2017;
module.exports.iclr2017workshop = iclr2017workshop
module.exports.iclr2017workshopAreaChairs = iclr2017workshopAreaChairs;
module.exports.iclr2017workshopProgramChairs = iclr2017workshopProgramChairs;
module.exports.hugo = hugo;
module.exports.programChair_1 = programChair_1;
module.exports.oriol = oriol;
module.exports.programChair_2 = programChair_2;
module.exports.marcAurelio = marcAurelio;
module.exports.programChair_3 = programChair_3;
module.exports.tara = tara;
module.exports.programChair_4 = programChair_4;
module.exports.michael = michael;
module.exports.areaChair_1 = areaChair_1;

