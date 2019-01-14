import argparse
import openreview
from openreview import invitations
import datetime
import os
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)
    conference.close_submissions()

    submissions = client.get_notes(invitation=conference.get_submission_id())

    for paper in submissions:
        client.post_group(openreview.Group(**{
            'id': '/'.join([conference.get_id(), 'Paper{}'.format(paper.number)]),
            'readers': ['everyone'],
            'writers': [conference.get_id()],
            'signatories': [],
            'signatures': [conference.get_id()]
        }))

    bid_invitation = openreview.Invitation(**{
        'id': '/'.join([conference.get_id(), '-', 'Bid']),
        'expdate': None, # todo
        'duedate': None, # todo
        'web': os.path.abspath('../webfield/bidWebfield.js'), # todo
        'signatures': [conference.get_id()],
        'readers': [conference.get_id(), conference.get_program_chairs_id(), conference.get_area_chairs_id()],
        'invitees': [conference.get_program_chairs_id(), conference.get_area_chairs_id()],
        'writers': [conference.get_id()],
        'multiReply': True,
        'taskCompletionCount': 50,
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': conference.get_submission_id(),
            'readers': {
                'values-copied': [conference.get_id(), '{signatures}']
            },
            'signatures': {
                'values-regex': '~.*'
            },
            'content': {
                'tag': {
                    'value-radio': [
                        'Very High','High', 'Neutral', 'Low', 'Very Low', 'No Bid'
                    ],
                    'required': True
                }
            }
        }
    })
    client.post_invitation(bid_invitation)

    conflict_claim_invitation = openreview.Invitation(**{
        'id': '/'.join([conference.get_id(), '-', 'Conflict_of_Interest']),
        'duedate': None, #todo
        'expdate': None, #todo
        'readers': ['everyone'],
        'writers': [conference.get_id()],
        'signatures': [conference.get_id()],
        'invitees': ['~'],
        'multiReply': True,
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': conference.get_submission_id(),
            'readers': {
                'values': ['everyone']
            },
            'signatures': {'values-regex': '~.*'},
            'content': {
                'tag': {
                    'value-dropdown': [
                        'Yes: I am certain that I have a conflict of interest with this paper.',
                        'Maybe: I believe that I may have a conflict of interest with this paper, but I am not certain.',
                        'No: I do not have a conflict of interest with this paper.'
                    ],
                    'required': True,
                    'description': 'Do you have a conflict of interest?'
               }
            }
        }
    })
    client.post_invitation(conflict_claim_invitation)

    area_chairs_group = client.get_group(conference.get_area_chairs_id())
    with open(os.path.abspath('../webfield/programCommitteeWebfield_bidding-stage.js')) as f:
        area_chairs_group.web = f.read()
        area_chairs_group.signatories.append(area_chairs_group.id)
        client.post_group(area_chairs_group)

    print('DONE.')
