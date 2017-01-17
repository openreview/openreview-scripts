function() {

    var or3client = lib.or3client;
    var uaiGroup = 'auai.org/UAI/2017';
    var coChairsGroup = 'auai.org/UAI/2017/Program_Co-Chairs';
    var spcGroup = 'auai.org/UAI/2017/Senior_Program_Committee';
    var pcGroup = 'auai.org/UAI/2017/Program_Committee';

    var overwritingNote = {
        original: note.id,
        invitation: 'auai.org/UAI/2017/-/blind-submission',
        forum: null,
        parent: null,
        signatures: [uaiGroup],
        writers: [uaiGroup],
        readers: [coChairsGroup, spcGroup, pcGroup],
        content: {
            authors: [],
            authorids: []
        }
    }

    //Send an email to the author of the submitted note, confirming its receipt
    var mail = {
        "groups": note.content.authorids,
        "subject": "Confirmation of your submission to UAI 2017: \"" + note.content.title + "\".",
        "message": `Your submission to UAI 2017 has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
    };


    or3client.or3request(or3client.notesUrl, overwritingNote, 'POST', token)
    .then(savedNote => {
      var groupId = uaiGroup + '/Paper' + savedNote.number + '/Authors';
      var authorGroup = {
        id: groupId,
        signatures: [uaiGroup],
        writers: [uaiGroup],
        members: note.content.authorids,
        readers: [coChairsGroup, groupId],
        signatories: [groupId]
      };
      console.log(authorGroup);
      return or3client.or3request(or3client.grpUrl, authorGroup, 'POST', token)
      .then(savedGroup => {
        savedNote.content.authorids = [savedGroup.id];
        savedNote.content.authors = ['Blinded names'];
        savedNote.readers.push(savedGroup.id);
        return or3client.or3request(or3client.notesUrl, savedNote, 'POST', token);
      });
    })
    .then(result => or3client.or3request(or3client.mailUrl, mail, 'POST', token))
    .then(result => done())
    .catch(error => done(error));

    return true;
}
