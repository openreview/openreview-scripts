function() {

	var or3client = lib.or3client;

	var overwritingNote = {
		original: note.id,
    invitation: 'UAI.org/2017/conference/-/blind-submission',
    forum: null,
    parent: null,
    signatures: ['UAI.org/2017/conference'],
    writers: ['UAI.org/2017/conference'],
    readers: ["UAI.org/2017/conference/Program_Co-Chairs", "UAI.org/2017/conference/Senior_Program_Committee", "UAI.org/2017/conference/Program_Committee"],
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
