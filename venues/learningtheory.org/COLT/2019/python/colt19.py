'''
COLT 2019 demo configuration
http://learningtheory.org/colt2019/
June 25 - 28

SUBMISSION DEADLINE Feb. 1, 11pm PST
AUTHOR FEEDBACK Mar. 22-27
AUTHORS NOTIFICATION Apr. 17

'''

import openreview
from openreview import invitations
import os

# group ids
CONFERENCE_ID = 'learningtheory.org/COLT/2019'
SHORT_PHRASE = 'COLT 2019'

PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'

PROGRAM_COMMITTEE_ID = CONFERENCE_ID + '/Program_Committee'
REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'

AUTHORS_ID = CONFERENCE_ID + '/Authors'

# invitation ids
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission'

# template strings
PAPER_TEMPLATE_STR = CONFERENCE_ID + '/Paper<number>'
PAPER_REVIEWERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Reviewers'
PAPER_AREA_CHAIRS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Area_Chairs'
PAPER_AUTHORS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Authors'
PAPER_REVIEW_NONREADERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Review_Nonreaders'
PAPER_COMMENT_NONREADERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Comment_Nonreaders'

PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR = PAPER_REVIEWERS_TEMPLATE_STR + '/Unsubmitted'
PAPER_REVIEWERS_SUBMITTED_TEMPLATE_STR = PAPER_REVIEWERS_TEMPLATE_STR + '/Submitted'

OFFICIAL_COMMENT_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Comment'
OFFICIAL_REVIEW_TEMPLATE_STR = CONFERENCE_ID + '/-/Paper<number>/Official_Review'

# The groups corresponding to these regexes will get automatically created upon assignment
PAPER_AREA_CHAIRS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/Area_Chair[0-9]+'
PAPER_ANONREVIEWERS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/AnonReviewer[0-9]+'

# Email templates

# Deadlines
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=2, day=2, hour=6) # Feb 2, 6am GMT == Feb 1, 11pm PST
ADD_BID_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=3, day=27)
OFFICIAL_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=3, day=27)
META_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=10, day=27)



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

program_committee = openreview.Group.from_json({
    'id': PROGRAM_COMMITTEE_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, PROGRAM_COMMITTEE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': []
})
with open(os.path.abspath('../webfield/programCommitteeWebfield.js')) as f:
    program_committee.web = f.read()

reviewers = openreview.Group.from_json({
    'id': REVIEWERS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, PROGRAM_COMMITTEE_ID, REVIEWERS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})
with open(os.path.abspath('../webfield/reviewerWebfield.js')) as f:
    reviewers.web = f.read()

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
                PROGRAM_CHAIRS_ID,
                PROGRAM_COMMITTEE_ID,
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
            PROGRAM_COMMITTEE_ID
        ],
        'invitees': [],
        'web': os.path.abspath('../webfield/bidWebfield.js')
    },
    # content_params = {
    #     'tag': {
    #         'description': 'Bid description',
    #         'order': 1,
    #         'value-radio': [
    #             'Very High',
    #             'High',
    #             'Neutral',
    #             'Low',
    #             'Very Low',
    #             'Conflict'
    #         ],
    #         'required': True
    #     }
    # }
)

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

