#!/usr/bin/python

"""
A script for managing invitations with parameters that depend on the papers to which
they are attached.

Usage:

python invitations.py Official_Comment --enable
python invitations.py Official_Comment --disable
"""

import openreview
import argparse
import akbc19 as conference_config
import os
import time

change_archival_status_template = {
    'id': conference_config.CONFERENCE_ID + '/-/Paper<number>/Change_Archival_Status',
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [conference_config.CONFERENCE_ID + '/Paper<number>/Authors'],
    'signatures': [conference_config.CONFERENCE_ID],
    'multiReply': None,
    'reply': {
        'referent': '<original>',
        'forum': '<original>',
        'content': {'archival status' : conference_config.submission_inv.reply['content']['archival status']},
        'signatures': conference_config.submission_inv.reply['signatures'],
        'writers': conference_config.submission_inv.reply['writers'],
        'readers': conference_config.submission_inv.reply['readers']
    }
}

official_review_template = {
    'id': conference_config.OFFICIAL_REVIEW_TEMPLATE_STR,
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [conference_config.PAPER_REVIEWERS_TEMPLATE_STR],
    'noninvitees': [],
    'signatures': [conference_config.CONFERENCE_ID],
    'duedate': conference_config.OFFICIAL_REVIEW_DEADLINE,
    'multiReply': False,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': [
                conference_config.PROGRAM_CHAIRS_ID,
                conference_config.PAPER_AREA_CHAIRS_TEMPLATE_STR,
                conference_config.PAPER_REVIEWERS_TEMPLATE_STR,
                '~'
                ]
        },
        'nonreaders': {
            'values': [conference_config.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': conference_config.PAPER_ANONREVIEWERS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                conference_config.CONFERENCE_ID,
                '{signatures}'
            ]
        },
        'content': openreview.invitations.content.review
    }
}
with open(os.path.abspath('../process/officialReviewProcess.js')) as f:
    official_review_template['process'] = f.read()

revise_review_template = {
    'id': conference_config.CONFERENCE_ID + '/-/<reviewer_id>/Revise/Review',
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [], # this needs to be filled in manually on a per-reviewer basis
    'signatures': [conference_config.CONFERENCE_ID],
    'multiReply': None,
    'reply': {
        'referent': None, # this needs to be filled in manually on a per-reviewer basis
        'forum': '<forum>',
        'content': openreview.invitations.content.review,
        'signatures': official_review_template['reply']['signatures'],
        'writers': official_review_template['reply']['writers'],
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': ['everyone']
        }
    }
}

review_rating_template = {
    'id': conference_config.CONFERENCE_ID + '/-/Paper<number>/Review_Rating',
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [conference_config.PAPER_REVIEWERS_TEMPLATE_STR],
    'noninvitees': [conference_config.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR],
    'signatures': [conference_config.CONFERENCE_ID],
    'duedate': conference_config.OFFICIAL_REVIEW_DEADLINE,
    'process': None,
    'multiReply': None,
    'reply': {
        'forum': '<forum>',
        'replyto': None,
        'invitation': conference_config.OFFICIAL_REVIEW_TEMPLATE_STR,
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': ['everyone']
        },
        'nonreaders': {
            'values': [conference_config.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': conference_config.PAPER_ANONREVIEWERS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                '{signatures}'
            ]
        },
        'content': openreview.invitations.content.review_rating
    }
}

meta_review_template = {
    'id': conference_config.CONFERENCE_ID + '/-/Paper<number>/Meta_Review',
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [conference_config.PAPER_AREA_CHAIRS_TEMPLATE_STR],
    'noninvitees': [],
    'signatures': [conference_config.CONFERENCE_ID],
    'duedate': conference_config.META_REVIEW_DEADLINE,
    'multiReply': False,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {
            'description': 'Select all user groups that should be able to read this comment. Selecting \'All Users\' will allow paper authors, reviewers, area chairs, and program chairs to view this comment.',
            'values': [
                conference_config.PAPER_AREA_CHAIRS_TEMPLATE_STR,
                conference_config.PROGRAM_CHAIRS_ID
            ]

        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': conference_config.PAPER_AREA_CHAIRS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-regex': conference_config.PAPER_AREA_CHAIRS_TEMPLATE_REGEX
        },
        'content': openreview.invitations.content.meta_review
    }
}
with open(os.path.join(os.path.dirname(__file__), '../process/metaReviewProcess.js')) as f:
    meta_review_template['process'] = f.read()

add_revision_template = {
    'id': conference_config.CONFERENCE_ID + '/-/Paper<number>/Add_Revision',
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [conference_config.CONFERENCE_ID + '/Paper<number>/Authors'],
    'signatures': [conference_config.CONFERENCE_ID],
    'multiReply': None,
    'reply': {
        'referent': '<original>',
        'forum': '<original>',
        'content': conference_config.submission_inv.reply['content'],
        'signatures': conference_config.submission_inv.reply['signatures'],
        'writers': conference_config.submission_inv.reply['writers'],
        'readers': conference_config.submission_inv.reply['readers']
    }
}

official_comment_template = {
    'id': conference_config.OFFICIAL_COMMENT_TEMPLATE_STR,
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [
        conference_config.PAPER_REVIEWERS_TEMPLATE_STR,
        conference_config.PAPER_AUTHORS_TEMPLATE_STR,
        conference_config.PAPER_AREA_CHAIRS_TEMPLATE_STR,
        conference_config.PROGRAM_CHAIRS_ID
    ],
    # 'noninvitees': [conference_config.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR],
    'signatures': [conference_config.CONFERENCE_ID],
    'multiReply': True,
    'reply': {
        'forum': '<forum>',
        'replyto': None,
        'readers': {
            'description': 'Select all user groups that should be able to read this comment.',
            'value-dropdown-hierarchy': [
                'everyone',
                conference_config.PAPER_AUTHORS_TEMPLATE_STR,
                conference_config.PAPER_REVIEWERS_TEMPLATE_STR,
                conference_config.PAPER_AREA_CHAIRS_TEMPLATE_STR,
                conference_config.PROGRAM_CHAIRS_ID
            ]
        },
        'nonreaders': {
            'values': [conference_config.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': '',
            'values-regex': '|'.join([
                conference_config.PAPER_ANONREVIEWERS_TEMPLATE_REGEX,
                conference_config.PAPER_AUTHORS_TEMPLATE_STR,
                conference_config.PAPER_AREA_CHAIRS_TEMPLATE_REGEX,
                conference_config.PROGRAM_CHAIRS_ID,
            ]),
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                conference_config.CONFERENCE_ID,
                '{signatures}'
            ]
        },
        'content': openreview.invitations.content.comment
    }
}
with open(os.path.abspath('../process/commentProcess.js')) as f:
    official_comment_template['process'] = f.read()

public_comment_template = {
    'id': conference_config.PUBLIC_COMMENT_TEMPLATE_STR,
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': ['~'],
    'noninvitees': [
        conference_config.PAPER_AUTHORS_TEMPLATE_STR,
        conference_config.PAPER_REVIEWERS_TEMPLATE_STR,
        conference_config.PAPER_AREA_CHAIRS_TEMPLATE_STR,
        conference_config.PROGRAM_CHAIRS_ID
    ],
    'signatures': [conference_config.CONFERENCE_ID],
    'multiReply': True,
    'reply': {
        'forum': '<forum>',
        'replyto': None,
        'readers': {
            'description': 'Select all user groups that should be able to read this comment.',
            'value-dropdown-hierarchy': [
                'everyone',
                conference_config.PAPER_AUTHORS_TEMPLATE_STR,
                conference_config.PAPER_REVIEWERS_TEMPLATE_STR,
                conference_config.PAPER_AREA_CHAIRS_TEMPLATE_STR,
                conference_config.PROGRAM_CHAIRS_ID
            ]
        },
        'nonreaders': {
            'values': [conference_config.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            "description": "How your identity will be displayed.",
            "values-regex": "~.*|\\(anonymous\\)"
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                conference_config.CONFERENCE_ID,
                '{signatures}'
            ]
        },
        'content': openreview.invitations.content.comment
    }
}
with open(os.path.abspath('../process/commentProcess.js')) as f:
    public_comment_template['process'] = f.read()

withdraw_submission_template = {
    'id': conference_config.CONFERENCE_ID + '/-/Paper<number>/Withdraw_Submission',
    'readers': ['everyone'],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [conference_config.CONFERENCE_ID + '/Paper<number>/Authors'],
    'signatures': [conference_config.CONFERENCE_ID],
    'multiReply': False,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {
            'description': 'Select all user groups that should be able to read this comment.',
            'values': ['everyone']
        },
        'signatures': {
            'description': '',
            'values-regex': conference_config.PAPER_AUTHORS_TEMPLATE_STR,
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values':  []
        },
        'content': {
            'title': {
                'value': 'Submission Withdrawn by the Authors',
                'order': 1
            },
            'withdrawal confirmation': {
                'description': conference_config.withdrawal_statement,
                'value-radio': ['I have read and agree with the withdrawal statement on behalf of myself and my co-authors.'],
                'order': 2,
                'required': True
            }
        }
    }
}
with open(os.path.abspath('../process/withdrawProcess.js')) as f:
    withdraw_submission_template['process'] = f.read()

invitation_templates = {
    'Add_Bid': conference_config.add_bid.to_json(),
    'Official_Comment': official_comment_template,
    'Add_Revision': add_revision_template,
    'Official_Review': official_review_template,
    'Meta_Review': meta_review_template,
    'Public_Comment': public_comment_template,
    'Withdraw_Submission': withdraw_submission_template,
    'Change_Archival_Status': change_archival_status_template
}

current_timestamp = lambda: int(round(time.time() * 1000))

def enable_invitation(template_key, target_paper=None):
    if target_paper:
        new_invitation = openreview.Invitation.from_json(
            openreview.tools.fill_template(invitation_templates[template_key], target_paper))
    else:
        new_invitation = openreview.Invitation.from_json(
            invitation_templates[template_key], target_paper)

    return new_invitation

def disable_invitation(template_key, target_paper=None):
    if target_paper:
        new_invitation = openreview.Invitation.from_json(
            openreview.tools.fill_template(invitation_templates[template_key], target_paper))
    else:
        new_invitation = openreview.Invitation.from_json(
            invitation_templates[template_key])

    new_invitation.expdate = current_timestamp()
    return new_invitation

def enable_and_post(client, paper, template_key):
    new_inv = enable_invitation(template_key, target_paper=paper)
    return client.post_invitation(new_inv)

def disable_bids(client):
    return client.post_invitation(disable_invitation('Add_Bid'))

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('invitations', nargs='*', help="any of the following: " + ", ".join(invitation_templates.keys()))
    parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    blind_submissions = openreview.tools.iterget_notes(client, invitation=conference_config.BLIND_SUBMISSION_ID)

    for paper in blind_submissions:
        for template in args.invitations:
            assert template in invitation_templates, 'invitation template not defined'
            if args.disable:
                new_invitation = disable_invitation(template, target_paper=paper)
            else:
                new_invitation = enable_invitation(template, paper)
            posted_invitation = client.post_invitation(new_invitation)
            print('posted new invitation {} to paper {}'.format(posted_invitation.id, paper.id))


