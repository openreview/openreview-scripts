import openreview

archive_group = openreview.Group(**{
    'id': 'OpenReview.net/Archive',
    'members': [],
    'writers': [],
    'readers': ['everyone'],
    'signatures': ['OpenReview.net'],
    'signatories': [],
    'web': './archiveWebfield.js'
})

direct_upload_invitation = openreview.Invitation(**{
    'id': 'OpenReview.net/Archive/-/Direct_Upload',
    'readers': ['~'],
    'writers': ['OpenReview.net'],
    'signatures': ['OpenReview.net'],
    'invitees': ['~'],
    'duedate': 2539795181000,
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'Your authorized identity to be associated with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values-regex': '~.*'
        },
        'content': {
            'pdf': {
                'description': 'Choose one of the following: (1) Upload a PDF file. (2) Enter a URL to a PDF file.',
                'order': 2,
                'value-regex': 'upload|(http|https):\/\/.+\.pdf',
                'required': True
            },
            'title': {
                'description': 'Title of paper.',
                'order': 3,
                'value-regex': '.{1,250}',
                'required': True
            },
            'authors': {
                'description': 'Comma separated list of author names.',
                'order': 4,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required': True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match at least one of those listed in the author\'s profile.',
                'order': 5,
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required': True
            }
        }

    }
})

homepage_upload_invitation = openreview.Invitation(**{
    'id': 'OpenReview.net/-/Homepage_Upload',
    'readers': ['~'],
    'writers': ['OpenReview.net'],
    'signatures': ['OpenReview.net'],
    'invitees': ['~'],
    'duedate': 2539795181000,
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': ['{signatures}']
        },
        'signatures': {
            'description': 'Your authorized identity to be associated with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values-regex': ['~.*']
        },
        'content': {
            'homepage': {
                'description': 'Enter the URL of your homepage containing links to paper PDFs.',
                'order': 1,
                'value-regex': '(http|https):\/\/.+',
                'required': True
            }
        }

    }
})
