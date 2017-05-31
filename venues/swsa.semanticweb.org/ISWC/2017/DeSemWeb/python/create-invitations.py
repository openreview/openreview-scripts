import argparse
import openreview
import config

def get_submit_review_invitation(submissionId, number):
    reply = {
        'forum': submissionId,
        'replyto': submissionId,
        'writers': {
            'values': [config.CONF]
        },
        'signatures': {
            'values-regex': '~.*|\(anonymous\)'
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
                'value-radio': ['+3','+2','+1','0','-1','-2','-3'],
                'required': True
            }
        }
    }

    invitation = openreview.Invitation(id = config.CONF + '/-/Paper' + str(number) + '/Submit/Review',
        duedate = config.DUE_TIMESTAMP,
        signatures = [config.CONF],
        writers = [config.CONF],
        invitees = ['everyone'],
        noninvitees = [],
        readers = ['everyone'],
        process = '../process/reviewProcess.js',
        reply = reply)

    return invitation

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()


client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.SUBMISSION)

for n in submissions:
    client.post_invitation(get_submit_review_invitation(n.id, n.number))
