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
"ICML / Peer Review 2013",
"ICML 2013 Workshop on Peer Reviewing and Publishing Models",
"Jun 20, 2013, Atlanta, Georgia, USA",
"http://sites.google.com/site/workshoponpeerreviewing"
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

var notesP = httpGetP('notes', {invitation: 'ICML.cc/2013/PeerReview/-/submission'}).then(function(result) {
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

        var oralDecisions = [];
        var posterDecisions = [];
        var rejectDecisions = [];

        _.forEach(notes, function (n) {
            notesDict[n.id] = n;

            if (n.content.decision == 'oral') {
                oralDecisions.push(n);
//                    } else if (n.content.decision == 'conferencePoster') {
//                        posterDecisions.push(n);
            } else if (n.content.decision == 'reject') {
                rejectDecisions.push(n);
            }
        });

        displayNotes(notesDict, oralDecisions, $panel, 'Accepted for Oral Presentation', '');
        $panel.append($('<div>', {style: 'height: 50px;'}));
//                displayNotes(notesDict, posterDecisions, $panel, 'Accepted for Poster Presentation', '');
//                $panel.append($('<div>', {style: 'height: 50px;'}));
        displayNotes(notesDict, rejectDecisions, $panel, 'Submitted Papers', '');

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

