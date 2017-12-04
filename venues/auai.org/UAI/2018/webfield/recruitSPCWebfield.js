var httpGetP = function(url, queryOrBody) {
  var df = $.Deferred();
  httpGet(url, queryOrBody, function(result) {
    df.resolve(result);
  }, function(err) {
    df.reject(result);
  });
  return df.promise();
};

$attach('#header', 'mkHostHeader', [
  "UAI 2018 Conference",
  "Uncertainty in Artificial Intelligence",
  "San Francisco, USA, August 2018",
  "http://auai.org"
], true);

var $header = $('#header');

if (args && args.noteId) {


  httpGetP('notes', { id: args.noteId }).then(function(result) {
    accepted = (result.notes[0].content.response == 'Yes')
    var message = accepted ? `Thank you for accepting the invitation!` : 'You have declined the invitation.';
    var $response = $('#response');
    $response.append(
      $('<div>', {class: 'panel'})
      .append($('<div>', {class: 'row'}).text(message))
    );

    if(accepted){
      $response.append(
        $('<div>',{class:'panel'}).append(
          $('<div>',{class:'row'}).append(
            $('<span>').text("If you do not already have an OpenReview account, please sign up "),
            $('<a>',{
              href: '/signup',
              text: 'here'
            }),
            $('<span>').text(".")
          ),
          $('<div>',{class:'row'}).append(
            $('<span>').text("If you have an existing OpenReview account, please ensure that the email address that received this invitation is linked to your "),
            $('<a>',{
              href:'/profile?mode=edit',
              text:'profile page'
            }),
            $('<span>').text(" and has been confirmed.")
          )
        )
      )
    }

  });
}

