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
    revision_content = {
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
