'''
SIGIR 2019 demo configuration
https://sigir.org
'''

import openreview
from openreview import invitations
import os


# group ids
CONFERENCE_ID = 'SIGIR.org/2019/Badging'
SHORT_PHRASE = 'SIGIR 2019'

CHAIRS_ID = CONFERENCE_ID + '/Chairs'

REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'
REVIEWERS_INVITED_ID = REVIEWERS_ID + '/Invited'
REVIEWERS_DECLINED_ID = REVIEWERS_ID + '/Declined'

AUTHORS_ID = CONFERENCE_ID + '/Authors'

# invitation ids
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'

RECRUIT_REVIEWERS_ID = CONFERENCE_ID + '/-/Recruit_Reviewers'

# template strings
PAPER_TEMPLATE_STR = CONFERENCE_ID + '/Paper<number>'
PAPER_REVIEWERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Reviewers'
PAPER_AUTHORS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Authors'

PUBLIC_COMMENT_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Public_Comment'
OFFICIAL_COMMENT_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Comment'
OFFICIAL_BADGE_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Badge'

# Email templates
HASH_SEED = "2810398440804348173"
RECRUIT_MESSAGE_SUBJ = 'SIGIR 2018: Invitation to Badge artifacts'
RECRUIT_REVIEWERS_MESSAGE = '''Dear {name},

We are writing to invite you for badging for artifacts for SIGIR ACM.
As a recognized researcher by the ACM community, we hope you can contribute to the review process of SIGIR ACM Badging.

Please, make sure you are available during the review, discussion and badging period.
We will be using OpenReview throughout the badging process, which we hope will make the badging process
more engaging and allow us to more effectively leverage the whole SIGIR community.

We hope you can accept our invitation and help make SIGIR thrive.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We'd appreciate an answer within 10 days.

If you accept, please make sure to either update your Toronto Paper Matching System (TPMS) account,
or create one if you do not have one already: http://torontopapermatching.org/webapp/profileBrowser/login/.
We will be using TPMS to assign reviewers to papers, and having an account that reflects your expertise will
be crucial for you to receive papers for which you are suited. Also please make sure your OpenReview account
lists the email you are using for your TPMS account. There will also be a brief survey through the OpenReview system.

If you have any question, please contact the chairs at YYY@googlegroups.com.
We are also maintaining a list of reviewer guidelines and frequently asked questions
here: XYZURL.

We are looking forward to your reply, and are grateful if you accept this invitation and help make this SIGIR badging process a success!

Cheers!

ZZZ, Senior Program Chair
YYYY, Program Chair
XXXX, General Chair

Contact: XYZXYZ@googlegroups.com

'''

# Deadlines
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2020, month=1, day=1, hour=22)

# Global group definitions
conference = openreview.Group.from_json({
    'id': CONFERENCE_ID,
    'readers':['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': ["~Super_User1"],
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

# # Change webfield name in line below
# with open(os.path.abspath('../webfield/programchairWebfield.js')) as f:
#     program_chairs.web = f.read()

reviewers = openreview.Group.from_json({
    'id': REVIEWERS_ID,
    'readers':[CONFERENCE_ID, CHAIRS_ID, REVIEWERS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

# # Change webfield name in line below
# with open(os.path.abspath('../webfield/reviewerWebfield.js')) as f:
#     reviewers.web = f.read()

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
