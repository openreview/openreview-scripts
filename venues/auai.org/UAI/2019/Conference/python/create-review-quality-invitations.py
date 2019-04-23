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

    map_review_to_quality = {}
    all_reviews =
    # This is the Conference level Invitation for all withdrawn submissions
    withdrawn_submission_invitation = client.post_invitation(openreview.Invitation(
        id = conference.get_id() + "/-/Withdrawn_Submission",
        readers = ['everyone'],
        writers = [conference.get_id()],
        invitees = [conference.get_id()],
        noninvitees = [],
        signatures = [conference.get_id()],
        reply = {
           'forum': None,
           'replyto': None,
           'readers': {
               'description': 'The users who will be allowed to read the reply content.',
               'values-regex': conference.get_program_chairs_id() + '|' + conference.get_id() + '/Paper[0-9]*/Authors'
           },
           'signatures': {
               'description': 'How your identity will be displayed with the above content.',
               'values': [conference.get_id()]
           },
           'writers': {
               'description': 'Users that may modify this record.',
               'values':  [conference.get_id()]
           },
           'content': {}
        },
        nonreaders = []
    ))

    # Template for per-paper withdraw submission invitation
    withdraw_submission_template = {
        'id': conference.get_id() + '/-/Paper<number>/Withdraw_Submission',
        'readers': ['everyone'],
        'writers': [conference.get_id()],
        'invitees': [conference.get_id() + '/Paper<number>/Authors'],
        'signatures': ['OpenReview.net'],
        'multiReply': False,
        'reply': {
            'forum': '<forum>',
            'replyto': '<forum>',
            'readers': {
                'description': 'Select all user groups that should be able to read this comment.',
                'values': [conference.get_program_chairs_id(), conference.get_id() + '/Paper<number>/Authors']
            },
            'signatures': {
                'description': '',
                'values-regex': conference.get_id()+'/Paper<number>/Authors',
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values':  [conference.get_id()]
            },
            'content': {
                'title': {
                    'value': 'Submission Withdrawn by the Authors',
                    'order': 1
                },
                'withdrawal confirmation': {
                    'description': withdrawal_statement,
                    'value-radio': ['I have read and agree with the withdrawal statement on behalf of myself and my co-authors.'],
                    'order': 2,
                    'required': True
                }
            }
        }
    }
    with open(os.path.abspath('../process/withdrawProcess.js')) as f:
        withdraw_submission_template['process'] = f.read()

    blind_notes = openreview.tools.iterget_notes(client, invitation=conference.get_blind_submission_id())
    for index, note in enumerate(blind_notes):
        client.post_invitation(openreview.Invitation.from_json(
            openreview.tools.fill_template(withdraw_submission_template, note)
        ))
        if (index+1)%10 == 0:
            print ('Processed ', index+1)

    print ('Processed ', index+1)