'''
ICLR 2019 demo configuration
https://iclr.cc
Monday June 10 - Saturday June 15, 2019
'''

import openreview
from openreview import invitations
import os


with open('subject_areas.csv') as f:
    subject_areas = f.read().split(',\n')

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

OPEN_COMMENT_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Open_Comment'
OFFICIAL_COMMENT_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Comment'
OFFICIAL_REVIEW_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Review'

# The groups corresponding to these regexes will get automatically created upon assignment
PAPER_AREA_CHAIRS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/Area_Chair[0-9]+'
PAPER_ANONREVIEWERS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/AnonReviewer[0-9]+'

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
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=9, day=27, hour=9)
ADD_BID_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=5)
OFFICIAL_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=29)
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
            'values-regex': '|'.join(['~.*', CONFERENCE_ID])
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

questionnaire_instructions_invitation = openreview.Invitation.from_json({
    'id': CONFERENCE_ID + '/-/Reviewer_Questionnaire',
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {'values': [REVIEWERS_ID, AREA_CHAIRS_ID, PROGRAM_CHAIRS_ID, CONFERENCE_ID]},
        'writers': {'values': [CONFERENCE_ID]},
        'signatures': {'values': [CONFERENCE_ID]},
        'content': {
            'title': {'value': 'Questionnaire for Reviewers'},
            'Instructions': {
                'value': 'Help us get to know our reviewers better and the ways to make the reviewing process smoother by answering these questions. If you don\'t see the questionnaire form below, click on the blue "Reviewer Questionnaire Response" button below these instructions.',
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
    'duedate': OFFICIAL_REVIEW_DEADLINE,
    'expdate': OFFICIAL_REVIEW_DEADLINE,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {'values': [PROGRAM_CHAIRS_ID]},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {
                'value': 'Reviewer Questionnaire Response',
                'order': 1,
                'required': True
            },
            'Confirm Profile Updated': {
                'description': 'Have you updated your OpenReview profile to include your most up-to-date relations, work history, and conflicts of interest?',
                'value-radio': ['Yes', 'No'],
                'order': 2,
                'required': True
            },
            'Confirm TPMS Registration': {
                'description': 'Have you registered and/or updated your TPMS account, and updated your OpenReview profile to include the email address you used for TPMS?',
                'value-radio': ['Yes', 'No'],
                'order': 3,
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
                'order': 4,
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
                'order': 5,
                'required': True

            },
            'Previous ICLR Author': {
                'description': 'Have you published at ICLR in the last two years?',
                'value-radio': ['Yes','No'],
                'order': 6,
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
                'order': 7,
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
                'order': 8,
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

# Configure AC recommendations
ac_recommendation_template = {
        'id': CONFERENCE_ID + '/-/Paper<number>/Recommend_Reviewer',
        'invitees': [],
        'multiReply': True,
        'readers': ['everyone'],
        'writers': [CONFERENCE_ID],
        'signatures': [CONFERENCE_ID],
        'duedate': openreview.tools.timestamp_GMT(year=2018, month=6, day=6),
        'reply': {
            'forum': '<forum>',
            'replyto': '<forum>',
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values-copied': [
                    # CONFERENCE_ID, //seems like we can get rid of this for now
                    '{signatures}'
                ]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': '~.*'
            },
            'content': {
                'tag': {
                    'description': 'Recommend a reviewer to review this paper',
                    'order': 1,
                    'required': True,
                    'values-url': '/groups?id=' + REVIEWERS_ID
                }
            }
        }
    }

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
                PROGRAM_CHAIRS_ID
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
        'readers': {'values': [CONFERENCE_ID]},
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


# Per-paper group template definitions
papergroup_template = openreview.Group.from_json({
    'id': PAPER_TEMPLATE_STR,
    'readers':[CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})


reviewers_template = openreview.Group.from_json({
    'id': PAPER_REVIEWERS_TEMPLATE_STR,
    'readers':[
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

area_chairs_template = openreview.Group.from_json({
    'id': PAPER_REVIEWERS_TEMPLATE_STR,
    'readers':[
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

review_nonreaders_template = openreview.Group.from_json({
    'id': PAPER_REVIEW_NONREADERS_TEMPLATE_STR,
    'readers':[
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

comment_nonreaders_template = openreview.Group.from_json({
    'id': PAPER_COMMENT_NONREADERS_TEMPLATE_STR,
    'readers':[
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_unsubmitted_template = openreview.Group.from_json({
    'id': PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR,
    'readers':[
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID,
        PAPER_AREA_CHAIRS_TEMPLATE_STR
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_submitted_template = openreview.Group.from_json({
    'id': PAPER_REVIEWERS_SUBMITTED_TEMPLATE_STR,
    'readers':[
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID,
        PAPER_AREA_CHAIRS_TEMPLATE_STR
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})


# Configure the invitations that will be attached on a per-paper basis
# These are constructed using templates.
official_comment_template = {
    'id': OFFICIAL_COMMENT_TEMPLATE_STR,
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': [
        PAPER_REVIEWERS_TEMPLATE_STR,
        PAPER_AUTHORS_TEMPLATE_STR,
        PAPER_AREA_CHAIRS_TEMPLATE_STR,
        PROGRAM_CHAIRS_ID
    ],
    'noninvitees': [PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR],
    'signatures': [CONFERENCE_ID],
    'process': os.path.abspath('../process/commentProcess.js'),
    # 'multiReply': True,
    'multiReply': None,
    'reply': {
        'forum': '<forum>',
        'replyto': None,
        'readers': {
            'description': 'Select all user groups that should be able to read this comment.',
            'values-dropdown': [
                'everyone',
                PAPER_AUTHORS_TEMPLATE_STR,
                PAPER_REVIEWERS_TEMPLATE_STR,
                PAPER_AREA_CHAIRS_TEMPLATE_STR,
                PROGRAM_CHAIRS_ID
            ]
        },
        'nonreaders': {
            'values': [PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': '',
            'values-regex': '|'.join([
                PAPER_ANONREVIEWERS_TEMPLATE_REGEX,
                PAPER_AUTHORS_TEMPLATE_STR,
                PAPER_AREA_CHAIRS_TEMPLATE_REGEX,
                PROGRAM_CHAIRS_ID,
            ]),
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                CONFERENCE_ID,
                '{signatures}'
            ]
        },
        'content': invitations.content.comment
    }
}

official_review_template = {
    'id': OFFICIAL_REVIEW_TEMPLATE_STR,
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': [PAPER_REVIEWERS_TEMPLATE_STR],
    'noninvitees': [PAPER_REVIEWERS_SUBMITTED_TEMPLATE_STR],
    'signatures': [CONFERENCE_ID],
    'duedate': OFFICIAL_REVIEW_DEADLINE,
    'process': os.path.abspath('../process/officialReviewProcess.js'),
    # 'multiReply': False,
    'multiReply': None,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': ['everyone']
        },
        'nonreaders': {
            'values': [PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': PAPER_ANONREVIEWERS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                CONFERENCE_ID,
                '{signatures}'
            ]
        },
        'content': invitations.content.review
    }
}

review_rating_template = {
    'id': CONFERENCE_ID + '/-/Paper<number>/Review_Rating',
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': [PAPER_REVIEWERS_TEMPLATE_STR],
    'noninvitees': [PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR],
    'signatures': [CONFERENCE_ID],
    'duedate': OFFICIAL_REVIEW_DEADLINE,
    'process': None,
    # 'multiReply': True,
    'multiReply': None,
    'reply': {
        'forum': '<forum>',
        'replyto': None,
        'invitation': OFFICIAL_REVIEW_TEMPLATE_STR,
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': ['everyone']
        },
        'nonreaders': {
            'values': [PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': PAPER_ANONREVIEWERS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                '{signatures}'
            ]
        },
        'content': invitations.content.review_rating
    }
}

meta_review_template = {
    'id': CONFERENCE_ID + '/-/Paper<number>/Meta_Review',
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': [PAPER_AREA_CHAIRS_TEMPLATE_STR],
    'noninvitees': [],
    'signatures': [CONFERENCE_ID],
    'duedate': META_REVIEW_DEADLINE,
    'process': os.path.join(os.path.dirname(__file__), '../process/metaReviewProcess.js'),
    # 'multiReply': False,
    'multiReply': None,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {
            'description': 'Select all user groups that should be able to read this comment. Selecting \'All Users\' will allow paper authors, reviewers, area chairs, and program chairs to view this comment.',
            'values': [
                PAPER_AREA_CHAIRS_TEMPLATE_STR,
                PROGRAM_CHAIRS_ID
            ]

        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': PAPER_AREA_CHAIRS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-regex': PAPER_AREA_CHAIRS_TEMPLATE_REGEX
        },
        'content': invitations.content.review
    }
}

add_revision_template = {
    'id': CONFERENCE_ID + '/-/Paper<number>/Add_Revision',
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'invitees': [CONFERENCE_ID + '/Paper<number>/Authors'],
    'signatures': [CONFERENCE_ID],
    # 'multiReply': True,
    'multiReply': None,
    'reply': {
        'referent': '<forum>',
        'forum': '<forum>',
        'content': submission_inv.reply['content'],
        'signatures': submission_inv.reply['signatures'],
        'writers': submission_inv.reply['writers'],
        'readers': submission_inv.reply['readers']
    }

}

