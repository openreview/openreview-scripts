'''

Iterates through the list of ICLR 2018 submissions and updates the bibtex field
based on the most recent version.

'''

import argparse
import openreview
import config

def get_bibtex(note):
    firstWord = note.content['title'].split(' ')[0].lower()

    return '''@article{
  anonymous2018''' + firstWord + ''',
  title={''' + note.content['title'] + '''},
  author={Anonymous},
  journal={International Conference on Learning Representations},
  year={2018},
  url={https://openreview.net/forum?id=''' + note.id + '''}
}'''

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)

for n in submissions:
    # a submission potentially has many references, but we want to change only
    # the "prime" reference, which has an ID equal to its referent.
    refs = client.get_revisions(referent=n.id)
    prime_ref = [x for x in refs if x.id == x.referent][0]

    prime_ref.content['_bibtex'] = get_bibtex(n)
    new_ref = client.post_note(prime_ref)
    print "updated {0}".format(new_ref.id)
