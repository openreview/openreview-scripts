#!/usr/bin/python

import argparse
import openreview

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()


"""
This is the initialization script for the FutureData lab's internal reviewing system.

It should be run only once, by the superuser, to initialize the configuration.
Further edits should be made by the FutureData admin (Group ID: futuredata.stanford.edu/Admin)

"""

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

## Define a group representing the lab, named using the lab's domain name.
## the "web" parameter accepts a path to an html file. This file will be rendered when a user
## visits the group URL at https://openreview.net/group?id=futuredata.stanford.edu
futuredata = openreview.Group('futuredata.stanford.edu', web = '../webfield/futuredata_webfield.html')

## Define a group representing the OpenReview administrator for the lab. We will give the
## members of this group special permissions.
futuredata_admin = openreview.Group('futuredata.stanford.edu/Admin')

## Add a single member to this group, for now. Eventually the administrator will be an actual
## member of the FutureData lab.
futuredata_admin.members = ["~Michael_Spector1"]

## Add the administrator group to the futuredata.stanford.edu group. Eventually, all members
## of the lab should be added to this members list.
futuredata.members = ['futuredata.stanford.edu/Admin']

## The "writers" field determines who may edit the group futuredata.stanford.edu group, and
## the "readers" field determines who may view it.
futuredata.writers = ['futuredata.stanford.edu/Admin']
futuredata.readers = ['futuredata.stanford.edu']

## The "signatories" field determines who may "sign for" the group; in other words, anyone
## in the "signatories" field may sign posted groups, notes, and invitations in the name of
## futuredata.stanford.edu
futuredata.signatories = ['futuredata.stanford.edu/Admin']

## Use the client to post both groups to the server.
futuredata = client.post_group(futuredata)
futuredata_admin = client.post_group(futuredata_admin)



paper_submission_reply = {
    'forum': None,
    'replyto': None,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['futuredata.stanford.edu']
    },
    'signatures': {
        'description': 'How your identity will be displayed with the above content.',
        'values-regex': '~.*'
    },
    'writers': {
        'values-regex': '~.*'
    },
    'content': {
        'title': {
            'description': 'Title of paper.',
            'order': 1,
            'value-regex': '.{1,250}',
            'required':True
        },
        'authors': {
            'description': 'Comma separated list of author names.',
            'order': 2,
            'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
            'required':True
        },
        'authorids': {
            'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile.',
            'order': 3,
            'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
            'required':True
        },
        'keywords': {
            'description': 'Comma separated list of keywords.',
            'order': 6,
            'values-regex': "(^$)|[^;,\\n]+(,[^,\\n]+)*"
        },
        'TL;DR': {
            'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
            'order': 7,
            'value-regex': '[^\\n]{0,250}',
            'required':False
        },
        'abstract': {
            'description': 'Abstract of paper.',
            'order': 8,
            'value-regex': '[\\S\\s]{1,5000}',
            'required':True
        },
        'pdf': {
            'description': 'Upload a PDF file that ends with .pdf',
            'order': 9,
            'value-regex': 'upload',
            'required':True
        }
    }
}

paper_submission = openreview.Invitation('futuredata.stanford.edu/-/Paper',
    readers = ['futuredata.stanford.edu'],
    writers = ['futuredata.stanford.edu/Admin'],
    invitees = ['futuredata.stanford.edu'],
    signatures = ['futuredata.stanford.edu/Admin'],
    reply = paper_submission_reply
)

client.post_invitation(paper_submission)


## Create and post a comment invitation attached to every 'futuredata.stanford.edu/-/Paper' Note.

comment_reply = {
    'invitation': 'futuredata.stanford.edu/-/Paper',
    'forum': None,
    'replyto': None,
    'signatures': {
        'values-regex': '~.*|\(anonymous\)'
    },
    'writers': {
        'values-regex': '~.*|\(anonymous\)'
    },
    'readers': {
        'values': ['futuredata.stanford.edu']
    },
    'content': {
        'title': {
            'order': 0,
            'value-regex': '.{1,500}',
            'description': 'Brief summary of your comment.',
            'required': True
        },
        'comment': {
            'order': 1,
            'value-regex': '[\\S\\s]{1,5000}',
            'description': 'Your comment or reply.',
            'required': True
        }
    }
}

comment_invitation = openreview.Invitation('futuredata.stanford.edu/-/Comment',
    readers = ['everyone'],
    writers = ['futuredata.stanford.edu/Admin'],
    invitees = ['futuredata.stanford.edu'],
    signatures = ['futuredata.stanford.edu/Admin'],
    reply = comment_reply
    )
client.post_invitation(comment_invitation)


