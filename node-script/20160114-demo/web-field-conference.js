function(view, placeholder, getData, user){

  function buildHeader(placeholder) {
    placeholder.append($('<div>', { 
      class: 'panel'
    })
    .append(
      $('<h1>').text("ICLR 2016 - Conference Track"),
      $('<h2>').text("International Conference on Learning Representations"),
      $('<h3>').text("May 2 - 4, 2016, Caribe Hilton, San Juan, Puerto Rico"),
      $('<div>', {
        class: 'row'
      })
      .append(
        $('<span>').text('Please see the venue website ('),
        $('<a>', {
          href: 'http://www.iclr.cc/doku.php?id=iclr2016:main', 
          text: 'http://www.iclr.cc/doku.php?id=iclr2016:main'
        }),
        $('<span>').text(') for more information.')
      ),
      $('<div>', {class: 'row'}).text('Submission deadline: 18 Feb 2016')
    ));
  }

  function buildInvitations(view, placeholder, user) {
    console.log('buildInvitations');

    getData('invitations', {
      replyForum: null, 
      signature: 'ICLR.cc/2016/conference'
    })
    .then(function(result) {

      //shouldn't get only active invitations?
      var filteredInvitations = _.filter(result.invitations, function(invitation) {
        return (invitation.duedate > Date.now());
      })

      placeholder.append(view.mkInvitationRows(filteredInvitations, user));

    });

  }

  function buildNotes(view, placeHolder, user) {

    getData('notes', {
      invitation: 'ICLR.cc/2016/conference/-/submission', 
      maxtcdate: Date.now()
    })
    .then(function(result) {
      console.log("buildNotes result", result);
      placeHolder.append(_.map(result.notes, function(note) {
        console.log("makeNotePanel", note, user);
        return view.mkNotePanel(note, user, null, null, true, true);
      })); 
    });
  }

  buildHeader(placeholder);
  buildInvitations(view, placeholder, user);
  buildNotes(view, placeholder, user);
}