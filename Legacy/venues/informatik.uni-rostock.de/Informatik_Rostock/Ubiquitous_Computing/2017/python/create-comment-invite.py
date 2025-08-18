#!/usr/bin/python

###############################################################################
# ex. python create-invitations.py --cpath MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# To be run after submission due date to create review invitations for all the papers.
# For each paper:
# 1) create authorGroup (can see reviews, can't write a review)
#           reviewer group (reviewers for this paper)
#           and nonReviewerGroup (folks that aren't allowed to read the review at least not yet)
# 2) create review invitation
###############################################################################

## Import statements
import argparse
import sys
import os
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
#parser.add_argument('--cpath', required=True, help="conference path ex. MyConf.org/2017")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
try:
    if args.username!=None and args.password!=None:
        client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
    else:
        client = Client(baseurl=args.baseurl)
except:
    print "Error: invalid Client arguments: baseurl:{0} username:{1} password:{2}".format(args.baseurl, args.username, args.password)
    sys.exit()

## check conference directory exists
base_path = "../"
config_path = base_path+"/python/"
if os.path.isfile(config_path+"config.py") is False:
    print "Cannot locate config.py in:"+config_path
    sys.exit()
## load conference specific data
sys.path.insert(0, config_path)
import config

## Comments can be added to any paper but only by the members of the commenter group
## Comment Group
client.post_group(openreview.Group(
    id=config.COMMENTERS,
    signatures=[config.CONF],
    writers=[config.CONF],
    members=[],
    readers=[config.COMMENTERS],
    signatories=[]))
print("post group: "+config.COMMENTERS)

## check comment process function exists
process_path = base_path+'/process/commentProcess.js'
if os.path.isfile(process_path) is False:
    print "Cannot locate comment process function at:"+process_path
    sys.exit()
## Comment invitation
comment_invite = openreview.Invitation(config.COMMENT, process=process_path, **config.comment_params)
comment_reply = {
    'invitation': config.SUBMISSION,
    'forum': None,
    'replyto': None,
    'signatures': {
        'values-regex': '~.*|\(anonymous\)'
    },
    'writers': {
        'values-regex': '~.*|\(anonymous\)'
    },
    'readers': {
        'values': [config.COMMENTERS]
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
comment_invite.reply = comment_reply
client.post_invitation(comment_invite)