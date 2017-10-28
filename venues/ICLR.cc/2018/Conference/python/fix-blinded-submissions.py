'''
This is a one time script to add missing ICLR 2018 blind submissions.
'''

import openreview
import config
import csv
import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print client.baseurl

# get originals with missing blind copies
submissions = client.get_notes(invitation=config.SUBMISSION)
blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)

print "there are {0} submissions and {1} blind copies".format(len(submissions), len(blind_submissions))

blinds_by_original = {b.original: b for b in blind_submissions}

missing_originals = [n.id for n in submissions if n.id not in blinds_by_original]

# build the missing blind copies

def get_bibtex(note):
    first_word = note.content['title'].split(' ')[0].lower();

    return '@article{\
          \nanonymous2017' + first_word + ',\
          \ntitle={' + note.content['title'] + '},\
          \nauthor={Anonymous},\
          \njournal={International Conference on Learning Representations},\
          \nyear={2017}\
      \n}'





def get_blinded(original_note):
    blind_submission_params = {
        'original': original_note.id,
        'invitation': config.BLIND_SUBMISSION,
        'forum': None,
        'signatures': [config.CONF],
        'writers': [config.CONF],
        'readers': ['everyone'],
        'content': {
            'authors': ['Anonymous'],
            'authorids': ['ICLR.cc/2018/Conference/-/Paper{0}/Authors'.format(original_note.number)],
            '_bibtex': get_bibtex(original_note)
        }
    }
    return openreview.Note(**blind_submission_params)

for original_id in missing_originals:
    original_note = client.get_note(original_id)
    blind_note = client.post_note(get_blinded(original_note))
    print "posting blind note ", blind_note.id

submissions = client.get_notes(invitation=config.SUBMISSION)
blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)

print "there are {0} submissions and {1} blind copies".format(len(submissions), len(blind_submissions))

