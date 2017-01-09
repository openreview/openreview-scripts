var fs = require('fs');
var _ = require('underscore');


//migrate groups
var groupsQuery = `
	for n in openreview_groups
	filter like(n.id,'UAI.org%')
	return n
`

var uaigroups = db._query(groupsQuery).toArray();

db.openreview_groups.removeByExample({'id':'UAI.org/2017'});

_.each(uaigroups, function(g){
	var newId = g.id.replace('/conference','').replace('UAI.org','auai.org/UAI');
	console.log(g.id,'-->',newId);
	db.openreview_groups.updateByExample({'id':g.id},{'id':newId});
});

db.openreview_groups.updateByExample({'id':'auai.org/UAI'},
	{	'readers':['everyone'],
		'writers' : ['OpenReview.net'],
        'signatures' : ['OpenReview.net'],
        'signatories' : []
    });

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017'},
	{	'web':fs.readFileSync('../webfield/uai2017_webfield.html', 'utf8'),
        'readers':['everyone'],
        'writers':['auai.org/UAI/2017'],
        'signatures':['OpenReview.net'],
        'signatories':['auai.org/UAI/2017'],
        'members':[]
    });

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Program_Co-Chairs'},
	{	'readers':['everyone'],
		'writers':['OpenReview.net','auai.org/UAI/2017/Program_Co-Chairs'],
		'signatures':['OpenReview.net'],
		'signatories':['auai.org/UAI/2017/Program_Co-Chairs']
	});

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Senior_Program_Committee'},
	{
        'readers'     : ['everyone'],
        'writers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'signatures'  : ['auai.org/UAI/2017/Program_Co-Chairs'],
        'signatories' : ['auai.org/UAI/2017/Program_Co-Chairs']
	});

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Senior_Program_Committee/invited'},
    {   'readers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'writers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'signatures'  : ['auai.org/UAI/2017/Program_Co-Chairs'],
        'signatories' : []
    });

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Senior_Program_Committee/declined'},
	{
        'readers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'writers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'signatures'  : ['auai.org/UAI/2017/Program_Co-Chairs'],
        'signatories' : []
	});

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Senior_Program_Committee/emailed'},
	{
        'readers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'writers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'signatures'  : ['auai.org/UAI/2017/Program_Co-Chairs'],
        'signatories' : []
	});

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Program_Committee'},
	{
        'readers'     : ['everyone'],
        'writers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'signatures'  : ['auai.org/UAI/2017/Program_Co-Chairs'],
        'signatories' : []
	});

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Program_Committee/invited'},
	{
        'readers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'writers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'signatures'  : ['auai.org/UAI/2017/Program_Co-Chairs'],
        'signatories' : []
	});

db.openreview_groups.updateByExample({'id':'auai.org/UAI/2017/Program_Committee/declined'},
	{
        'readers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'writers'     : ['auai.org/UAI/2017/Program_Co-Chairs','auai.org/UAI/2017'],
        'signatures'  : ['auai.org/UAI/2017/Program_Co-Chairs'],
        'signatories' : []
	});


//migrate invitations
var invitationsQuery = `
	for n in openreview_invitations
	filter like(n.id,'UAI.org%')
	return n
`

var uaiinvitations = db._query(invitationsQuery).toArray();
//UAI.org/2017/conference/-/spc_registration
//UAI.org/2017/conference/-/SPC_Expertise
//UAI.org/2017/conference/-/submission
//UAI.org/2017/conference/-/spc_invitation

_.each(uaiinvitations, function(i){
	var newId = i.id.replace('/conference','').replace('UAI.org','auai.org/UAI');
	console.log(i.id,'-->',newId);
	db.openreview_invitations.updateByExample({'id':i.id},{'id':newId});
});


//migrate notes
var notesQuery = `
	for n in openreview_notes
	filter like(n.invitation,'UAI.org%')
	return n
`

var uainotes = db._query(notesQuery).toArray();
_.each(uainotes, function(n){
	var newInv = n.invitation.replace('/conference','').replace('UAI.org','auai.org/UAI');
	console.log('note ', n.id,'invitation updated');
	db.openreview_notes.updateByExample({'id':n.id},{
		'invitation':newInv,
		'writers':"UAI.org/2017/conference"
	});
});

