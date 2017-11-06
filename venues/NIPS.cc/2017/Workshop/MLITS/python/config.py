#!/usr/bin/python

import sys, os

"""
GROUPS

Defines constants for CONF (the name of the conference), and for the names of each group.
All other groups will be named by joining the name with CONF: <CONF>/<NAME>

Example:

    CONF = 'my.conference/2017'
    PROGRAM_CHAIRS = 'Program_Chairs'

    --> my.conference/2017/Program_Chairs

"""

CONF = "NIPS.cc/2017/Workshop/MLITS"
ADMIN = CONF + '/Admin'
PROGRAM_CHAIRS = CONF + '/Program_Chairs'
AREA_CHAIRS = CONF + '/Area_Chairs'
REVIEWERS = CONF + '/Reviewers'
### Duedate Oct 21, 23:59 UTC
DUE_TIMESTAMP = 1508630350000
## Nov 10 23:59 GMT
REVIEW_DUE_TIMESTAMP = 1510358399000
WEBPATH = os.path.join(os.path.dirname(__file__), '../webfield/conf.html')

"""
INVITATIONS

Defines constants for various invitations.
The full name of an invitation will be generated by joining the name with CONF by "/-/": <CONF>/-/<INVITATION_NAME>

Example:

    CONF = 'my.conference/2017'
    SUBMISSION = 'Submission'

    --> my.conference/2017/-/Submission

"""

SUBMISSION = CONF + '/-/Submission'
COMMENT = CONF + '/-/Comment'


"""
PARAMETERS

Dictionaries that represent argument combinations defining Group and Invitation permissions.

Example:

    restricted = {
        'readers': [CONF],
        'writers': [CONF],
        'signatories': [CONF],
    }

    The "restricted" configuration above will only allow the CONF group to read, write, and sign
    for the newly created Group that uses it.
"""

group_params = {
    'readers': [CONF],
    'writers': [CONF],
    'signatories': [CONF],
    'signatures': [CONF]
}

submission_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': ['~'],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/submissionProcess.js')
}

comment_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': ['~'],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/commentProcess.js')
}

review_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/officialReviewProcess.js')
}


"""
TEMPLATES

"""


submission_reply = {
    'forum': None,
    'replyto': None,
    'invitation': None,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['everyone']
    },
    'signatures': {
        'description': 'How your identity will be displayed with the above content.',
        'values-regex': '~.*'
    },
    'writers': {
        'values': []
    },
    'content':{
        'title': {
            'description': 'Title of paper (up to 250 chars).',
            'order': 1,
            'value-regex': '.{1,250}',
            'required':True
        },
        'authors': {
            'description': 'Comma separated list of author names.',
            'order': 2,
            'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
            'required':True
        },
        'authorids': {
            'description': 'Comma separated list of author email addresses, lowercase, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile.',
            'order': 3,
            'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
            'required':True
        },
        'keywords': {
            'description': 'Comma separated list of keywords.',
            'order': 6,
            'values-regex': "(^$)|[^;,\\n]+(,[^,\\n]+)*"
        },
        'TL;DR': {
            'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper (up to 250 chars)',
            'order': 7,
            'value-regex': '[^\\n]{0,250}',
            'required':False
        },
        'abstract': {
            'description': 'Abstract of paper (up to 5000 chars).',
            'order': 8,
            'value-regex': '[\\S\\s]{1,5000}',
            'required':True
        },
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'order': 9,
            'value-regex': 'upload',
            'required':True
        }
    }
}

comment_reply = {
    'forum': None,
    'replyto': None,
    'invitation': SUBMISSION,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['everyone']
    },
    'signatures': {
        'description': 'How your identity will be displayed with the above content.',
        'values-regex': '~.*'
    },
    'writers': {
        'values-regex': '~.*'
    },
    'content':{
        'title': {
            'order': 0,
            'value-regex': '.{1,500}',
            'description': 'Brief summary of your comment (up to 500 chars).',
            'required': True
        },
        'comment': {
            'order': 1,
            'value-regex': '[\\S\\s]{1,5000}',
            'description': 'Your comment or reply (up to 5000 chars).',
            'required': True
        }
    }
}

review_content = {
    'title': {
        'order': 1,
        'value-regex': '.{0,500}',
        'description': 'Brief summary of your review (up to 500 chars).',
        'required': True
    },
    'review': {
        'order': 2,
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (up to 5000 chars).',
        'required': True
    },
    'rating': {
        'order': 3,
        'value-dropdown': [
            '5: Top 15% of accepted papers, strong accept',
            '4: Top 50% of accepted papers, clear accept',
            '3: Marginally above acceptance threshold',
            '2: Marginally below acceptance threshold',
            '1: Strong rejection'
        ],
        'required': True
    },
    'confidence': {
        'order': 4,
        'value-radio': [
            '3: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
            '2: The reviewer is fairly confident that the evaluation is correct',
            '1: The reviewer\'s evaluation is an educated guess'
        ],
        'required': True
    }
}