'''
NAMPI - an ICML workshop

2018-05-08: setup workshop recruiting infrastructure


'''

import openreview
from openreview import invitations
import os

CONFERENCE_ID = 'ICML.cc/2018/Workshop/NAMPI'
PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'
REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'
REVIEWERS_INVITED_ID = REVIEWERS_ID + '/Invited'
REVIEWERS_DECLINED_ID = REVIEWERS_ID + '/Declined'


'''
Group definitions.
'''
CONFERENCE = openreview.Group(**{
    'id': CONFERENCE_ID,
    'readers':['everyone'],
    'writers': [],
    'signatures': [],
    'signatories': [CONFERENCE_ID],
    'members': [],
    'web': '../webfield/homepage.js'
})

PROGRAM_CHAIRS = openreview.Group(**{
    'id': PROGRAM_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [],
    'signatures': [],
    'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'members': [],
})

REVIEWERS = openreview.Group(**{
    'id': REVIEWERS_ID,
    'readers':[CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

REVIEWERS_INVITED = openreview.Group(**{
    'id': REVIEWERS_INVITED_ID,
    'readers':[CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

REVIEWERS_DECLINED = openreview.Group(**{
    'id': REVIEWERS_DECLINED_ID,
    'readers':[CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

'''
Invitation definitions.
'''

RECRUIT_REVIEWERS = invitations.Recruitment(
    id = CONFERENCE_ID + '/-/Recruit_Reviewers',
    conference_id = CONFERENCE_ID,
    process = os.path.abspath('../process/recruitReviewerProcess.js'),
    web = os.path.abspath('../webfield/recruitReviewerWebfield.js')
)

'''
Email templates.
'''
RECRUIT_MESSAGE_SUBJ = 'NAMPI 2018: Invitation to Review'
RECRUIT_MESSAGE = '''Dear {name},

You have been invited to serve as a reviewer for the ICML 2018 NAMPI workshop.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We really hope you will be able to accept our invitation and help us select a high quality program for NAMPI 2018!

Best regards,
The NAMPI 2018 Program Chairs

'''
