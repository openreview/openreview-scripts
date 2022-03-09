def process(client, note, invitation):

    if ('2 - possible accept to main conference' in note.content['suggested_decision'] or '3 - possible accept to findings' in note.content['suggested_decision']) and 'ranking' not in note.content:
        raise openreview.OpenReviewException('Please select a ranking for this paper.')