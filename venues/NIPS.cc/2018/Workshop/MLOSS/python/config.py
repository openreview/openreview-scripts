#!/usr/bin/python

import sys, os
from openreview import tools
"""
GROUPS

Defines constants for CONFERENCE_ID (the name of the conference), and for the names of each group.
All other groups will be named by joining the name with CONFERENCE_ID: <CONFERENCE_ID>/<NAME>

Example:

    CONFERENCE_ID = 'my.conference/2017'
    PROGRAM_CHAIRS = 'Program_Chairs'

    --> my.conference/2017/Program_Chairs

"""

CONFERENCE_ID = 'NIPS.cc/2018/Workshop/MLOSS'
PROGRAM_CHAIRS = CONFERENCE_ID + '/Program_Chairs'
REVIEWERS = CONFERENCE_ID + '/Reviewers'

# GMT is the same as UTC
SUBMISSION_TIMESTAMP = tools.timestamp_GMT(2018, month=9, day=30, hour=23, minute=59)
REVIEW_TIMESTAMP = tools.timestamp_GMT(2018, month=10, day=20, hour=23, minute=59)
WEBPATH = os.path.join(os.path.dirname(__file__), '../webfield/conferenceWebfield.js')


"""
INVITATIONS

Defines constants for various invitations.
The full name of an invitation will be generated by joining the name with CONFERENCE_ID by "/-/": <CONFERENCE_ID>/-/<INVITATION_NAME>

Example:

    CONFERENCE_ID = 'my.conference/2017'
    SUBMISSION = 'Submission'

    --> my.conference/2017/-/Submission

"""

SUBMISSION = CONFERENCE_ID + '/-/Submission'
BLIND_SUBMISSION = CONFERENCE_ID + '/-/Blind_Submission'
COMMENT = CONFERENCE_ID + '/-/Comment'

"""
PARAMETERS

Dictionaries that represent argument combinations defining Group and Invitation permissions.

Example:

    restricted = {
        'readers': [CONFERENCE_ID],
        'writers': [CONFERENCE_ID],
        'signatories': [CONFERENCE_ID],
    }

    The "restricted" configuration above will only allow the CONFERENCE_ID group to read, write, and sign
    for the newly created Group that uses it.
"""
conference_params = {
    'id': CONFERENCE_ID,
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [],
    'signatories': [CONFERENCE_ID],
    'members': []
}

group_params = {
    'readers': [CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID]
}

program_chairs_params = {
    'readers': [CONFERENCE_ID, PROGRAM_CHAIRS],
    'writers': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS],
    'signatures': [CONFERENCE_ID],
}

submission_params = {
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': ['~'],
    'signatures': [CONFERENCE_ID],
    'process': os.path.join(os.path.dirname(__file__), '../process/submissionProcess.js')
}

comment_params = {
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': ['~'],
    'signatures': [CONFERENCE_ID],
    'process': os.path.join(os.path.dirname(__file__), '../process/commentProcess.js')
}


review_params = {
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'duedate': REVIEW_TIMESTAMP
}


"""
TEMPLATES

"""

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
        'order': 4,
        'value-dropdown': [
            '5: Top 15% of accepted papers, strong accept',
            '4: Top 50% of accepted papers, clear accept',
            '3: Marginally above acceptance threshold',
            '2: Marginally below acceptance threshold',
            '1: Strong rejection'
        ],
        'required': True
    },
    'presentation': {
        'order': 6,
        'description':'Recommended presentation style:',
        'value-radio': [
            'Poster spotlight',
            'Talk',
            'Demo'
        ],
        'required': True
    },
    'confidence': {
        'order': 5,
        'value-radio': [
            '3: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
            '2: The reviewer is fairly confident that the evaluation is correct',
            '1: The reviewer\'s evaluation is an educated guess'
        ],
        'required': True
    }
}
