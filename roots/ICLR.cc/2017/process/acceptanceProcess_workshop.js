function(){
  var or3client = lib.or3client;


  function getTemplate(forum, decision) {

  	if (decision == 'Accept') {

    	var template = `Dear Author,

We are pleased to inform you that your ICLR 2017 submission to the Workshop Track
${forum.number} - ${forum.content.title}
has been accepted to the Workshop Track as a poster presentation.

Please don't forget to make your travel arrangements. ICLR early registration will only be in effect until March 24th, 2017. Please register by visiting the conference website at: http://www.iclr.cc/doku.php?id=iclr2017:main . There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2017.

We received 127 Workshop Track submissions! Out of these we accepted 81 workshop submissions for poster presentation in the Workshop Track (63%).

Congratulations and thank you for your contribution.

We look forward to seeing you in Toulon, France!

Marc’Aurelio, Hugo, Tara and Oriol -- the ICLR 2017 program committee

    	`;


      return {
        "groups": forum.content.authorids,
        "subject": "ICLR 2017 workshop track: final decision - poster",
        "message": template
      };
  	}


  	if (decision == 'Reject') {
    	var template = `Dear Author,

We are writing to inform you that your ICLR 2017 Workshop Track submission
${forum.number} - ${forum.content.title}
was not accepted.

We received 127 Workshop Track submissions. Out of these we accepted only 81 workshop submissions for poster presentation in the Workshop Track.

Thank you for your interest in the conference, and we hope you'll nevertheless consider joining us in Toulon, France.

Marc’Aurelio, Hugo, Tara and Oriol -- the ICLR 2017 program committee

`;

      return {
        "groups": forum.content.authorids,
        "subject":"ICLR 2017 workshop track: final decision - rejection",
        "message": template
      };
  	}

  	return {};

  }

  var origNoteP = or3client.or3request(or3client.notesUrl + '?id=' + note.forum, {}, 'GET', token);
  origNoteP.then(result => {
  	var forum = result.notes[0];
    var decision = note.content.decision;
    var email = getTemplate(forum, decision);
    return or3client.or3request( or3client.mailUrl, email, 'POST', token );
  })
  .then(result => or3client.addInvitationNoninvitee(note.invitation, note.signatures[0],token))
  .then(result => done())
  .catch(error => {
  	console.log('error: ' + error);
  	done(error);
  });
  return true;
};
