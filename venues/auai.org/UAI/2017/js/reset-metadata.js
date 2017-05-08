var notes = db._query("FOR note IN openreview_notes FILTER CONTAINS(note.invitation, 'auai.org/UAI/2017/-/Paper/Metadata') RETURN note._id").toArray()
for(i=0;i<notes.length;i++){
	db.openreview_notes.remove(notes[i])
}
