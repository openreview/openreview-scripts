#!/usr/bin/python

import sys, os
import argparse
import openreview
import config

def create_deanonymize_invitation(note):
  invitation = openreview.Invitation(**{
      'id': f'{config.CONF}/-/Paper{note.number}/Deanonymize',
      'signatures': [config.CONF],
      'writers': [config.CONF],
      'invitees': [f'OpenReview.net/Anonymous_Preprint/Paper{note.number}/Authors'],
      'noninvitees': [],
      'readers': ['everyone'],
      'process': os.path.join(os.path.dirname(__file__), '../process/deanonymize_process.py'),
      'reply': {
        'forum': note.id,
        'referent': note.id,
        'signatures': config.submission_params['reply']['signatures'],
        'writers': config.submission_params['reply']['writers'],
        'readers': config.submission_params['reply']['readers'],
        'content': {
          'deanonymize': {
            'description': 'Confirm that you want to deanonymize this submission. Your identity will be permanently revealed. This cannot be undone.',
            'order': 1,
            'value-radio': ['Confirmed'],
            'required': True
          }
        }
      }
    })

  return invitation

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

for note in openreview.tools.iterget_notes(client, invitation='OpenReview.net/Anonymous_Preprint/-/Blind_Submission'):
  invitation = create_deanonymize_invitation(note)
  client.post_invitation(invitation)
