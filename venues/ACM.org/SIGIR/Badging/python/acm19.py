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
    'signatories': [CONFERENCE_ID],
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

# with open(os.path.abspath('../webfield/chairWebfield.js')) as f:
#     chairs.web = f.read()

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

# Template for artifacts

artifactSubmission = {
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
    'pdf': {
        'fieldDisplayLabel': 'PDF',
        'description': 'Either upload a PDF file or provide a direct link to your artifact (link must begin with http(s))',
        'order': 7,
        'value-regex': 'upload|(http|https):\/\/.+',
        'required':True
    }
}

class ArtifactSubmission(openreview.Invitation):
    def __init__(self, conference_id = None, id = None,
        duedate = None, process = None, inv_params = {},
        reply_params = {}, content_params = {}, mask = {}):

        self.conference_id = conference_id

        if id:
            self.id = id
        else:
            self.id = '/'.join([self.conference_id, '-', 'Submission'])

        default_inv_params = {
            'id': self.id,
            'readers': ['everyone'],
            'writers': [self.conference_id],
            'invitees': ['~'],
            'signatures': [self.conference_id],
            'duedate': duedate,
            'process': process
        }

        default_reply_params = {
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
                'values': [self.conference_id]
            }
        }

        self.content_params = {}
        self.content_params.update(artifactSubmission)
        self.content_params.update(content_params)

        if mask:
            self.content_params = mask

        self.reply_params = {}
        self.reply_params.update(default_reply_params)
        self.reply_params.update(reply_params)
        self.reply_params['content'] = self.content_params

        self.inv_params = {}
        self.inv_params.update(default_inv_params)
        self.inv_params.update(inv_params)
        self.inv_params['reply'] = self.reply_params

        super(ArtifactSubmission, self).__init__(**self.inv_params)

    def add_process(self, process):
        self.process = process.render()

# Configure paper submissions
submission_inv = ArtifactSubmission(
    id = SUBMISSION_ID,
    conference_id = CONFERENCE_ID,
    duedate = SUBMISSION_DEADLINE,
    process = os.path.abspath('../process/submissionProcess.js'),
    reply_params = {
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
        }
    }
)
