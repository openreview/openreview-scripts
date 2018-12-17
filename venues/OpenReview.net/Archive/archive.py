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
    'duedate': None,
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

confirmation_tag_invitation = openreview.Invitation(**{
    'id': 'OpenReview.net/Archive/-/Authorship_Claim',
    'duedate': 2538773200000,
    'expdate': None,
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Archive'],
    'signatures': ['OpenReview.net/Archive'],
    'invitees': ['~'],
    'multiReply': True,
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'OpenReview.net/Archive/-/Imported_Record',
        'readers': {
            'values': ['everyone']
        },
        'signatures': {'values-regex': '~.*'},
        'content': {
            'tag': {
                'value-dropdown': [
                    'Yes, I am an author of this paper.',
                    'No, I am not an author of this paper.',
                ],
                'required': True,
                'description': 'Is this your paper?'
           }
        }
    }
})

imported_record_invitation = openreview.Invitation(
    id='OpenReview.net/-/Imported_Record',
    signatures=['SemanticScholar.org'],
    readers=['everyone'],
    writers=['OpenReview.net'],
    invitees=['OpenReview.net'],
    reply={
        'readers': {'values':['everyone']},
        'writers': {'values': []},
        'signatures': {'values': ['SemanticScholar.org']},
        'content': {
            'title': {
                'value-regex': '.{1,300}',
                'required': True,
                'description': 'Title of paper.',
                'order': 1
            },
            'abstract': {
                'value-regex': '[\\S\\s]*',
                'required': False,
                'description': 'Abstract of paper.',
                'order': 8
            },
            'authorids': {
                'values-regex': '.*',
                'required': True,
                'description': "Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author's profile. Please provide real emails; identities will be anonymized.",
                'order': 3
            },
            'authors': {
                'values-regex': '[^;,\\n]+(,[^,\\n]+)*',
                'required': True,
                'description': 'Comma separated list of author names. Please provide real names; identities will be anonymized.',
                'order': 2}
        }
    }
)
