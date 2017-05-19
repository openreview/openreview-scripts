function() {

    var or3client = lib.or3client;

    //Send an email to the author of the submitted note, confirming its receipt
    var mail = {
        "groups": note.content.authorids,
        "subject": "Confirmation of your submission to ICML 2017 MLAV Workshop: \"" + note.content.title + "\".",
        "message": `Your submission to ICML 2017 Machine Learning for Autonomous Vehicles has been posted.\n\nTitle: `+note.content.title+`\n\nAbstract: `+note.content.abstract+`\n\nTo view the note, click here: `+baseUrl+`/forum?id=` + note.forum
    };

    or3client.or3request(or3client.mailUrl, mail, 'POST', token)
    .then(result => done())
    .catch(error => done(error));

    return true;
}
