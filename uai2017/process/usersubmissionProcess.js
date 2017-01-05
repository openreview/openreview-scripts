function() {

	var or3client = lib.or3client;

	var overwritingNote = {
		original: note.id,
    invitation: 'auai.org/UAI/2017/-/blind-submission',
    forum: null,
    parent: null,
    signatures: ['auai.org/UAI/2017'],
    writers: ['auai.org/UAI/2017'],
    readers: ["auai.org/UAI/2017/Chairs", "auai.org/UAI/2017/SPC", "auai.org/UAI/2017/PC"],
    content: {
 			authors: [],
 			authorids: []
    }
	}

	or3client.or3request(or3client.notesUrl, overwritingNote, 'POST', token)
	.then(result => done())
	.catch(error => done(error));

	return true;
}
