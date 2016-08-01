var fs = require('fs');
var _ = require('lodash');

var headers = { 'User-Agent': 'test-create-script' }; //what are these?
var rootUser = {
  id:'OpenReview.net',
  password:''
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
  'writers': ['ICLR.cc',rootUser.id],
  'members': [rootUser.id],
  'readers': ['everyone'],
  'signatories': ['ICLR.cc']
};

var iclr2017 = {
  'id': iclr.id+'/2017',
  'signatures': [iclr.id],
  'writers': [iclr.id],
  'readers': ['everyone'],
  'members': [],
  'signatories': [iclr.id, iclr.id+'/2017']
};

var iclr2017conference = {
  'id': iclr2017.id+'/conference',
  'signatures': [iclr2017.id],
  'writers': [iclr2017.id],
  'readers': ['everyone'],
  'members': [], //members of the conference group are set below
  'signatories': [iclr2017.id, iclr2017.id+'/conference'],
  'web': fs.readFileSync('../webfield/iclr2017_webfield.html', "utf8")
};

var iclr2017conferenceAreaChairs = {
  'id': iclr2017conference.id+'/areachairs',
  'signatures':[iclr2017conference.id],
  'writers':[iclr2017conference.id],
  'readers':['everyone'],
  'members':[], //members of the area chairs group are set below
  'signatories':[iclr2017conference.id+'/areachairs']
}

var iclr2017conferenceProgramChairs = {
  'id': iclr2017conference.id+'/programchairs',
  'signatures': [iclr2017conference.id],
  'writers': [iclr2017conference.id],
  'readers': ['everyone'],
  'members': [], //members of program chairs group are set below
  'signatories':[iclr2017conference.id+'/programchairs']
};



var hugo = {
  'id': 'hugo@openreview.net',
  'first':'Hugo',
  'last':'LaRochelle'
};
var programChair1 = {
  'id': iclr2017conferenceProgramChairs.id+'/1',
  'signatures':[iclr2017conferenceProgramChairs.id],
  'writers':[iclr2017conferenceProgramChairs.id],
  'readers':['everyone'],
  'members': [hugo.id],
  'signatories': [iclr2017conferenceProgramChairs.id+'/1', hugo.id]
};
iclr2017conferenceProgramChairs.members = [programChair1.id];



var oriol = {
  'id': 'oriol@openreview.net',
  'first': 'Oriol',
  'last': 'Vinyals'
}
var areaChair1 = {
  'id': iclr2017conferenceAreaChairs.id+'/1',
  'signatures':[iclr2017conferenceAreaChairs.id],
  'writers':[iclr2017conferenceAreaChairs.id],
  'readers':['everyone'],
  'members': [oriol.id],
  'signatories': [iclr2017conferenceAreaChairs.id+'/1', oriol.id]
};

var areaChair1reviewers = {
  'id': areaChair1.id+'/reviewers',
  'signatures': [areaChair1.id],
  'writers': [areaChair1.id],
  'readers': ['everyone'],
  'members': [], //added below
  'signatories':[areaChair1.id+'/reviewers']
};

var michael = {
  'id': 'spector@cs.umass.edu',
  'first':'Michael',
  'last':'Spector'
};
var reviewer1 = {
  'id': 'reviewer-1',
  'signatures': [areaChair1.id],
  'writers': [areaChair1.id],
  'readers': [areaChair1.id, programChair1.id],
  'members': [michael.id],
  'signatories':[michael.id]
}

var melisa = {
  'id':'melisabok@gmail.com',
  'first':'Melisa',
  'last':'Bok'
};
var reviewer2 = {
  'id': 'reviewer-2',
  'signatures': [areaChair1.id],
  'writers': [areaChair1.id],
  'readers': [areaChair1.id, programChair1.id],
  'members': [melisa.id],
  'signatories':[melisa.id]
}
areaChair1reviewers.members = [reviewer1.id, reviewer2.id]


var tara = {
  'id': 'tara@openreview.net',
  'first': 'Tara',
  'last': 'Sainath'
}
var areaChair2 = {
  'id': iclr2017conferenceAreaChairs.id+'/2',
  'signatures':[iclr2017conferenceAreaChairs.id],
  'writers':[iclr2017conferenceAreaChairs.id],
  'readers':['everyone'],
  'members': [tara.id],
  'signatories': [iclr2017conferenceAreaChairs.id+'/2', tara.id]
};

iclr2017conferenceAreaChairs.members = [areaChair1.id, areaChair2.id];

var areaChair2reviewers = {
  'id': areaChair2.id+'/reviewers',
  'signatures': [areaChair2.id],
  'writers': [areaChair2.id],
  'readers': ['everyone'],
  'members': [], //added below
  'signatories':[areaChair2.id+'/reviewers']
};

var thomas = {
  'id': 'thomas@openreview.net',
  'first':'Thomas',
  'last':'Logan'
};
var reviewer3 = {
  'id': 'reviewer-3',
  'signatures': [areaChair2.id],
  'writers': [areaChair2.id],
  'readers': [areaChair2.id, programChair1.id],
  'members': [thomas.id],
  'signatories':[thomas.id]
}

var andrew = {
  'id':'andrew@openreview.net',
  'first':'Andrew',
  'last':'McCallum'
};
var reviewer4 = {
  'id': 'reviewer-4',
  'signatures': [areaChair2.id],
  'writers': [areaChair2.id],
  'readers': [areaChair2.id, programChair1.id],
  'members': [andrew.id],
  'signatories':[andrew.id]
}
areaChair2reviewers.members = [reviewer3.id, reviewer4.id]



iclr2017conference.members = [].concat(iclr2017conferenceProgramChairs.members, iclr2017conferenceAreaChairs.members);

var note1 = {
  'content': {
    'CMT_id':'',
    'abstract':'This is note 1',
    'author_emails':"author@gmail.com",
    'authors':'Author 1',
    'conflicts':'cs.berkeley.edu',
    'pdf':'http://arxiv.org/pdf/1407.1808v1.pdf',
    'title':'Note 1',
    'keywords':['keyword']
  },
  'forum': null,
  'invitation': iclr2017conference.id+'/-/submission',
  'parent': null,
  'pdfTransfer':"url",
  'readers':["everyone"],
  'signatures':["~super_user1"],
  'writers':["~super_user1"],
};


module.exports.iclr = iclr;
module.exports.iclr2017 = iclr2017;
module.exports.iclr2017conference = iclr2017conference
module.exports.iclr2017conferenceAreaChairs = iclr2017conferenceAreaChairs;
module.exports.iclr2017conferenceProgramChairs = iclr2017conferenceProgramChairs;
module.exports.hugo = hugo;
module.exports.programChair1 = programChair1;
module.exports.oriol = oriol;
module.exports.tara = tara;
module.exports.areaChair1 = areaChair1;
module.exports.areaChair1reviewers = areaChair1reviewers
module.exports.areaChair2 = areaChair2;
module.exports.areaChair2reviewers = areaChair2reviewers
module.exports.michael = michael;
module.exports.melisa = melisa;
module.exports.thomas = thomas;
module.exports.andrew = andrew;
module.exports.reviewer1 = reviewer1;
module.exports.reviewer2 = reviewer2;
module.exports.reviewer3 = reviewer3;
module.exports.reviewer4 = reviewer4;
module.exports.note1 = note1;
