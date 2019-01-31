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
            'invitation': 'learningtheory.org/COLT/2019/Conference/-/Blind_Submission',
            'readers': {
                'values-copied': [conference.get_id(), '{signatures}']
            },
            'signatures': {
                'values-regex': '~.*'
            },
            'content': {
                'tag': {
                    'value-radio': [
                        'Very High','High', 'Neutral', 'Low', 'Very Low', 'Conflict of Interest', 'No Bid'
                    ],
                    'required': True
                }
            }
        }
    })
    client.post_invitation(bid_invitation)
    
    area_chairs_group = client.get_group(conference.get_area_chairs_id())
    with open(os.path.abspath('../webfield/programCommitteeWebfield_bidding-stage.js')) as f:
        area_chairs_group.web = f.read()
        area_chairs_group.signatories.append(area_chairs_group.id)
        client.post_group(area_chairs_group)

    print('DONE.')
