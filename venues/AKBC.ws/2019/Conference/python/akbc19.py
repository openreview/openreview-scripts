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
ARCHIVAL_STATUS_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Update_Archival_Status'

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

You have been nominated by the area chairs of the first international conference on Automated Knowledge Base Construction (AKBC) to serve as a reviewer.  As a respected researcher in the area, we hope you will accept and help us make the conference a success.

Reviewers are also welcome to submit papers, so please also consider submitting to the conference!

Key facts:
After 10 years of successful workshops, AKBC is becoming a conference.
Conference web site: http://akbc.ws 
Paper submission deadline: November 16
Review deadline: January 9
Rebuttal and discussion: January 9 - February 1
Discussion between ACs and reviewers: February 1 - February 10
Release of final decisions: February 13
Area Chairs: Tim Rocktäschel, Luke Zettlemoyer, Siva Reddy, Matt Gardner, Hannaneh Hajishirzi, Sunita Sarawagi, Michael Cafarella, Paul Groth, Roman Klinger, Michael Wick, Max Nickel, Jay Pujara, Kai-Wei Chang, Lora Aroyo

We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole AKBC community.

The success of AKBC depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you will accept our invitation.

To ACCEPT the invitation, please click on the following link:


{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

Please answer within 10 days.

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in.

If you have any questions, please contact the program chairs at info@akbc.ws.

Cheers!

Isabelle Augenstein, Program Co-chair
Sameer Singh, Program Co-chair
Andrew McCallum, General Chair

Contact: 
Email: info@akbc.ws
Website: http://akbc.ws 
Twitter: @akbc_conf 

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
FINAL_DECISION_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=2, day=13, hour=22)


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
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
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
                PROGRAM_CHAIRS_ID,
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
submission_inv.reply_params['content']['archival status'] = {'description': 'Authors can change the archival/non-archival status up until the decision deadline',
    'value-radio': [
        'Archival', 
        'Non-Archival'
    ],
    'required': True
}
submission_inv.reply_params['content']['subject areas'] = {'order' : 5,
    'description' : "Select or type subject area",
    'values-dropdown': [
        'Machine Learning',
        'Natural Language Processing',
        'Information Extraction',
        'Question Answering',
        'Reasoning',
        'Databases',
        'Information Integration',
        'Knowledge Representation',
        'Semantic Web',
        'Search',
        'Applications: Science',
        'Applications: Biomedicine',
        'Applications: Other',
        'Relational AI',
        'Fairness',
        'Human computation',
        'Crowd-sourcing',
        'Other'
    ],
    'required': True
}

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
