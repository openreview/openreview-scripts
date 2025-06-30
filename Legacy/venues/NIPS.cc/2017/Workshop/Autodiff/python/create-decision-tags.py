## Import statements
import argparse
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

reply = {
    'forum': None,
    'replyto': None,
    'invitation': 'NIPS.cc/2017/Workshop/Autodiff/-/Submission',
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['everyone']
    },
    'signatures': {
        'description': 'Your authorized identity to be associated with the above content.',
        'values': ['OpenReview.net']
    },
    'writers': {
        'values': ['OpenReview.net']
    },
    'content':{
        'tag': {
            'description': 'Decision of paper.',
            'order': 1,
            'value-regex': '.{1,250}',
            'required': True
        }
    }
}

invitation = Invitation(id = 'NIPS.cc/2017/Workshop/Autodiff/-/Decision', readers = ['everyone'], writers = ['OpenReview.net'], signatures = ['OpenReview.net'], invitees = ['OpenReview.net'], reply = reply, multiReply = True)

client.post_invitation(invitation)

notes = client.get_notes(invitation = 'NIPS.cc/2017/Workshop/Autodiff/-/Paper.*/Acceptance_Decision')

for n in notes:
    tag = Tag(forum = n.forum, replyto = n.replyto, invitation ='NIPS.cc/2017/Workshop/Autodiff/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/Autodiff/Program_Chairs'], tag = n.content['Acceptance decision'])
    client.post_tag(tag)
