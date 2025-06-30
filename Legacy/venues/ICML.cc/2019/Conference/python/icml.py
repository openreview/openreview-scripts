'''
ICML 2019 demo configuration
https://icml.cc/Conferences/2019
Monday June 10 - Saturday June 15, 2019
'''

import openreview
from openreview import invitations
import os

# group ids
CONFERENCE_ID = 'ICML.cc/2019/Conference'
SHORT_PHRASE = 'ICML 2019'

PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'
AREA_CHAIRS_ID = CONFERENCE_ID + '/Area_Chairs'
SENIOR_AREA_CHAIRS_ID = CONFERENCE_ID + '/Senior_Area_Chairs'
EXPERT_REVIEWERS_ID = CONFERENCE_ID + '/Expert_Reviewers'
REVIEWERS_ID = CONFERENCE_ID + '/Reviewers'

# invitation ids
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
BLIND_SUBMISSION_ID = CONFERENCE_ID + '/-/Blind_Submission'

RECRUIT_AREA_CHAIRS_ID = CONFERENCE_ID + '/-/Recruit_Area_Chairs'
RECRUIT_REVIEWERS_ID = CONFERENCE_ID + '/-/Recruit_Reviewers'

METADATA_ID = CONFERENCE_ID + '/-/Paper_Metadata'

# template strings
PAPER_TEMPLATE_STR = CONFERENCE_ID + '/Paper<number>'
PAPER_REVIEWERS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Reviewers'
PAPER_AREA_CHAIRS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Area_Chairs'
PAPER_AUTHORS_TEMPLATE_STR = PAPER_TEMPLATE_STR + '/Authors'

# The groups corresponding to these regexes will get automatically created upon assignment
PAPER_AREA_CHAIRS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/Area_Chair[0-9]+'
PAPER_ANONREVIEWERS_TEMPLATE_REGEX = PAPER_TEMPLATE_STR + '/AnonReviewer[0-9]+'


# Deadlines
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=7, day=1)
ADD_BID_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=7, day=7)
OFFICIAL_REVIEW_DEADLINE = openreview.tools.timestamp_GMT(year=2018, month=7, day=14)



# Global group definitions
conference = openreview.Group(**{
    'id': CONFERENCE_ID,
    'readers':['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [],
    'signatories': [CONFERENCE_ID],
    'members': [],
    'web': os.path.abspath('../webfield/homepage.js')
})

program_chairs = openreview.Group(**{
    'id': PROGRAM_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [],
    'signatures': [],
    'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'members': [],
    'web': os.path.abspath('../webfield/programchairWebfield.js')
})

area_chairs = openreview.Group(**{
    'id': AREA_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, AREA_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
    'web': os.path.abspath('../webfield/areachairWebfield.js')
})

senior_area_chairs = openreview.Group(**{
    'id': SENIOR_AREA_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, SENIOR_AREA_CHAIRS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': []
})


reviewers = openreview.Group(**{
    'id': REVIEWERS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, AREA_CHAIRS_ID, REVIEWERS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

expert_reviewers = openreview.Group(**{
    'id': EXPERT_REVIEWERS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID, AREA_CHAIRS_ID, EXPERT_REVIEWERS_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

# Configure paper submissions
submission_inv = invitations.Submission(
    id = SUBMISSION_ID,
    conference_id = CONFERENCE_ID,
    duedate = SUBMISSION_DEADLINE,
    reply_params = {
        'readers': {
            'values-regex': '|'.join(['~.*', CONFERENCE_ID + '.*'])
        },
        'signatures': {
            'values-regex': '|'.join(['~.*', CONFERENCE_ID])
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
        'title': {
            'values-regex': '.*',
            'required': False,
        },
        'abstract': {
            'values-regex': '.*',
            'required': False
        },
        'authors': {
            'values': ['Anonymous']
        },
        'authorids': {
            'values': ['Anonymous']
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

jrac_placeholder_inv = invitations.Submission(
    id = 'ICML.cc/2019/Conference/-/JrAC_Placeholder',
    conference_id = CONFERENCE_ID,
    duedate = SUBMISSION_DEADLINE,
    reply_params = {
        'readers': {
            'values-regex': '|'.join(['~.*', CONFERENCE_ID + '.*'])
        },
        'signatures': {
            'values-regex': '|'.join(['~.*', CONFERENCE_ID])
        },
        'writers': {
            'values-regex': '|'.join(['~.*', CONFERENCE_ID])
        }
    }
)
jrac_placeholder_inv.reply['content'] = {
    'title': {
        'value-regex': '~.*'
    }
}


# Configure bidding
bid_inv = openreview.Invitation(**{
    'id': 'ICML.cc/2019/Conference/-/Bid',
    'readers': ['everyone'],
    'writers': ['ICML.cc/2019/Conference'],
    'signatures': ['ICML.cc/2019/Conference'],
    'invitees': [AREA_CHAIRS_ID],
    'multiReply': True,
    'expdate': 1549038307000,
    'duedate': 1549038307000,
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'ICML.cc/2019/Conference/-/Blind_Submission',
        'readers': {
            'values': [
                'ICML.cc/2019/Conference'
            ]
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': {
            'tag': {
                'values-radio': [
                  'Very High',
                  'High',
                  'Neutral',
                  'Low',
                  'Very Low',
                  'No Bid'
                ]
            }
        }
    },
    'web': os.path.abspath('../webfield/bidWebfield.js')
})

# Configure bidding
sac_bid_inv = openreview.Invitation(**{
    'id': 'ICML.cc/2019/Conference/-/SAC_Bid',
    'readers': ['everyone'],
    'writers': ['ICML.cc/2019/Conference'],
    'signatures': ['ICML.cc/2019/Conference'],
    'invitees': ['OpenReview.net'],
    'multiReply': True,
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'ICML.cc/2019/Conference/-/JrAC_Placeholder',
        'readers': {
            'values': [
                'ICML.cc/2019/Conference'
            ]
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': {
            'tag': {
                'values-radio': [
                    '1 - Not Willing',
                    '2 - Neutral',
                    '3 - Willing',
                    '4 - Eager'
                ]
            }
        }
    }
})

scores_by_bid = {
    '1 - Not Willing': -1.0,
    '2 - Neutral': 0,
    '3 - Willing': 0.5,
    '4 - Eager': 1.0
}

bids_by_score = {
    -1.0: '1 - Not Willing',
    0: '2 - Neutral',
    0.5: '3 - Willing',
    1.0: '4 - Eager'
}

# Metadata and matching stuff
metadata_inv = openreview.Invitation(**{
    'id': METADATA_ID,
    'readers': [
        CONFERENCE_ID,
        AREA_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'invitees': [],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': BLIND_SUBMISSION_ID,
        'readers': {
            'values': [
                CONFERENCE_ID,
                AREA_CHAIRS_ID
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

# Metadata and matching stuff
jrac_metadata_inv = openreview.Invitation(**{
    'id': 'ICML.cc/2019/Conference/-/JrAC_Metadata',
    'readers': [
        CONFERENCE_ID
    ],
    'writers': [CONFERENCE_ID],
    'invitees': [],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'ICML.cc/2019/Conference/-/JrAC_Placeholder',
        'readers': {
            'values': [
                CONFERENCE_ID
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

assignment_inv = openreview.Invitation(**{
    'id': ASSIGNMENT_INV_ID,
    'readers': [CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': BLIND_SUBMISSION_ID,
        'readers': {
            'values': [
                'ICML.cc/2019/Conference',
                'ICML.cc/2019/Conference/Area_Chairs'
            ]
        },
        'writers': {
            'values': [CONFERENCE_ID]
        },
        'signatures': {
            'values': [CONFERENCE_ID]
        },
        'content': {}
    }
})

CONFIG_INV_ID = CONFERENCE_ID + '/-/Assignment_Configuration'

config_inv = openreview.Invitation(**{
    'id': CONFIG_INV_ID,
    'readers': [CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'invitees': [],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': None,
        'readers': {
            'values': [CONFERENCE_ID, AREA_CHAIRS_ID]
        },
        'writers': {
            'values': [CONFERENCE_ID]
        },
        'signatures': {
            'values': [CONFERENCE_ID]
        },
        'content': {
            'label': {
                'value-regex': '.{1,250}',
                'required': True,
                'description': 'Title of the configuration.',
                'order': 1
            },
            'max_users': {
                'value-regex': '[0-9]+',
                'required': True,
                'description': 'Max number of reviewers that can review a paper',
                'order': 2
            },
            'min_users': {
                'value-regex': '[0-9]+',
                'required': True,
                'description': 'Min number of reviewers required to review a paper',
                'order': 3
            },
            'max_papers': {
                'value-regex': '[0-9]+',
                'required': True,
                'description': 'Max number of reviews a person has to do',
                'order': 4
            },
            'min_papers': {
                'value-regex': '[0-9]+',
                'required': True,
                'description': 'Min number of reviews a person should do',
                'order': 5
            },
            'alternates': {
                'value-regex': '[0-9]+',
                'required': True,
                'description': 'Number of alternate reviewers for a paper',
                'order': 6
            },
            'config_invitation': {
                'value-regex': 'ICML.cc/2019/Conference/-/Assignment_Configuration',
                'required': True,
                'description': 'Invitation to get the configuration note',
                'order': 7
            },
            'paper_invitation': {
                'value-regex': 'ICML.cc/2019/Conference/.*',
                'required': True,
                'description': 'Invitation to get the configuration note',
                'order': 8
            },
            'metadata_invitation': {
                'value-regex': 'ICML.cc/2019/Conference/-/.*',
                'required': True,
                'description': 'Invitation to get the configuration note',
                'order': 9
            },
            'assignment_invitation': {
                'value': 'ICML.cc/2019/Conference/-/Paper_Assignment',
                'required': True,
                'description': 'Invitation to get the configuration note',
                'order': 10
            },
            'constraints_invitation': {
                'value': 'ICML.cc/2019/Conference/-/Assignment_Configuration/Lock',
                'required': True,
                'description': 'Invitation to get the configuration note',
                'order': 10
            },
            'match_group': {
                'value-regex': 'ICML.cc/2019/Conference/.*',
                'required': True,
                'description': 'Invitation to get the configuration note',
                'order': 11
            },
            'scores_names': {
                'values-dropdown': [
                    'affinity',
                    'bid',
                    'subjectArea',
                    'recommendation'
                ],
                'required': True,
                'description': 'List of scores names',
                'order': 12
            },
            'scores_weights': {
                'values-regex': '\\d*\\.?\\d*',
                'required': True,
                'description': 'Comma separated values of scores weigths, should follow the same order than scores_names',
                'order': 13
            },
            'status': {
                'value-dropdown': [
                    'Initialized',
                    'Running',
                    'Error',
                    'Failure',
                    'Complete',
                    'Deployed'
                ]
                }
            }
        }
    }
)

lock_tag_inv = openreview.Invitation(**{
    'id': 'ICML.cc/2019/Conference/-/Assignment_Configuration/Lock',
    'readers': ['everyone'],
    'writers': ['ICML.cc/2019/Conference'],
    'signatures': ['ICML.cc/2019/Conference'],
    'invitees': ['~'],
    'multiReply': True,
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'ICML.cc/2019/Conference/-/Blind_Submission',
        'readers': {
            'values': [
                'ICML.cc/2019/Conference/Area_Chairs',
                'ICML.cc/2019/Conference'
            ]
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': {
            'tag': {
                'value-regex': '.*'
            }
        }
    }
})

# Per-paper group template definitions
papergroup_template = openreview.Group(**{
    'id': PAPER_TEMPLATE_STR,
    'readers':[CONFERENCE_ID],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})

reviewers_template = openreview.Group(**{
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

area_chairs_template = openreview.Group(**{
    'id': PAPER_AREA_CHAIRS_TEMPLATE_STR,
    'readers':[
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': [],
})
