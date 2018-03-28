import os

CONF = 'auai.org/UAI/2018'

official_comment_template = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/commentProcess.js'),
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {},
        'signatures': {},
        'writers': {},
        'content':{
            'title': {
                'order': 0,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your comment.',
                'required': True
            },
            'comment': {
                'order': 1,
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Your comment or reply (max 5000 characters).',
                'required': True
            }
        }
    }
}

official_review_template = {
    'readers': ['everyone'],
    'writers': ['auai.org/UAI/2018'],
    'invitees': [],
    'signatures': ['auai.org/UAI/2018'],
    'process': os.path.join(os.path.dirname(__file__), '../process/officialReviewProcess.js'),
    'duedate': 1524355199000, # Saturday, April 21, 2018 11:59:59 PM
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {},
        'signatures': {},
        'writers': {},
        'content':{
            'title': {
                'order': 1,
                'value-regex': '.{0,500}',
                'description': 'Brief summary of your review.',
                'required': True
            },
            'review': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,200000}',
                'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (max 200000 characters).',
                'required': True
            },
            'rating': {
                'order': 3,
                'value-dropdown': [
                    '10: Top 5% of accepted papers, seminal paper',
                    '9: Top 15% of accepted papers, strong accept',
                    '8: Top 50% of accepted papers, clear accept',
                    '7: Good paper, accept',
                    '6: Marginally above acceptance threshold',
                    '5: Marginally below acceptance threshold',
                    '4: Ok but not good enough - rejection',
                    '3: Clear rejection',
                    '2: Strong rejection',
                    '1: Trivial or wrong'
                ],
                'required': True
            },
            'confidence': {
                'order': 4,
                'value-radio': [
                    '5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
                    '4: The reviewer is confident but not absolutely certain that the evaluation is correct',
                    '3: The reviewer is fairly confident that the evaluation is correct',
                    '2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper',
                    '1: The reviewer\'s evaluation is an educated guess'
                ],
                'required': True
            }
        }
    }
}
