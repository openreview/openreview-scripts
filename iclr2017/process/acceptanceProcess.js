function(){
  var or3client = lib.or3client;


  function getTemplate(forum, decision) {

  	if (decision == 'Accept (Oral)') {

    	var template = `Dear Author,

We are very pleased to inform you that your ICLR 2017 submission to the Conference Track
${forum.number} - ${forum.content.title}
has been accepted to the Conference Track as an oral presentation.

Note that your paper will also have to be presented at one of our poster sessions, we will provide details about poster sessions and poster formats soon.

You should now prepare the camera ready version of your contribution, which should include inserting the statement \\iclrfinalcopy in your LaTeX source file.

We ask that you update your paper on OpenReview with this latest version no later than February 24th, 2017.

https://openreview.net/forum?id=${forum.id}

Please don't forget to make your travel arrangements. ICLR early registration will only be in effect until March 24th, 2017. It will soon be possible to register by visiting the conference website at: http://www.iclr.cc/doku.php?id=iclr2017:main . Please, check in a few days. There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2017.

We received 507 Conference Track submissions -- up from 265 last year! Out of these we accepted only 15 conference submissions for oral presentation (3%) and 181 conference submissions for poster presentation in the Conference Track (36%).

Congratulations and thank you for your contribution.

We look forward to seeing you in Toulon, France!

Marc’Aurelio, Hugo, Tara and Oriol -- the ICLR 2017 program committee
    	`;


      return {
        "groups": forum.content.authorids,
        "subject": "ICLR 2017 conference track: final decision - oral",
        "message": template
      };
  	}

  	if (decision == 'Accept (Poster)') {
    	var template = `Dear Author,

We are pleased to inform you that your ICLR 2017 submission to the Conference Track
${forum.number} - ${forum.content.title}
has been accepted to the Conference Track as a poster presentation.

You should now prepare the camera ready version of your contribution, which should include inserting the statement \\iclrfinalcopy in your LaTeX source file.

We ask that you update your paper on OpenReview with this latest version no later than February 24th, 2017.

https://openreview.net/forum?id=${forum.id}

Please don't forget to make your travel arrangements. ICLR early registration will only be in effect until March 24th, 2017. It will soon be possible to register by visiting the conference website at: http://www.iclr.cc/doku.php?id=iclr2017:main . Please, check in a few days. There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2017.

We received 507 Conference Track submissions -- up from 265 last year! Out of these we accepted only 15 conference submissions for oral presentation (3%) and 181 conference submissions for poster presentation in the Conference Track (36%).

Congratulations and thank you for your contribution.

We look forward to seeing you in Toulon, France!

Marc’Aurelio, Hugo, Tara and Oriol -- the ICLR 2017 program committee
    	`;

      return {
        "groups": forum.content.authorids,
        "subject":"ICLR 2017 conference track: final decision - poster",
        "message": template
      };
  	}

  	if (decision == 'Invite to Workshop Track') {
    	var template = `Dear Author,

We are writing to inform you that your ICLR 2017 submission to the Conference Track
${forum.number} - ${forum.content.title}
was not accepted to the Conference Track. However, we'd be happy to have you present this work as a poster in the ICLR 2017 Workshop Track.

If you do not wish to present in the ICLR 2017 Workshop Track, you have nothing to do (converting to a workshop contribution is "opt-in").

But if you do (as we hope!), you should prepare a camera ready version of your contribution that uses the style file for Workshop Track papers, available here: http://www.iclr.cc/lib/exe/fetch.php?media=iclr2017:iclr2017_stylefiles_workshop.zip.
Simply, update the file style file (the top of the first page should state that your paper is a workshop contribution). There is no need to further reformat your paper; in particular, you do not need to (unless you want to) satisfy the 3 page length requirement. Your paper will not go under further review and it will be automatically accepted at the Workshop Track.

We will be accepting Workshop Track contributions until February 17th, 2017, 5PM EST. Papers can be submitted via OpenReview at:
https://openreview.net/group?id=ICLR.cc/2017/workshop

Please don't forget to make your travel arrangements. ICLR early registration will only be in effect until March 24th, 2017. It will soon be possible to register by visiting the conference website at: http://www.iclr.cc/doku.php?id=iclr2017:main . Please, check in a few days. There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2017.

We received 507 Conference Track submissions -- up from 265 last year! Out of these we accepted only 15 conference submissions for oral presentation (3%) and 181 conference submissions for poster presentation in the Conference Track (36%).

Congratulations and thank you for your contribution.

We look forward to seeing you in Toulon, France!

Marc’Aurelio, Hugo, Tara and Oriol -- the ICLR 2017 program committee
    	`;

      return {
        "groups": forum.content.authorids,
        "subject":"ICLR 2017 conference track: final decision - invite to Workshop Track",
        "message": template
      };
  	}

  	if (decision == 'Reject') {
    	var template = `Dear Author,

We are writing to inform you that your ICLR 2017 submission
${forum.number} - ${forum.content.title}
was not accepted.

We received 507 Conference Track submissions -- up from 265 last year. Out of these we accepted only 15 conference submissions for oral presentation (3%) and 181 conference submissions for poster presentation in the Conference Track (36%).

Thank you for your interest in the conference, and we hope you'll nevertheless consider joining us in Toulon, France.

Marc’Aurelio, Hugo, Tara and Oriol -- the ICLR 2017 program committee
`;

      return {
        "groups": forum.content.authorids,
        "subject":"ICLR 2017 conference track: final decision - rejection",
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
