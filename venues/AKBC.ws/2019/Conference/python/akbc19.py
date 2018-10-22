'''
AKBC 2019 demo configuration
http://www.akbc.ws/
May 20 - May 22, 2019
'''

import openreview
from openreview import invitations
import os

# group ids
CONFERENCE_ID = 'AKBC.ws/2019/Conference'
SHORT_PHRASE = 'AKBC 2019'

PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'
AREA_CHAIRS_ID = CONFERENCE_ID + '/Area_Chairs'
AREA_CHAIRS_INVITED_ID = AREA_CHAIRS_ID + '/Invited'
AREA_CHAIRS_DECLINED_ID = AREA_CHAIRS_ID + '/Declined'

REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'
REVIEWERS_INVITED_ID = REVIEWERS_ID + '/Invited'
REVIEWERS_DECLINED_ID = REVIEWERS_ID + '/Declined'

AUTHORS_ID = CONFERENCE_ID + '/Authors'

# invitation ids
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission'

RECRUIT_AREA_CHAIRS_ID = CONFERENCE_ID + '/-/Recruit_Area_Chairs'
RECRUIT_REVIEWERS_ID = CONFERENCE_ID + '/-/Recruit_Reviewers'

# template strings
PAPER_TEMPLATE_STR = CONFERENCE_ID + '/Paper<number>'
PAPER_REVIEWERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Reviewers'
PAPER_AREA_CHAIRS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Area_Chairs'
PAPER_AUTHORS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Authors'
PAPER_REVIEW_NONREADERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Review_Nonreaders'
PAPER_COMMENT_NONREADERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Comment_Nonreaders'

PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR = PAPER_REVIEWERS_TEMPLATE_STR + '/Unsubmitted'
PAPER_REVIEWERS_SUBMITTED_TEMPLATE_STR = PAPER_REVIEWERS_TEMPLATE_STR + '/Submitted'

PUBLIC_COMMENT_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Public_Comment'
OFFICIAL_COMMENT_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Comment'
OFFICIAL_REVIEW_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Review'

# The groups corresponding to these regexes will get automatically created upon assignment
PAPER_AREA_CHAIRS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/Area_Chair[0-9]+'
PAPER_ANONREVIEWERS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/AnonReviewer[0-9]+'

# paper withdrawal
withdrawal_statement = 'On behalf of the authors of this paper, \
I hereby withdraw this submission from consideration for AKBC 2019. \
I understand that this cannot be undone, \
and that my identity and the identity of my co-authors will be revealed upon withdrawal, \
and that the record of this submission (including all existing reviews and comments) \
will remain publicly accessible on OpenReview.'

# Email templates
HASH_SEED = "2810398440804348173"
RECRUIT_MESSAGE_SUBJ = 'AKBC 2019: Invitation to Review'
RECRUIT_REVIEWERS_MESSAGE = '''Dear {name},

We are writing to invite you to be a reviewer for the 1st Conference on Automated Knowledge Base Construction (AKBC 2019), to take place in Amherst, MA, May 20-22, 2019, Monday-Wednesday; see call for papers at: http://www.akbc.ws/2019/cfp/.
As a recognized researcher by the AKBC community, we hope you can contribute to the review process of AKBC 2019.

A tentative timeline for the AKBC reviewing process is:
November 16: Paper submission deadline
January 9: Review deadline
January 9 - February 1: Rebuttal and discussion
February 1 - February 10: Discussion between ACs and reviewers
February 13: Release of final decisions

Please, make sure you are available during the review and discussion period.
We will be using OpenReview throughout the review process, which we hope will make the review process more engaging and allow us to more effectively leverage the whole AKBC community.

The success of AKBC depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you can accept our invitation and help make the first AKBC conference a great success.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We'd appreciate an answer within 10 days.

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.

If you have any questions, please contact the program chairs at info@akbc.ws.

We are looking forward to your reply, and are grateful if you accept this invitation and help make AKBC 2019 a success!

Cheers!

Isabelle Augenstein, Program Co-chair
Sameer Singh, Program Co-chair
Andrew McCallum, General Chair

Contact: info@akbc.ws

'''

RECRUIT_AREA_CHAIRS_MESSAGE = '''Dear {name},

You have been invited to serve as an area chair for the AKBC 2019 Conference.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We  hope you will be able to accept our invitation and help us select a high quality program for AKBC 2019.

Best regards,
The AKBC 2019 Program Chairs

'''

# Deadlines

# submission deadline is 
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=11, day=17, hour=8)
BLIND_SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=11, day=23, hour=23)

# add bid deadline is 2PM PST = 10PM GMT = 5PM EDT
ADD_BID_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=11, day=30, hour=22)
OFFICIAL_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=1, day=9, hour=22)
QUESTIONNAIRE_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=2, hour=22)
QUESTIONNAIRE_EXPIRY = openreview.tools.timestamp_GMT(year=2018, month=10, day=20)
META_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=1, day=10, hour=22)


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

program_chairs = openreview.Group.from_json({
    'id': PROGRAM_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [],
    'signatures': [],
    'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'members': []
})
with open(os.path.abspath('../webfield/programchairWebfield.js')) as f:
    program_chairs.web = f.read()

area_chairs = openreview.Group.from_json({
    'id': AREA_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, AREA_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': []
})
with open(os.path.abspath('../webfield/areachairWebfield.js')) as f:
    area_chairs.web = f.read()

area_chairs_invited = openreview.Group.from_json({
    'id': AREA_CHAIRS_INVITED_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

area_chairs_declined = openreview.Group.from_json({
    'id': AREA_CHAIRS_DECLINED_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers = openreview.Group.from_json({
    'id': REVIEWERS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, AREA_CHAIRS_ID, REVIEWERS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})
with open(os.path.abspath('../webfield/reviewerWebfield.js')) as f:
    reviewers.web = f.read()

reviewers_invited = openreview.Group.from_json({
    'id': REVIEWERS_INVITED_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_declined = openreview.Group.from_json({
    'id': REVIEWERS_DECLINED_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

authors = openreview.Group.from_json({
    'id': AUTHORS_ID,
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})
with open(os.path.abspath('../webfield/authorWebfield.js')) as f:
    authors.web = f.read()

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
            'values-regex': '~.*',
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

blind_submission_inv = invitations.Submission(
    id = BLIND_SUBMISSION_ID,
    conference_id = CONFERENCE_ID,
    duedate = BLIND_SUBMISSION_DEADLINE,
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
            'values': ['everyone']
        }
    }
)

# Configure reviewer recruitment
recruit_reviewers = invitations.RecruitReviewers(
    id = RECRUIT_REVIEWERS_ID,
    conference_id = CONFERENCE_ID,
    process = os.path.abspath('../process/recruitReviewersProcess.js'),
    web = os.path.abspath('../webfield/recruitResponseWebfield.js'),
    inv_params = {
        'invitees': ['everyone']
    },
    reply_params = {
        'signatures': {'values': ['(anonymous)']}
    }
)

# Configure bidding
add_bid = invitations.AddBid(
    conference_id = CONFERENCE_ID,
    duedate = ADD_BID_DEADLINE,
    completion_count = 50,
    inv_params = {
        'readers': [
            CONFERENCE_ID,
            PROGRAM_CHAIRS_ID,
            REVIEWERS_ID,
            AREA_CHAIRS_ID
        ],
        'invitees': [],
        'web': os.path.abspath('../webfield/bidWebfield.js')
    }
)

SCORES_INV_ID = CONFERENCE_ID + '/-/User_Scores'
scores_inv = openreview.Invitation.from_json({
    'id': SCORES_INV_ID,
    'invitees': [CONFERENCE_ID],
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'content': {},
        'forum': None,
        'replyto': None,
        'invitation': BLIND_SUBMISSION_ID,
        'readers': {'values-regex':'~.*'},
        'writers': {'values': [CONFERENCE_ID]}
    }
})


METADATA_INV_ID = CONFERENCE_ID + '/-/Paper_Metadata'

# Metadata and matching stuff
metadata_inv = openreview.Invitation.from_json({
    'id': METADATA_INV_ID,
    'readers': [
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': BLIND_SUBMISSION_ID,
        'readers': {
            'values': [
                CONFERENCE_ID,
            ]
        },
        'writers': {
            'values': [CONFERENCE_ID]
        },
        'signatures': {
            'values': [CONFERENCE_ID]},
        'content': {}
    }
})

ASSIGNMENT_INV_ID = CONFERENCE_ID + '/-/Paper_Assignment'

assignment_inv = openreview.Invitation.from_json({
    'id': ASSIGNMENT_INV_ID,
    'readers': [CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': BLIND_SUBMISSION_ID,
        'readers': {'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]},
        'writers': {'values': [CONFERENCE_ID]},
        'signatures': {'values': [CONFERENCE_ID]},
        'content': {}
    }
})

CONFIG_INV_ID = CONFERENCE_ID + '/-/Assignment_Configuration'

config_inv = openreview.Invitation.from_json({
    'id': CONFIG_INV_ID,
    'readers': [CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [PROGRAM_CHAIRS_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': None,
        'readers': {'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]},
        'writers': {'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]},
        'signatures': {'values': [PROGRAM_CHAIRS_ID]},
        'content': {}
    }

})

# This is the Conference level Invitation for all withdrawn submissions
withdrawn_submission_invitation = openreview.Invitation.from_json({
    'id': CONFERENCE_ID + "/-/Withdrawn_Submission",
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': [CONFERENCE_ID],
    'noninvitees': [],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': [CONFERENCE_ID]
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values':  [CONFERENCE_ID]
        },
        'content': {}
    },
    "nonreaders": []
})
