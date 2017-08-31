import argparse
import openreview
import config

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--hide', action = 'store_true')
parser.add_argument('--show', action = 'store_true')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
original_submissions_by_id = {i.id: i for i in client.get_notes(invitation=config.SUBMISSION)}


for b in blind_submissions:
    original_note = client.get_note(b.original)

    overwriting_note = openreview.Note(**{
        'id': b.id,
        'original': b.original,
        'invitation': config.BLIND_SUBMISSION,
        'forum': b.forum,
        'signatures': [config.CONF],
        'writers': [config.CONF],
        'readers': ['everyone'],
        'content': {
            'authors': original_note.content['authors'] if args.show and not args.hide else ['Anonymous'],
            'authorids': original_note.content['authorids'] if args.show and not args.hide else [config.CONF + '/Paper{0}/Authors'.format(b.number)]
        }
    })

    print "{0} note {1}".format('Revealing' if args.show and not args.hide else 'Hiding', overwriting_note.id)
    client.post_note(overwriting_note)
