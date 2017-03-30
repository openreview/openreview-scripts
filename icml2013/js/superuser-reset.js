// var counter = db.openreview_counters.byExample({'id':'ICML.cc/2013/Inferning/-/submission'}).toArray()[0]
// db.openreview_counters.remove(counter._id)

//also reset the counters for all the other invitations, not just submission

var notes = db._query("FOR note IN openreview_notes FILTER CONTAINS(note.invitation, 'ICML.cc/2013/Inferning') RETURN note._id").toArray()
for(i=0;i<notes.length;i++){
	db.openreview_notes.remove(notes[i])
}

var notes = db._query("FOR note IN openreview_notes FILTER CONTAINS(note.invitation, 'ICML.cc/2013/PeerReview') RETURN note._id").toArray()
for(i=0;i<notes.length;i++){
	db.openreview_notes.remove(notes[i])
}

var groups = db._query("FOR group IN openreview_groups FILTER CONTAINS(group.id, 'ICML.cc/2013/Inferning') RETURN group._id").toArray()
for(i=0;i<groups.length;i++){
	db.openreview_groups.remove(groups[i])
}
var groups = db._query("FOR group IN openreview_groups FILTER CONTAINS(group.id, 'ICML.cc/2013/PeerReview') RETURN group._id").toArray()
for(i=0;i<groups.length;i++){
	db.openreview_groups.remove(groups[i])
}

var invitations = db._query("FOR invitation IN openreview_invitations FILTER CONTAINS(invitation.id, 'ICML.cc/2013/Inferning') RETURN invitation._id").toArray()
for(i=0;i<invitations.length;i++){
	db.openreview_invitations.remove(invitations[i])
}

var invitations = db._query("FOR invitation IN openreview_invitations FILTER CONTAINS(invitation.id, 'ICML.cc/2013/PeerReview') RETURN invitation._id").toArray()
for(i=0;i<invitations.length;i++){
	db.openreview_invitations.remove(invitations[i])
}