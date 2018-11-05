// Constants
var CONFERENCE_ID = 'AKBC.ws/2013';
var INVITATION_ID = CONFERENCE_ID + '/-/submission'
var HEADER = {
    title: 'Automated Knowledge Base Construction 2013',
    subtitle: 'The 3rd Workshop on Knowledge Extraction at CIKM 2013',
    date: 'Oct 27 - 28, 2013, San Francisco, CA, USA',
    website: 'http://www.akbc.ws'
}

// Display Homepage
Webfield.ui.setup('#group-container', CONFERENCE_ID);

Webfield.ui.venueHeader(HEADER);

Webfield.ui.spinner('#notes', { inline: true });

Webfield.get('/notes', { invitation: INVITATION_ID })
    .then(function (result) {
        return result.notes;
    }, function (error) {
        return error;
    })
    .then(function (notes) {
        if (notes) {
            var $panel = $('#notes');
            $panel.empty();

            var notesDict = {};

            var oralDecisions = [];
            var posterDecisions = [];
            var rejectDecisions = [];

            _.forEach(notes, function (n) {
                notesDict[n.id] = n;

                if (n.content.decision == 'conferenceOral') {
                    oralDecisions.push(n);
                } else if (n.content.decision == 'conferencePoster') {
                    posterDecisions.push(n);
                } else if (n.content.decision == 'reject') {
                    rejectDecisions.push(n);
                }
            });

            displayNotes(notesDict, oralDecisions, $panel, 'Accepted for Oral Presentation', '');
            $panel.append($('<div>', {style: 'height: 50px;'}));

            displayNotes(notesDict, posterDecisions, $panel, 'Accepted for Poster Presentation', '');
            $panel.append($('<div>', {style: 'height: 50px;'}));

            displayNotes(notesDict, rejectDecisions, $panel, 'Not selected for presentation at this time', '');
        }
    });

function displayNotes(notes, decisions, $panel, text, summary) {
    $panel.append($('<div>', {class: 'panel'}).append($('<h2>', {style: 'text-decoration: underline;'}).text(text)));

    _.forEach(decisions, function (decision) {
        var forum = notes[decision.forum];
        if (forum) {
            $('#notes').append(view.mkNotePanel(forum, {
                titleLink: 'HREF',
                withReplyCount: true,
                withSummary: summary
            }));
        } else {
            console.log('Forum not found', decision.forum);
        }
    });
}
