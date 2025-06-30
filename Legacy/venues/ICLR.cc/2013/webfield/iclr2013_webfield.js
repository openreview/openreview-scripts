function httpGet(url, queryOrBody, success, failure) {
  controller.get(url, queryOrBody, success, failure);
}

function $attach(loc, viewFnName, viewFnArgs, append) {
  var $container = $(loc);
  var $el = view[viewFnName].apply(view, viewFnArgs);
  if (append) {
    $container.append($el);
  } else {
    $container.prepend($el);
  }
}

var $containter = $('#group-container');
$containter.append([
  $('<div id = "header">'),
  $('<div id = "invitation">'),
  $('<div id = "notes">')
]);


$attach('#header', 'mkHostHeader', [
"ICLR 2013",
"International Conference on Learning Representations",
"May 02 - 04, 2013, Scottsdale, Arizona, USA",
"https://sites.google.com/site/representationlearning2013/"
], true);

var sm = mkStateManager();

var httpGetP = function (url, queryOrBody) {
    var df = $.Deferred();
    httpGet(url, queryOrBody,
        function (result) {
            df.resolve(result);
        },
        function (result) {
            df.reject(result);
        });
    return df.promise();
};

var notesP = httpGetP('notes', {invitation: 'ICLR.cc/2013/conference/-/submission'}).then(function(result) {
        return result.notes;
    },
    function (error) {
        return error
    });

$.when(notesP).done(function (notes) {

    if (notes) {
        var $panel = $('#notes');
        $panel.empty();

        var notesDict = {};

        var workshopOralDecisions = [];
        var workshopPosterDecisions = [];

        var conferenceOralDecisions = [];
        var conferencePosterDecisions = [];
        var rejectDecisions = [];

        _.forEach(notes, function (n) {
            notesDict[n.id] = n;

            if (n.content.decision == 'conferenceOral-iclr2013-conference') {
                conferenceOralDecisions.push(n);
            } else if (n.content.decision == 'conferencePoster-iclr2013-conference') {
                conferencePosterDecisions.push(n);
            } else if (n.content.decision == 'conferenceOral-iclr2013-workshop') {
                workshopOralDecisions.push(n);
            } else if (n.content.decision == 'conferencePoster-iclr2013-workshop') {
                workshopPosterDecisions.push(n);
            } else if (n.content.decision == 'reject') {
                rejectDecisions.push(n);
            }
        });

        $panel.append($('<div>').append($('<h1>').text('ICLR 2013 Conference Track')));
        displayNotes(notesDict, conferenceOralDecisions, $panel, 'Accepted for Oral Presentation', '');
        $panel.append($('<div>', {style: 'height: 50px;'}));
        displayNotes(notesDict, conferencePosterDecisions, $panel, 'Accepted for Poster Presentation', '');
        $panel.append($('<div>', {style: 'height: 50px;'}));

        $panel.append($('<div>').append($('<h1>').text('ICLR 2013 Workshop Track')));
        displayNotes(notesDict, workshopOralDecisions, $panel, 'Accepted for Oral Presentation', '');
        $panel.append($('<div>', {style: 'height: 50px;'}));
        displayNotes(notesDict, workshopPosterDecisions, $panel, 'Accepted for Poster Presentation', '');
        $panel.append($('<div>', {style: 'height: 50px;'}));
        displayNotes(notesDict, rejectDecisions, $panel, 'Not selected for presentation at this time', '');

    }

});

function displayNotes(notes, decisions, $panel, text, summary) {
    $panel.append($('<div>', {class: 'panel'}).append($('<h2>', {style: 'text-decoration: underline; '}).text(text)));

    _.forEach(decisions, function (decision) {

        var forum = notes[decision.forum];
        if (forum) {
            $attach('#notes', 'mkNotePanel', [forum, {
                titleLink: 'HREF',
                withReplyCount: true,
                withSummary: summary
            }], true);
        } else {
            console.log('Forum not found', decision.forum);
        }

    });

}
