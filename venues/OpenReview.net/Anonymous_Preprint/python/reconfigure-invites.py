#!/usr/bin/python

import sys, os
import argparse
import openreview
import config
import datetime

# Changes in functionality - moves a bunch of process functions into super-invitations
# adds option to deanonymize, and add comments
# updates bibtex when revisions added

# This script expires previous versions of invitations
# creates super invitations
# changes the submissionProcess function.

"""

OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net.net)
    username - the email address of the logging in user
    password - the user's password

"""

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

# clear out previous version of invitations with /-/PaperN instead of /PaperN/-/
print("Removing old style invitations.")
now_ms = datetime.datetime.timestamp(datetime.datetime.now())*1000
invites = client.get_invitations(regex=config.CONF+"/-/Paper.*")
for invite in invites:
    invite.duedate = now_ms
    invite.expdate = now_ms
    client.post_invitation(invite)

print("Creating super invites.")
# parent Comment invite
super_comment = client.post_invitation(openreview.Invitation(
        id = config.CONF+'/-/Comment',
        signatures = [config.CONF],
        readers = ["everyone"],
        writers = [config.CONF],
        invitees = ["everyone"],
        reply = {
            "signatures": {
                "values-regex": "~.*",
                "description": "Your authorized identity to be associated with the above content."
            },
            "writers": {
                "values-copied": [config.CONF,"{signatures}"],
            },
            "readers": {
                "description": "The users who will be allowed to read the above content.",
                "values": ["everyone"]
            },
            "content": {
                'title': {
                    'order': 0,
                    'value-regex': '.{1,500}',
                    'description': 'Brief summary of your comment (max 500 characters).',
                    'required': True
                },
                'comment': {
                    'order': 1,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Your comment or reply (max 5000 characters).',
                    'required': True
                }
            }
        },
        process = "../process/commentProcess.js"
    ))

# parent Revision invite
submission_invite = client.get_invitation(id = config.CONF+"/-/Submission")
super_revision = client.post_invitation(openreview.Invitation(
        id = config.CONF+'/-/Revision',
        signatures = [config.CONF],
        readers = ["everyone"],
        writers = [config.CONF],
        reply = {
            "signatures": {
                "values-regex": "~.*|"+config.CONF,
                "description": "Your authorized identity to be associated with the above content."
            },
            "writers": {
                "values-copied": [config.CONF,"{signatures}"],
            },
            "readers": {
                "description": "The users who will be allowed to read the above content.",
                "values": ["everyone"]
            },
            "content": submission_invite.reply['content']
        },
        process = "../process/revisionProcess.py"
    ))

# parent Withdraw invite
super_withdraw = client.post_invitation(openreview.Invitation(
    id=config.CONF+'/-/Withdraw',
    signatures=[config.CONF],
    readers=["everyone"],
    writers=[config.CONF],
    reply={
        "signatures": {
            "values-regex": "~.*|"+config.CONF,
            "description": "Your authorized identity to be associated with the above content."
        },
        "writers": {
            "values-copied": [config.CONF, "{signatures}"],
        },
        "readers": {
            "description": "The users who will be allowed to read the above content.",
            "values-copied": [
                config.CONF,
                "{signatures}"
            ]
        },
        "content": {
            "title": {
                "value": "Submission Withdrawn by the Authors",
                "order": 1
            },
            "withdrawal_confirmation": {
                "description": "Please confirm to withdraw.",
                "value-radio": [
                    "I want to withdraw the anonymous submission on behalf of myself and my co-authors."
                ],
                "order": 2,
                "required": True
            }
        },

    },
    process="..//process/withdrawProcess.js"
))

# parent Reveal_Authors invite
super_reveal = client.post_invitation(openreview.Invitation(
    id=config.CONF+'/-/Reveal_Authors',
    signatures=[config.CONF],
    readers=["everyone"],
    writers=[config.CONF],
    reply={
        "signatures": {
            "values-regex": "~.*|"+config.CONF,
            "description": "Your authorized identity to be associated with the above content."
        },
        "writers": {
            "values-copied": [config.CONF, "{signatures}"],
        },
        "readers": {
            "description": "The users who will be allowed to read the above content.",
            "values-copied": [
                config.CONF,
                "{signatures}"
            ]
        },
        "content": {
            "title": {
                "value": "Reveal Submission Authors",
                "order": 1
            },
            "reveal_confirmation": {
                "description": "Please confirm to reveal authors.",
                "value-radio": [
                    "I want to reveal all author names on behalf of myself and my co-authors."
                ],
                "order": 2,
                "required": True
            }
        },

    },
    process="../process/revealProcess.py",
    multiReply=False,
))

# remake submission invite with updated submissionProcess
submission = client.post_invitation(openreview.Invitation(
    config.SUBMISSION, duedate=config.DUE_TIMESTAMP, **config.submission_params))

print("Updating current invitations.")
# update current invitations to refer to super invitations
notes = client.get_notes(invitation=config.CONF+'/-/Blind_Submission')
for note in notes:
    #comment
    comment_reply = {'forum':note.forum,
                     'signatures': {"values-regex": "~.*|"+config.CONF+"/Paper"+str(note.number)+"/Authors",
                                  "description": "How your identity will be displayed."}}
    comment_invite = client.post_invitation(openreview.Invitation(
            id = config.CONF+'/Paper'+str(note.number)+'/-/Comment',
            super = super_comment.id,
            signatures = [config.CONF],
            reply = comment_reply
    ))

    #revision
    revision_reply = {'forum': note.original, 'referent': note.original,
                      'signatures': {
                          "values-regex": config.CONF+"/Paper" + str(note.number) + "/Authors",
                          "description": "How your identity will be displayed."}}
    revision_invite = client.post_invitation(openreview.Invitation(
        id=config.CONF+'/Paper' + str(note.number) + '/-/Revision',
        super = super_revision.id,
        invitees=note.content['authorids'],
        signatures=[config.CONF],
        reply=revision_reply,
    ))

    #withdraw
    withdraw_reply = {'forum': note.forum, 'replyto': note.forum,
                      'signatures': {
                          "values-regex": config.CONF+"/Paper" + str(note.number) + "/Authors",
                          "description": "How your identity will be displayed."}}
    withdraw_invite = client.post_invitation(openreview.Invitation(
        id=config.CONF+'/Paper' + str(note.number) + '/-/Withdraw',
        super=super_withdraw.id,
        invitees=note.content['authorids'],
        signatures=[config.CONF],
        reply=withdraw_reply,
    ))

    #reveal authors
    reveal_reply = {'forum': note.forum, 'replyto': note.forum,
                    'signatures': {"values-regex": "~.*",
                                   "description": "How your identity will be displayed."}}
    reveal_invite = client.post_invitation(openreview.Invitation(
        id=config.CONF+'/Paper' + str(note.number) + '/-/Reveal_Authors',
        super=super_reveal.id,
        invitees=note.content['authorids'],
        signatures=[config.CONF],
        reply=reveal_reply
    ))