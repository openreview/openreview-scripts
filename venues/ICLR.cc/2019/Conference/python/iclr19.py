'''
ICLR 2019 demo configuration
https://iclr.cc
Monday June 10 - Saturday June 15, 2019
'''

import openreview
from openreview import invitations
import os


# group ids
CONFERENCE_ID = 'ICLR.cc/2019/Conference'
SHORT_PHRASE = 'ICLR 2019'

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
I hereby withdraw this submission from consideration for ICLR 2019. \
I understand that this cannot be undone, \
and that my identity and the identity of my co-authors will be revealed upon withdrawal, \
and that the record of this submission (including all existing reviews and comments) \
will remain publicly accessible on OpenReview.'

# Email templates
HASH_SEED = "2810398440804348173"
RECRUIT_MESSAGE_SUBJ = 'ICLR 2019: Invitation to Review'
RECRUIT_REVIEWERS_MESSAGE = '''Dear {name},

We are writing to invite you to be a reviewer for the 7th International Conference on Learning Representations
(ICLR 2019); see call for papers at: www.iclr.cc.
As a recognized researcher by the ICLR community, we hope you can contribute to the review process of ICLR 2019.

The reviewing period will start around September 27th for conference submissions.
A tentative timeline for the ICLR reviewing process is:

September 27: Paper submission deadline
October 29: Review deadline
November 8 - November 21: Rebuttal and discussion
November 21 - December 5: Discussion between ACs and reviewers

Please, make sure you are available during the review and discussion period before accepting.
We will be using OpenReview throughout the review process, which we hope will make the review process
more engaging and allow us to more effectively leverage the whole ICLR community.

The success of ICLR depends on the quality of the reviewing process and ultimately on the quality and
dedication of the reviewers. We hope you can accept our invitation and help make ICLR thrive.

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

If you have any question, please contact the program chairs at iclr2019programchairs@googlegroups.com .
We are also maintaining a list of reviewer guidelines and frequently asked questions
here: https://iclr.cc/Conferences/2019/PaperInformation/ReviewerACGuidelines.

We are looking forward to your reply, and are grateful if you accept this invitation and help make ICLR 2019 a success!

Cheers!

Alexander Rush, Senior Program Chair
Sergey Levine, Program Chair
Karen Livescu, Program Chair
Shakir Mohamed, Program Chair
Tara Sainath, General Chair

Contact: iclr2019programchairs@googlegroups.com

'''

RECRUIT_AREA_CHAIRS_MESSAGE = '''Dear {name},

You have been invited to serve as an area chair for the ICLR 2019 Conference.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We  hope you will be able to accept our invitation and help us select a high quality program for ICLR 2019.

Best regards,
The ICLR 2019 Program Chairs

'''


# Deadlines
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=9, day=27, hour=22)
BLIND_SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=10, hour=9)
ADD_BID_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=6, hour=0)
OFFICIAL_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=29)
QUESTIONNAIRE_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=2, hour=22)
QUESTIONNAIRE_EXPIRY = openreview.tools.timestamp_GMT(year=2018, month=10, day=20)
META_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=11, day=7)



# Global group definitions
conference = openreview.Group.from_json({
    'id': CONFERENCE_ID,
    'readers':['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [],
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
                # CONFERENCE_ID, //seems like we can remove this
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

# User "registration".
# this is a workaround to force ICLR to show up in users'
# "your active venues" list, even if they haven't replied to
# any active ICLR invitations.
# It's a workaround in the sense that it requires us to
# falsify the "tauthor" field in the note using the Super User.

register_user_inv = openreview.Invitation.from_json({
    'id': CONFERENCE_ID + '/-/Register_User',
    'readers': ['everyone'],
    'writers': [],
    'invitees': ['~'],
    'signatures': [CONFERENCE_ID],
    # The dates below are the day after the in-person meeting of the conference
    'expdate': openreview.tools.timestamp_GMT(year=2019, month=5, day=10),
    'duedate': openreview.tools.timestamp_GMT(year=2019, month=5, day=10),
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {'values': [CONFERENCE_ID]},
        'writers': {'values': [CONFERENCE_ID]},
        'signatures': {'values': [CONFERENCE_ID]},
        'content': {
            'registered': {
                'value': 'yes'
            }
        }
    }
})

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

questionnaire_instructions_invitation = openreview.Invitation.from_json({
    'id': CONFERENCE_ID + '/-/Reviewer_Questionnaire',
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [CONFERENCE_ID],
    'duedate': QUESTIONNAIRE_DEADLINE,
    'expdate': QUESTIONNAIRE_EXPIRY,
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {'values': [REVIEWERS_ID, AREA_CHAIRS_ID, PROGRAM_CHAIRS_ID, CONFERENCE_ID]},
        'writers': {'values': [CONFERENCE_ID]},
        'signatures': {'values': [CONFERENCE_ID]},
        'content': {
            'title': {'value': 'Questionnaire for Reviewers'},
            'Instructions': {
                'value': 'Help us get to know our reviewers better and the ways to make the reviewing process smoother by answering these questions. If you don\'t see the questionnaire form below, click on the blue "Reviewer Questionnaire Response" button.',
                'order': 1
            }
        }
    }
})

questionnaire_instructions_note = openreview.Note.from_json({
    'readers': questionnaire_instructions_invitation.reply['readers']['values'],
    'writers': questionnaire_instructions_invitation.reply['writers']['values'],
    'signatures': questionnaire_instructions_invitation.reply['signatures']['values'],
    'invitation': questionnaire_instructions_invitation.id,
    'content': {
        'title': questionnaire_instructions_invitation.reply['content']['title']['value'],
        'Instructions': questionnaire_instructions_invitation.reply['content']['Instructions']['value'],
    }
})

questionnaire_response_template = {
    'id': CONFERENCE_ID + '/-/Reviewer_Questionnaire_Response',
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [REVIEWERS_ID],
    'duedate': QUESTIONNAIRE_DEADLINE,
    'expdate': QUESTIONNAIRE_EXPIRY,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {'values': [PROGRAM_CHAIRS_ID]},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'Confirm Profile Updated': {
                'description': 'Have you updated your OpenReview profile to include your most up-to-date relations, work history, and conflicts of interest?',
                'value-radio': ['Yes', 'No'],
                'order': 1,
                'required': True
            },
            'Confirm TPMS Registration': {
                'description': 'Have you registered and/or updated your TPMS account, and updated your OpenReview profile to include the email address you used for TPMS?',
                'value-radio': ['Yes', 'No'],
                'order': 2,
                'required': True
            },
            'Current Positions': {
                'description': 'Which categories describe you best? Select all that apply.',
                'values-dropdown': [
                    'Academia: Lecturer/Assistant Professor',
                    'Academia: Post-doctoral candidate',
                    'Academia: Associate Professor/Reader',
                    'Academia: Full professor',
                    'Industry: Research Scientist',
                    'Industry: Research Engineer',
                    'Industry: Software Engineer',
                    'Student: PhD',
                    'Student: Masters',
                    'Student: Other',
                    'Other' # At some point we'll want to let them add text here
                ],
                'order': 3,
                'required': True
            },
            'Reviewing Experience': {
                'description': 'How many times have you been a reviewer for any conference or journal?',
                'value-radio': [
                    'Never - this is my first time',
                    '1 time - building my reviewer skills',
                    '2-4 times  - comfortable with the reviewing process',
                    '5-10 times  - active community citizen',
                    '10+ times  - seasoned reviewer'
                ],
                'order': 4,
                'required': True

            },
            'Previous ICLR Author': {
                'description': 'Have you published at ICLR in the last two years?',
                'value-radio': ['Yes','No'],
                'order': 5,
                'required': True
            },
            'Your Recent Publication Venues': {
                'description': 'Where have you recently published? Select all that apply.',
                'values-dropdown': [
                    'Neural Information Processing Systems (NIPS)',
                    'International Conference on Machine Learning (ICML)',
                    'Artificial Intelligence and Statistics (AISTATS)',
                    'Uncertainty in Artificial Intelligence (UAI)',
                    'Association for Advances in Artificial Intelligence (AAAI)',
                    'Computer Vision and Pattern Recognition (CVPR)',
                    'International Conference on Computer Vision (ICCV)',
                    'International Joint Conference on Artificial Intelligence (IJCAI)',
                    'Robotics: Systems and Science (RSS)',
                    'Conference on Robotics and Learning (CORL)',
                    'Association for Computational Linguistics or related (ACL/NAACL/EACL)',
                    'Empirical Methods in Natural Language Processing (EMNLP)',
                    'Conference on Learning Theory (COLT)',
                    'Algorithmic Learning Theory (ALT)',
                    'Knowledge Discovery and Data Mining (KDD)',
                    'Other'
                ],
                'order': 6,
                'required': True
            },
            'Reviewing Preferences': {
                'description': 'What is the most important factor of the reviewing process for you? (Choose one)',
                'value-radio': [
                    'Getting papers that best match my area of expertise',
                    'Having the smallest number of papers to review',
                    'Having a long-enough reviewing period (6-8 weeks)',
                    'Having enough time for active discussion about papers.',
                    'Receiving clear instructions about the expectations of reviews.'
                ],
                'order': 7,
                'required': True
            }
        }
    }
}

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
    'invitees': ['ICLR.cc/2019/Conference'],
    'readers': ['everyone'],
    'writers': ['ICLR.cc/2019/Conference'],
    'signatures': ['ICLR.cc/2019/Conference'],
    'reply': {
        'content': {},
        'forum': None,
        'replyto': None,
        'invitation': 'ICLR.cc/2019/Conference/-/Blind_Submission',
        'readers': {'values-regex':'~.*'},
        'writers': {'values': ['ICLR.cc/2019/Conference']}
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
    'readers': [CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': None,
        'readers': {'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]},
        'writers': {'values': [CONFERENCE_ID]},
        'signatures': {'values': [CONFERENCE_ID]},
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

# Configure the invitations that will be attached on a per-paper basis
# These are constructed using templates in the script invitations.py


