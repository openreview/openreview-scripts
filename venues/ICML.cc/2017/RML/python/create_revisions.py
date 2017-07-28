# import statements
import openreview
import config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print client.baseurl

# setup variables
submissions = client.get_notes(invitation = config.SUBMISSION)

def revision_invitation(n):

    revision_reply = {
        'content': config.submission_content,
        'referent': n.id,
        'forum': n.forum,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values-regex': '~.*'
        }
    }

    return openreview.Invitation(config.CONF + '/-/Paper{0}/Add/Revision'.format(n.number),
        readers = ['everyone'],
        writers = [config.CONF],
        invitees = n.content['authorids'],
        signatures = [config.CONF],
        reply = revision_reply
        )


for n in submissions:
    inv = client.post_invitation(revision_invitation(n))
    print inv.id
