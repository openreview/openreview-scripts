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

SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission'

SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=6, day=1)

'''
Group definitions.
'''
conference = openreview.Group(**{
    'id': CONFERENCE_ID,
    'readers':['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
    'web': '../webfield/homepage.js'
})

program_chairs = openreview.Group(**{
    'id': PROGRAM_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [],
    'signatures': [],
    'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'members': [],
})

reviewers = openreview.Group(**{
    'id': REVIEWERS_ID,
    'readers':[CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_invited = openreview.Group(**{
    'id': REVIEWERS_INVITED_ID,
    'readers':[CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_declined = openreview.Group(**{
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

# Recruitment
recruit_reviewers = invitations.RecruitReviewers(
    id = CONFERENCE_ID + '/-/Recruit_Reviewers',
    conference_id = CONFERENCE_ID,
    process = os.path.abspath('../process/recruitReviewerProcess.js'),
    web = os.path.abspath('../webfield/recruitReviewerWebfield.js')
)


# Configure paper submissions
submission_inv = invitations.Submission(
    id = SUBMISSION_ID,
    conference_id = CONFERENCE_ID,
    duedate = SUBMISSION_DEADLINE,
    process = os.path.abspath('../process/submissionProcess.js'),
    reply_params = {
        'readers': {
            'values-copied': [
                CONFERENCE_ID,
                '{content.authorids}',
                '{signatures}'
            ]
        },
        'signatures': {
            'values-regex': '|'.join(['~.*', CONFERENCE_ID])
        },
        'writers': {
            'values-copied': [
                CONFERENCE_ID,
                '{signatures}'
            ]
        }
    }
)

blind_submission_inv = invitations.Submission(
    id = BLIND_SUBMISSION_ID,
    conference_id = CONFERENCE_ID,
    duedate = SUBMISSION_DEADLINE,
    mask = {
        'authors': {
            'values': ['Anonymous']
        },
        'authorids': {
            'values-regex': '.*'
        }
    },
    reply_params = {
        'signatures': {
            'values': [CONFERENCE_ID]},
        'readers': {
            'values-regex': CONFERENCE_ID + '.*'
        }
    }
)

'''
Email templates.
'''
RECRUIT_MESSAGE_SUBJ = 'Invitation to review for Neural Abstract Machines & Program Induction v2 (NAMPI_v2) workshop @ ICML 2018'
RECRUIT_MESSAGE = '''Dear {name},

We would like to invite you to serve on the Program Committee for the Neural Abstract Machines & Program Induction v2 (NAMPI_v2) workshop at ICML 2018. The workshop will broadly focus on neural approaches to computation, program induction, algorithm learning, abstract machines and data structures, and their relation to established learning and non-learning methods in the field. More details can be found here: https://uclmr.github.io/nampi/

The NAMPI_v2 workshop will be held in Stockholm, Sweden on July 15th, 2018.

The Program Committee will review up to 4-page (not including references) submissions, and will consist of experts in various fields of interest for the workshop. Realising your busy schedule, we will try to keep the load as low as possible. Our current estimate is 1-2 papers a person max.

We would be grateful if you could confirm your acceptance or refusal of the participation in the NAMPI_v2 committee by clicking on one of the links below..


To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

Workshop deadlines:
Paper submission: June 1st (There will be no extensions)
Notification of acceptance: June 15th
Final Papers Due: June 22nd
Deadlines are at 11:59pm PDT.

We will strive to organise a double-blind review with open comments on OpenRreview.net. In case double-blind review will not be available upon time of submission, we will do a single-blind review.

In case you accept the invitation, we will soon send you further instructions on how to proceed with the reviewing duties.

Please confirm your participation as soon as possible. We know that we will make NAMPI_v2 a big success with your help.



Kind regards,
Dawn, Matko, Pushmeet, Rob, Sebastian, Tejas, Tim


'''
