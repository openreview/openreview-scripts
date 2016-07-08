var fs = require('fs');

var headers = { 'User-Agent': 'test-create-script' }; //what are these?

var rootUser = {
  id:'OpenReview.net',
  password:'12345678'
}

// ECCV ROOT GROUP
var eccv = { //scrap this
  'id': 'ECCV2016.org',
  'signatures': [rootUser.id],
  'writers': ['ECCV2016.org', rootUser.id],
  'members': [rootUser.id],
  'readers': ['everyone'],
  'signatories': ['ECCV2016.org']
};

// GROUPS TO CREATE
var workshop = {
  'id': eccv.id+'/BNMW',
  'signatures': [rootUser.id],
  'writers': [eccv.id],
  'readers': ['everyone'],
  'members': [/*program chairs*/],
  'signatories': [eccv.id,eccv.id+'/BNMW'],
  'web': fs.readFileSync('bnmw_webfield.html', "utf8")
};

var paper = {
  'id': workshop.id+'/paper',
  'signatures': [rootUser.id],
  'writers': [workshop.id],
  'readers': ['everyone'],
  'members': [workshop.id],
  'signatories': [workshop.id,workshop.id+'/paper'],
};

var noteBody = {
  'content': {
    'CMT_id':'',
    'abstract':'We aim to detect all instances of a category in an image and, for each instance, mark the pixels that belong to it. We call this task Simultaneous Detection and Segmentation (SDS). Unlike classical bounding box detection, SDS requires a segmentation and not just a box. Unlike classical semantic segmentation, we require individual object instances. We build on recent work that uses convolutional neural networks to classify category-independent region proposals (R-CNN [16]), introducing a novel architecture tailored for SDS. We then use category-specific, top- down figure-ground predictions to refine our bottom-up proposals. We show a 7 point boost (16% relative) over our baselines on SDS, a 5 point boost (10% relative) over state-of-the-art on semantic segmentation, and state-of-the-art performance in object detection. Finally, we provide diagnostic tools that unpack performance and provide directions for future work.',
    'author_emails':"author@gmail.com",
    'authors':'Bharath Hariharan, Pablo Arbeláez, Ross Girshick, Jitendra Malik',
    'conflicts':'cs.berkeley.edu',
    'pdf':'http://arxiv.org/pdf/1407.1808v1.pdf',
    'title':'Simultaneous Detection and Segmentation2'
  },
  'forum': null,
  'invitation': workshop.id+'/-/submission',
  'parent': null,
  'pdfTransfer':"url",
  'readers':["everyone"],
  'signatures':["~super_user1"],
  'writers':["~super_user1"],
};

//DEMO HACK
var email1 = 'michael.l.spector@gmail.com';
var email2 = 'efstratios.gavves@gmail.com';

var reviewer_account1 = {
  'id': email1,
  'needsPassword': true
}

var reviewer_account2 = {
  'id': email2,
  'needsPassword': true
}

var wrapper_group1 = {
  'id': 'reviewer-1',
  'signatures': [rootUser.id],
  'writers': [email1],
  'readers': ['everyone'], //if this is an anonymizing wrapper group, it probably shouldn't have "everyone" as readers
  'members': [email1],
  'signatories': [email1]
};

var wrapper_group2 = {
  'id': 'reviewer-2',
  'signatures': [rootUser.id],
  'writers': [email2],
  'readers': ['everyone'], //if this is an anonymizing wrapper group, it probably shouldn't have "everyone" as readers
  'members': [email2],
  'signatories': [email2]
};

module.exports = {
  'headers':headers,
  'rootUser':rootUser,
  'eccv':eccv,
  'workshop':workshop,
  'paper':paper,
  'noteBody':noteBody,
  'email1':email1,
  'email2':email2,
  'reviewer_account1':reviewer_account1,
  'reviewer_account2':reviewer_account2,
  'wrapper_group1':wrapper_group1,
  'wrapper_group2':wrapper_group2
};


//emails
var jan = {
  'id': 'j.c.vangemert@tudelft.nl',
  'needsPassword': true
};

var basura = {
  'id': 'basura.fernando@anu.edu.au',
  'needsPassword': true
};

var stratis = {
  'id': 'efstratios.gavves@gmail.com',
  'needsPassword':true
}

var michael = {
  'id': 'michael.l.spector@gmail.com',
  'needsPassword': true
};

var program_chairs = {
  'id': '~ECCV_Program_Chairs',
  'signatures': [rootUser.id],
  'writers': [jan.id, basura.id, stratis.id, michael.id],
  'readers': ['everyone'], //if this is an anonymizing wrapper group, it probably shouldn't have "everyone" as readers
  'members': [jan.id, basura.id, stratis.id, michael.id],
  'signatories': [jan.id, basura.id, stratis.id, michael.id]
};