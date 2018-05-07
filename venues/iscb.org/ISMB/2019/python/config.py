# constants go here

import openreview
from openreview import webfield
from openreview import invitations
import os

'''
Define IDs. We do this so that we can assign ids to parameters
without having to create the objects first
'''

CONFERENCE_ID = 'iscb.org/ISMB/2019'
PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'
AREA_CHAIRS_ID = CONFERENCE_ID + '/Area_Chairs'
REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'

SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission'
RECRUIT_REVIEWERS_ID = 'TBD'


DEADLINE_TIMESTAMP = openreview.tools.timestamp_GMT(2019, 5, 1)
'''
Setup the homepage
'''

JS_CONSTANTS = {
    'CONFERENCE': CONFERENCE_ID,
    'AREA_CHAIRS': AREA_CHAIRS_ID,
    'PROGRAM_CHAIRS': PROGRAM_CHAIRS_ID,
    'REVIEWERS': REVIEWERS_ID,
    'SUBTITLE': 'Intelligent Systems in Molecular Biology',
    'TITLE': 'ISMB 2019',
    'RECRUIT_REVIEWERS': RECRUIT_REVIEWERS_ID,
    'DEADLINE': DEADLINE_TIMESTAMP,
    'DATE_STRING': 'May 5, 2019',
    'BLIND_INVITATION': BLIND_SUBMISSION_ID,
    'INSTRUCTIONS': 'test instructions',
    'WEBSITE': 'https://www.iscb.org/ismb2018-submit',
    'LOCATION': 'Location TBD',
    'SUBMISSION_INVITATION': SUBMISSION_ID,
}

HOMEPAGE = webfield.Webfield(
    os.path.join(os.path.dirname(__file__), '../webfield/homepage.js'),
    group_id = CONFERENCE_ID,
    js_constants = JS_CONSTANTS
).render()


'''
Setup the groups
'''

CONFERENCE = openreview.Group(**{
    'id': CONFERENCE_ID,
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [],
    'signatories': [],
    'members': []
})

CONFERENCE.web = HOMEPAGE

PROGRAM_CHAIRS = openreview.Group(**{
    'id': PROGRAM_CHAIRS_ID,
    'readers': [
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID,
    ],
    'writers': [ CONFERENCE_ID ],
    'signatures': [ CONFERENCE_ID ],
    'members': [],
    'signatories': []
})

REVIEWERS = openreview.Group(**{
    'id': REVIEWERS_ID,
    'readers': [
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID,
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'members': [],
    'signatories': []
})

AREA_CHAIRS = openreview.Group(**{
    'id': AREA_CHAIRS_ID,
    'readers': [
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID,
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'members': [],
    'signatories': []
})

SUBMISSION = invitations.Submission(
    id = SUBMISSION_ID,
    duedate = DEADLINE_TIMESTAMP, #  (GMT): Saturday, 10 March 2018 10:59:59
    reply_params = {
        'readers': {'values-copied': [
                CONFERENCE_ID, '{content.authorids}', '{signatures}']},
        'signatures': {'values-regex': '~.*|' + CONFERENCE_ID},
        'writers': {'values-regex': '~.*|' + CONFERENCE_ID}
    },
    content_params = {}
)

BLIND_SUBMISSION = invitations.Submission(
    id = BLIND_SUBMISSION_ID,
    duedate = DEADLINE_TIMESTAMP, #  (GMT): Saturday, 10 March 2018 10:59:59
    mask = {
        'authors': {'values': ['Anonymous']},
        'authorids': {'values-regex': '.*'}
    },
    reply_params = {
        'signatures': {'values': [CONFERENCE_ID]},
        'readers': {'values-regex': CONFERENCE_ID + '.*'}
    }
)
