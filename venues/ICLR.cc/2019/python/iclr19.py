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

REVIEWER_METADATA_ID = CONFERENCE_ID + '/-/Reviewer_Metadata'
AREA_CHAIR_METADATA_ID = CONFERENCE_ID + '/-/Area_Chair_Metadata'

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

You have been invited to serve as a reviewer for the ICLR 2019 Conference.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

We  hope you will be able to accept our invitation and help us select a high quality program for ICLR 2019.

Best regards,
The ICLR 2019 Program Chairs

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
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=9, day=1)
ADD_BID_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=9, day=7)
OFFICIAL_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=8, day=1)
META_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=9, day=24)



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
    'readers': [CONFERENCE_ID, PROGRAM_CHAIRS_ID, AUTHORS_ID],
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
            'values-regex': '|'.join(['~.*', CONFERENCE_ID])
        }
    },
    content_params = {
        'subject areas': {'required': True, 'values-dropdown': subject_areas}
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
    web = os.path.abspath('../webfield/recruitResponseWebfield.js')
)

subj_desc = ''.join([
    'To properly assign papers to reviewers, we ask that reviewers provide their areas ',
    'of expertise from among the provided list of subject areas. ',
    'Please submit your areas of expertise by clicking on the "Subject Areas" button below.',
    '\n\n'
    ])

coi_desc = ''.join([
    'In order to avoid conflicts of interest in reviewing, we ask that all reviewers take a moment to ',
    'update their OpenReview profiles with their latest information regarding work history and professional relationships. ',
    'After you have updated your profile, please confirm that your profile is up-to-date by clicking on ',
    'the "Profile Confirmed" button below.',
    '\n\n'
    ])

data_consent_desc = ''.join([
    'One of the missions of OpenReview is to enable the study of the scientific peer review process itself. ',
    'In accordance with that mission, OpenReview is collecting a dataset of peer reviews and ',
    'discussions between authors and reviewers for research purposes. ',
    'This dataset will include the contents of peer reviews and comments between authors, reviewers, and area chairs. ',
    'The dataset will be anonymized, and will not include your true identity, but may include non-identifiable metadata related to your profile (e.g. years of experience, field of expertise). ',
    'The dataset may be released to the public domain ',
    'after the final accept/reject decisions are made. ',
    'Do you agree to having your reviews and comments included in this dataset? ',
    'Please indicate your response by clicking on the "Consent Response" button below. ',
    '\n\n'
    ])

tpms_desc = ''.join([
    'In addition to subject areas, we will be using the Toronto Paper Matching System (TPMS) to compute paper-reviewer affinity scores. ',
    'Please take a moment to sign up for TPMS and/or update your TPMS account with your latest papers. ',
    'Then, please ensure that the email address that is affiliated with your TPMS account is linked to your OpenReview profile. ',
    'After you have done this, please confirm that your TPMS account is up-to-date by clicking the "TPMS Account Confirmed" button below. ',
    '\n\n'
    ])

registration_root_invitation = openreview.Invitation.from_json({
    'id': CONFERENCE_ID + '/-/Reviewer_Registration',
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
            'title': {'value': 'ICLR 2019 Reviewer Registration'},
            'Subject Areas': {
                'value': subj_desc,
                'order': 1
            },
            'Profile Confirmed': {
                'value': coi_desc,
                'order': 2
            },
            'Consent Response': {
                'value': data_consent_desc,
                'order': 9
            }
        }
    }
})

registration_root_note = openreview.Note.from_json({
    'readers': registration_root_invitation.reply['readers']['values'],
    'writers': registration_root_invitation.reply['writers']['values'],
    'signatures': registration_root_invitation.reply['signatures']['values'],
    'invitation': registration_root_invitation.id,
    'content': {
        'title': registration_root_invitation.reply['content']['title']['value'],
        'Subject Areas': registration_root_invitation.reply['content']['Subject Areas']['value'],
        'Profile Confirmed': registration_root_invitation.reply['content']['Profile Confirmed']['value'],
        'Consent Response': registration_root_invitation.reply['content']['Consent Response']['value'],
    }
})

consent_response_template = {
    'id': CONFERENCE_ID + '/-/Registration/Consent/Response', # I would like for this to be Consent_Response, but right now the prettyId function is taking the last TWO segments. It should only take the last.
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [REVIEWERS_ID],
    'duedate': 1520639999000, # March 9, 2018
    'process': '../process/registrationProcess.js',
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {'values': [CONFERENCE_ID]},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {
                'value': 'Consent Form Response',
                'order': 1
            },
            'consent': {
                'value-dropdown': [
                    'Yes, I agree to participate.',
                    'No, I do not agree to participate.'
                ],
                'required': True,
                'order': 2
            }
        }
    }
}

subj_response_template = {
    'id': CONFERENCE_ID + '/-/Registration/Subject/Areas', # same here, see comment above
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [REVIEWERS_ID],
    'duedate': 1520639999000, # March 9, 2018,
    'process': '../process/registrationProcess.js',
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {'values': [CONFERENCE_ID]},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {
                'value': 'Subject Area Response',
                'order': 1
            },
            'subject_areas': {
                'values-dropdown': subject_areas,
                'required': True,
                'order': 2
            }
        }
    }
}

profile_confirmed_template = {
    'id': CONFERENCE_ID + '/-/Registration/Profile/Confirmed',
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [REVIEWERS_ID],
    'duedate': 1520639999000, # March 9, 2018,
    'process': '../process/registrationProcess.js',
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {'values': [CONFERENCE_ID]},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {
                'value': 'Profile Confirmed Response',
                'order': 1
            },
            'confirmation': {
                'value': 'I confirm that I have updated my profile sufficiently to capture my conflicts of interest.',
                'required': True,
                'order': 2
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

# add_wager = invitations.AddWager(
#     conference_id = CONFERENCE_ID,
#     duedate = ADD_BID_DEADLINE,
#     completion_count = 50,
#     inv_params = {
#         'readers': [
#             CONFERENCE_ID,
#             PROGRAM_CHAIRS_ID,
#             REVIEWERS_ID,
#             AREA_CHAIRS_ID
#         ],
#         'invitees': [],
#         'web': os.path.abspath('../webfield/bidWebfield.js')
#     }
# )


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
                'values-copied': [CONFERENCE_ID, '{signatures}']
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


# Metadata and matching stuff
reviewer_metadata = openreview.Invitation.from_json({
    'id': REVIEWER_METADATA_ID,
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
        'readers': {'values': [CONFERENCE_ID]},
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
            'description': 'Select all user groups that should be able to read this comment. Selecting \'All Users\' will allow paper authors, reviewers, area chairs, and program chairs to view this comment.',
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
        # 'invitation': OFFICIAL_REVIEW_TEMPLATE_STR,
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
            'values': [CONFERENCE_ID, PAPER_AREA_CHAIRS_TEMPLATE_STR, PROGRAM_CHAIRS_ID]

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

