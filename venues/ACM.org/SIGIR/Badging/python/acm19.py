'''
ACM SIGIR Badging demo configuration
https://acm.org
'''

import openreview
import os


# group ids
CONFERENCE_ID = 'ACM.org/SIGIR/Badging'
SHORT_PHRASE = 'ACM Badging'

CHAIRS_ID = CONFERENCE_ID + '/Chairs'

REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'
REVIEWERS_INVITED_ID = REVIEWERS_ID + '/Invited'
REVIEWERS_DECLINED_ID = REVIEWERS_ID + '/Declined'

AUTHORS_ID = CONFERENCE_ID + '/Authors'

# invitation ids
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'

# template strings
PAPER_TEMPLATE_STR = CONFERENCE_ID + '/Paper<number>'
PAPER_REVIEWERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Reviewers'

# Deadlines
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2050, month=1, day=1, hour=22)

# Global group definitions
conference = openreview.Group.from_json({
    'id': CONFERENCE_ID,
    'readers':['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': ["OpenReview.net"],
    'signatories': [CONFERENCE_ID, CHAIRS_ID],
    'members': []
})
with open(os.path.abspath('../webfield/homepage.js')) as f:
    conference.web = f.read()

chairs = openreview.Group.from_json({
    'id': CHAIRS_ID,
    'readers':[CONFERENCE_ID, CHAIRS_ID],
    'writers': [],
    'signatures': [],
    'signatories': [CONFERENCE_ID, CHAIRS_ID],
    'members': []
})

reviewers = openreview.Group.from_json({
    'id': REVIEWERS_ID,
    'readers':[CONFERENCE_ID, CHAIRS_ID, REVIEWERS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_invited = openreview.Group.from_json({
    'id': REVIEWERS_INVITED_ID,
    'readers':[CONFERENCE_ID, CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_declined = openreview.Group.from_json({
    'id': REVIEWERS_DECLINED_ID,
    'readers':[CONFERENCE_ID, CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

# Configure paper submissions
submission_inv = openreview.Invitation(
    id = SUBMISSION_ID,
    duedate = SUBMISSION_DEADLINE,
    process = os.path.abspath('../process/submissionProcess.js'),
    invitees = ['~'],
    readers = ["everyone"],
    writers = [CONFERENCE_ID],
    signatures = [CONFERENCE_ID],
    reply = {
        'readers': {
            'values': [
                'everyone'
            ]
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'writers': {
            'values-copied': [
                CONFERENCE_ID,
                '{content.authorids}',
                '{signatures}'
            ]
        },
        'content': {
            'title': {
                'fieldDisplayLabel': 'Title',
                'description': 'Title of artifact.',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            'authors': {
                'fieldDisplayLabel': 'Authors',
                'description': 'Comma separated list of author names. Please provide real names.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'fieldDisplayLabel': 'Author IDs',
                'description': '''Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, 
                please make sure that the provided email address(es) match those listed in the author\'s profile. Please provide real emails.''',
                'order': 3,
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required':True
            },
            'abstract': {
                'fieldDisplayLabel': 'Abstract',
                'description': 'Abstract of paper.',
                'order': 4,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'artifact type': {
                'fieldDisplayLabel': 'Artifact Type',
                'description': 'Type of the artifact.',
                'order': 5,
                'values-dropdown': [
                    'Code',
                    'Dataset',
                    'User study log book',
                    'Other'
                ],
                'required': True
            },
            'requested badges': {
                'fieldDisplayLabel': 'Requested Badges',
                'description': 'Please select all the badges that you are requesting for.',
                'order': 6,
                'values-dropdown': [
                    'Artifacts Available',
                    'Artifacts Evaluated – Functional and Reusable',
                    'Results Replicated',
                    'Results Reproduced'
                ],
                'required': True
            },
            'html': {
                'fieldDisplayLabel': 'Html',
                'description': 'Either provide a direct url to your artifact (link must begin with http(s)) or upload a PDF file',
                'order': 7,
                'value-regex': '(http|https):\/\/.+',
                'required':False
            },
            'pdf': {
                'fieldDisplayLabel': 'PDF',
                'order': 8,
                'value-regex': 'upload',
                'required':False
            }
        }
    }
)

# Badging decision invitation for Chairs
badging_decision_inv = openreview.Invitation(
    id = CONFERENCE_ID + '/-/Decision',
    duedate = 1543161141000,
    readers = ['everyone'],
    writers = [CONFERENCE_ID],
    signatures = [CONFERENCE_ID],
    invitees = [CONFERENCE_ID + '/Chairs'],
    multiReply = True,
    taskCompletionCount = 1,
    reply = {
        'invitation': CONFERENCE_ID + '/-/Submission',
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
            'tag': {
                'description': 'Artifact Badge decision',
                'order': 1,
                'values-dropdown': ['No Badges', 'Artifacts Available', 'Artifacts Evaluated – Functional and Reusable', 'Results Replicated', 'Results Reproduced'],
                'required': True
            }
        }
    }
)
