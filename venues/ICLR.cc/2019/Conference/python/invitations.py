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
import iclr19
import os

official_review_template = {
    'id': iclr19.OFFICIAL_REVIEW_TEMPLATE_STR,
    'readers': ['everyone'],
    'writers': [iclr19.CONFERENCE_ID],
    'invitees': [iclr19.PAPER_REVIEWERS_TEMPLATE_STR],
    'noninvitees': [iclr19.PAPER_REVIEWERS_SUBMITTED_TEMPLATE_STR],
    'signatures': [iclr19.CONFERENCE_ID],
    'duedate': iclr19.OFFICIAL_REVIEW_DEADLINE,
    'process': os.path.abspath('../process/officialReviewProcess.js'),
    'multiReply': False,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': ['everyone']
        },
        'nonreaders': {
            'values': [iclr19.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': iclr19.PAPER_ANONREVIEWERS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                iclr19.CONFERENCE_ID,
                '{signatures}'
            ]
        },
        'content': openreview.invitations.content.review
    }
}

review_rating_template = {
    'id': iclr19.CONFERENCE_ID + '/-/Paper<number>/Review_Rating',
    'readers': ['everyone'],
    'writers': [iclr19.CONFERENCE_ID],
    'invitees': [iclr19.PAPER_REVIEWERS_TEMPLATE_STR],
    'noninvitees': [iclr19.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR],
    'signatures': [iclr19.CONFERENCE_ID],
    'duedate': iclr19.OFFICIAL_REVIEW_DEADLINE,
    'process': None,
    'multiReply': None,
    'reply': {
        'forum': '<forum>',
        'replyto': None,
        'invitation': iclr19.OFFICIAL_REVIEW_TEMPLATE_STR,
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': ['everyone']
        },
        'nonreaders': {
            'values': [iclr19.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': iclr19.PAPER_ANONREVIEWERS_TEMPLATE_REGEX
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
    'id': iclr19.CONFERENCE_ID + '/-/Paper<number>/Meta_Review',
    'readers': ['everyone'],
    'writers': [iclr19.CONFERENCE_ID],
    'invitees': [iclr19.PAPER_AREA_CHAIRS_TEMPLATE_STR],
    'noninvitees': [],
    'signatures': [iclr19.CONFERENCE_ID],
    'duedate': iclr19.META_REVIEW_DEADLINE,
    'process': os.path.join(os.path.dirname(__file__), '../process/metaReviewProcess.js'),
    'multiReply': False,
    'reply': {
        'forum': '<forum>',
        'replyto': '<forum>',
        'readers': {
            'description': 'Select all user groups that should be able to read this comment. Selecting \'All Users\' will allow paper authors, reviewers, area chairs, and program chairs to view this comment.',
            'values': [
                iclr19.PAPER_AREA_CHAIRS_TEMPLATE_STR,
                iclr19.PROGRAM_CHAIRS_ID
            ]

        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': iclr19.PAPER_AREA_CHAIRS_TEMPLATE_REGEX
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-regex': iclr19.PAPER_AREA_CHAIRS_TEMPLATE_REGEX
        },
        'content': openreview.invitations.content.review
    }
}

add_revision_template = {
    'id': iclr19.CONFERENCE_ID + '/-/Paper<number>/Add_Revision',
    'readers': ['everyone'],
    'writers': [iclr19.CONFERENCE_ID],
    'invitees': [iclr19.CONFERENCE_ID + '/Paper<number>/Authors'],
    'signatures': [iclr19.CONFERENCE_ID],
    'multiReply': None,
    'reply': {
        'referent': '<forum>',
        'forum': '<forum>',
        'content': iclr19.submission_inv.reply['content'],
        'signatures': iclr19.submission_inv.reply['signatures'],
        'writers': iclr19.submission_inv.reply['writers'],
        'readers': iclr19.submission_inv.reply['readers']
    }

}

official_comment_template = {
    'id': iclr19.OFFICIAL_COMMENT_TEMPLATE_STR,
    'readers': ['everyone'],
    'writers': [iclr19.CONFERENCE_ID],
    'invitees': [
        iclr19.PAPER_REVIEWERS_TEMPLATE_STR,
        iclr19.PAPER_AUTHORS_TEMPLATE_STR,
        iclr19.PAPER_AREA_CHAIRS_TEMPLATE_STR,
        iclr19.PROGRAM_CHAIRS_ID
    ],
    'noninvitees': [iclr19.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR],
    'signatures': [iclr19.CONFERENCE_ID],
    'process': os.path.abspath('../process/commentProcess.js'),
    'multiReply': True,
    'reply': {
        'forum': '<forum>',
        'replyto': None,
        'readers': {
            'description': 'Select all user groups that should be able to read this comment.',
            'values-dropdown': [
                'everyone',
                iclr19.PAPER_AUTHORS_TEMPLATE_STR,
                iclr19.PAPER_REVIEWERS_TEMPLATE_STR,
                iclr19.PAPER_AREA_CHAIRS_TEMPLATE_STR,
                iclr19.PROGRAM_CHAIRS_ID
            ]
        },
        'nonreaders': {
            'values': [iclr19.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR]
        },
        'signatures': {
            'description': '',
            'values-regex': '|'.join([
                iclr19.PAPER_ANONREVIEWERS_TEMPLATE_REGEX,
                iclr19.PAPER_AUTHORS_TEMPLATE_STR,
                iclr19.PAPER_AREA_CHAIRS_TEMPLATE_REGEX,
                iclr19.PROGRAM_CHAIRS_ID,
            ]),
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [
                iclr19.CONFERENCE_ID,
                '{signatures}'
            ]
        },
        'content': openreview.invitations.content.comment
    }
}

invitation_templates = {
    'Official_Comment': official_comment_template,
    'Add_Revision': add_revision_template,
    'Official_Review': official_review_template,
}

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

    blind_submissions = openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID)

    for paper in blind_submissions:
        for template in args.invitations:
            assert template in invitation_templates, 'invitation template not defined'
            new_invitation = openreview.Invitation.from_json(
                openreview.tools.fill_template(invitation_templates[template], paper))
            if args.disable:
                new_invitation.invitees = []
            posted_invitation = client.post_invitation(new_invitation)
            print('posted new invitation {} to paper {}'.format(posted_invitation.id, paper.id))


