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
    
    comment_template = {
        'id': conference.id + '/-/Paper<number>/Comment',
        'readers': [
            conference.id,
            conference.get_program_chairs_id(),
            conference.id + '/Paper<number>/Program_Committee/Submitted'],
        'writers': [
            conference.id,
            conference.get_program_chairs_id(),
            conference.id + '/Paper<number>/Program_Committee/Submitted'
        ],
        'invitees': [
            conference.get_program_chairs_id(),
            conference.id + '/Paper<number>/Program_Committee/Submitted'
        ],
        'noninvitees': [],
        'signatures': [conference.id],
        'duedate': openreview.tools.timestamp_GMT(year=2019, month=3, day=31),
        'multiReply': False,
        'reply': {
            'forum': '<forum>',
            'replyto': None,
            'readers': {
                'description': 'The users who will be allowed to read the reply content.',
                'values': [
                    conference.id + '/Paper<number>/Program_Committee/Submitted',
                    conference.get_program_chairs_id()
                ]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': conference.id + '/Paper<number>/Program_Committee_Member[0-9]+|' + conference.id + '/Program_Chairs'
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values-copied':  [
                    conference.id,
                    '{signatures}'
                ]
            },
            'content': openreview.invitations.content.comment
        }
    }

    with open('../process/commentProcess.js', 'r') as f:
        comment_template['process'] = f.read()
    blind_notes = list(openreview.tools.iterget_notes(client, invitation=conference.get_id() + '/-/Blind_Submission'))
    for index, note in enumerate(blind_notes):
        comment_invitation = client.post_invitation(
            openreview.Invitation.from_json(
                openreview.tools.fill_template(comment_template, note)
            )
        )
        if (index+1)%10 == 0 :
            print ('Processed ', index+1)
    print ('Processed ', index+1)
