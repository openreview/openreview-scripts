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
    'invitation': 'NIPS.cc/2017/Workshop/MLITS/-/Submission',
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

invitation = Invitation(id = 'NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], writers = ['OpenReview.net'], signatures = ['OpenReview.net'], invitees = ['OpenReview.net'], reply = reply, multiReply = True)

client.post_invitation(invitation)


tag = Tag(forum = 'H1gwPOLAW', replyto = 'H1gwPOLAW', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Poster')
client.post_tag(tag)

tag = Tag(forum = 'BJ4tluLAZ', replyto = 'BJ4tluLAZ', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Reject')
client.post_tag(tag)

tag = Tag(forum = 'rys_hvLRW', replyto = 'rys_hvLRW', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Oral')
client.post_tag(tag)

tag = Tag(forum = 'HyHG8LURb', replyto = 'HyHG8LURb', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Reject')
client.post_tag(tag)

tag = Tag(forum = 'HkW01LLA-', replyto = 'HkW01LLA-', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Reject')
client.post_tag(tag)

tag = Tag(forum = 'Hycq9SLCW', replyto = 'Hycq9SLCW', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Oral')
client.post_tag(tag)

tag = Tag(forum = 'rJ26HSLRb', replyto = 'rJ26HSLRb', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Oral')
client.post_tag(tag)

tag = Tag(forum = 'Bk4BBBLRZ', replyto = 'Bk4BBBLRZ', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Poster')
client.post_tag(tag)

tag = Tag(forum = 'BJ3-mrURW', replyto = 'BJ3-mrURW', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Poster')
client.post_tag(tag)

tag = Tag(forum = 'BkQszBIAW', replyto = 'BkQszBIAW', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Oral')
client.post_tag(tag)

tag = Tag(forum = 'HylddmUAZ', replyto = 'HylddmUAZ', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Poster')
client.post_tag(tag)

tag = Tag(forum = 'BypTNXUCW', replyto = 'BypTNXUCW', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Reject')
client.post_tag(tag)

tag = Tag(forum = 'Hy4q48h3Z', replyto = 'Hy4q48h3Z', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Poster')
client.post_tag(tag)

tag = Tag(forum = 'SyiF5-23Z', replyto = 'SyiF5-23Z', invitation ='NIPS.cc/2017/Workshop/MLITS/-/Decision', readers = ['everyone'], signatures = ['NIPS.cc/2017/Workshop/MLITS/Program_Chairs'], tag = 'Poster')
client.post_tag(tag)

