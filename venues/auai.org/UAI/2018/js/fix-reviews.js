var ids_to_fix = [
'HJSDO-8iM',
'H1ibhvBsM',
'SJQjmBrif',
'SyOczBrsf',
'rkVKtGSjf',
'r10rnWriG',
'rJ746yrjG',
'B1sHmsEsz',
'SJNWlONsz',
'SJhWlWEjf',
'H1n1FxVsz',
'rkEs_eEif',
'B1FVul4sz',
'HkAkOeNjM',
'ByOYPlEiG',
'HJVC11VoM',
'Hy9GwpXsM',
'H1WwmDQsz',
'SkuM_xmsz',
'B1RFIqGiG',
'B1WJ2ZGsz',
'Hy_whnbsz',
'r1JLZvbjz',
'rkg4aZWif',
'SkRpFclsM',
'B1wncBgof',
'HycjnPhqM',
'BJTSLv39M',
'ByFDiE35M',
'SyKQi439G',
'ByvgjNn9M',
'BJA39V29z',
'BylL5V3cG',
'By2KfbnqG',
'Hyv9_Lo9M',
'S1PjQVicz'
];

for(i=0; i<ids_to_fix.length; i++){
	id_to_fix = ids_to_fix[i];
	note_to_fix = db.openreview_notes.byExample({'id': id_to_fix}).toArray()[0];
	ref_to_fix = db.openreview_references.byExample({'id': id_to_fix}).toArray()[0];
	invitation = db.openreview_invitations.byExample({'id': note_to_fix.invitation}).toArray()[0];
	unsubmitted_group_id = invitation.invitees[0] + '/Unsubmitted';
	db.openreview_notes.update(note_to_fix, {'nonreaders': [unsubmitted_group_id]});
	db.openreview_references.update(ref_to_fix, {'nonreaders': [unsubmitted_group_id]});
}
