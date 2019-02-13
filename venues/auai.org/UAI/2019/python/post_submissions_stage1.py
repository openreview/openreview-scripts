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
    conference.set_authors()

    #Create revision invitations
    submissions = conference.get_submissions()

    for s in submissions:
        client.post_invitation(openreview.Invitation(
            id = conference.get_id() + '/-/Paper' + str(s.number) + '/Revision',
            duedate = openreview.tools.datetime_millis(datetime.datetime(2019, 3, 9, 11, 59)),
            readers = ['everyone'],
            writers = [conference.get_id()],
            signatures = [conference.get_id()],
            invitees = [conference.get_authors_id(s.number)],
            reply = {
                'forum': s.id,
                'referent': s.id,
                'readers': {
                    'values-copied': [conference.get_id(), '{content.authorids}', '{signatures}'],
                },
                'writers': {
                    'values-copied': [conference.get_id(), '{content.authorids}', '{signatures}'],
                },
                'signatures': {
                    'values-regex': '~.*',
                },
                'content': {
                    'pdf': {
                        'value-regex': 'upload',
                        'required': True
                    }
                }
            }
        ))
