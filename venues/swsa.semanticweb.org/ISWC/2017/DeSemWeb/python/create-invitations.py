import sys, os
import argparse
import openreview
import config

def get_submit_review_invitation(submissionId, number):
    reply = {
        'forum': submissionId,
        'replyto': submissionId,
        'writers': {
            'values-regex': '~.*|%s/Paper%s/AnonReviewer' % (config.CONF, number)
        },
        'signatures': {
            'values-regex': '~.*|%s/Paper%s/AnonReviewer' % (config.CONF, number)
        },
        'readers': {
            'values': ['everyone'],
            'description': 'The users who will be allowed to read the above content.'
        },
        'nonreaders': {
            'values': []
        },
        'content': {
            'title': {
                'order': 1,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your review.',
                'required': True
            },
            'review': {
                'order': 2,
                'value-regex': '[\\S\\s]+',
                'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
                'required': True
            },
            'rating': {
                'order': 3,
                'value-dropdown': ['+3','+2','+1','0','-1','-2','-3'],
                'required': True
            }
        }
    }

    invitation = openreview.Invitation(id = config.CONF + '/-/Paper' + str(number) + '/Submit/Review',
        duedate = config.DUE_TIMESTAMP,
        signatures = [config.CONF],
        writers = [config.CONF],
        invitees = [config.PROGRAM_CHAIRS, "%s/Paper%s/Reviewers" % (config.CONF, number)],
        noninvitees = [],
        readers = ['everyone'],
        process = os.path.join(os.path.dirname(__file__), '../process/reviewProcess.js'),
        reply = reply)

    return invitation

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--overwrite',action='store_true')
args = parser.parse_args()


client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.SUBMISSION)

for n in submissions:
    papergroup = client.post_group(openreview.Group(config.CONF+'/Paper%s' % n.number, **config.group_params))
    reviewergroup = client.post_group(openreview.Group(papergroup.id+'/Reviewers', **config.group_params))
    anonreviewergroup = client.post_group(openreview.Group(papergroup.id+'/AnonReviewer', **config.group_params))


    client.post_invitation(get_submit_review_invitation(n.id, n.number))
