// Run this script when the UAI paper metadata needs to be reset

var notes = db._query("FOR note IN openreview_notes FILTER CONTAINS(note.invitation, 'auai.org/UAI/2017/-/Paper/Metadata') RETURN note._id").toArray()
for(i=0;i<notes.length;i++){
	db.openreview_notes.remove(notes[i])
}

var refs = db._query("FOR note IN openreview_references FILTER CONTAINS(note.invitation, 'auai.org/UAI/2017/-/Paper/Metadata') RETURN note._id").toArray()
for(i=0;i<refs.length;i++){
	db.openreview_references.remove(refs[i])
}

var notes = db._query("FOR note IN openreview_notes FILTER CONTAINS(note.invitation, 'auai.org/UAI/2017/-/Reviewer/Metadata') RETURN note._id").toArray()
for(i=0;i<notes.length;i++){
	db.openreview_notes.remove(notes[i])
}

var refs = db._query("FOR note IN openreview_references FILTER CONTAINS(note.invitation, 'auai.org/UAI/2017/-/Reviewer/Metadata') RETURN note._id").toArray()
for(i=0;i<refs.length;i++){
	db.openreview_references.remove(refs[i])
}

var notes = db._query("FOR note IN openreview_notes FILTER CONTAINS(note.invitation, 'auai.org/UAI/2017/-/Area_Chair/Metadata') RETURN note._id").toArray()
for(i=0;i<notes.length;i++){
	db.openreview_notes.remove(notes[i])
}

var refs = db._query("FOR note IN openreview_references FILTER CONTAINS(note.invitation, 'auai.org/UAI/2017/-/Area_Chair/Metadata') RETURN note._id").toArray()
for(i=0;i<refs.length;i++){
	db.openreview_references.remove(refs[i])
}
